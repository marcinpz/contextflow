"""
GitHub API client for ContextFlow.

This module provides a client for interacting with the GitHub API
using PyGitHub library with proper error handling and rate limiting.
"""

import time
import logging
from typing import Optional, Iterator
from github import Github, GithubException

from .models import (
    GitHubRepositoryResponse,
    GitHubIssueResponse,
    GitHubProjectResponse,
    GitHubMilestoneResponse,
)
from src.config.github_config import (
    GITHUB_TOKEN,
    GITHUB_API_TIMEOUT,
    GITHUB_MAX_RETRIES,
    GITHUB_RETRY_DELAY,
)

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client.

        Args:
            token: GitHub personal access token. If None, uses GITHUB_TOKEN env var.
        """
        self.token = token or GITHUB_TOKEN
        if not self.token:
            raise ValueError("GitHub token is required")

        self.github = Github(self.token, timeout=GITHUB_API_TIMEOUT)
        self._rate_limit_remaining = None
        self._rate_limit_reset = None

    def _handle_rate_limit(self):
        """Handle GitHub API rate limiting with exponential backoff."""
        if self._rate_limit_remaining is not None and self._rate_limit_remaining <= 0:
            if self._rate_limit_reset:
                sleep_time = max(0, self._rate_limit_reset - time.time())
                logger.warning(f"Rate limit exceeded, sleeping for {sleep_time:.1f} seconds")
                time.sleep(sleep_time)

    def _retry_on_exception(self, func, *args, **kwargs):
        """Retry function on exceptions with exponential backoff."""
        for attempt in range(GITHUB_MAX_RETRIES):
            try:
                self._handle_rate_limit()
                result = func(*args, **kwargs)

                # Update rate limit info
                try:
                    rate_limit = self.github.rate_limiting
                    self._rate_limit_remaining = rate_limit[0]
                    self._rate_limit_reset = rate_limit[1]
                except AttributeError:
                    pass  # Rate limiting info not available

                return result
            except GithubException as e:
                if e.status == 403 and 'rate limit' in str(e).lower():
                    # Rate limit hit, wait and retry
                    sleep_time = GITHUB_RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Rate limit hit, retrying in {sleep_time:.1f} seconds")
                    time.sleep(sleep_time)
                elif e.status >= 500:
                    # Server error, retry
                    sleep_time = GITHUB_RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Server error {e.status}, retrying in {sleep_time:.1f} seconds")
                    time.sleep(sleep_time)
                else:
                    # Client error, don't retry
                    raise
            except Exception as e:
                if attempt < GITHUB_MAX_RETRIES - 1:
                    sleep_time = GITHUB_RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Unexpected error, retrying in {sleep_time:.1f} seconds: {e}")
                    time.sleep(sleep_time)
                else:
                    raise

        raise RuntimeError(f"Failed after {GITHUB_MAX_RETRIES} attempts")

    def get_repository(self, owner: str, repo: str) -> GitHubRepositoryResponse:
        """Get repository information.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            GitHubRepositoryResponse: Repository data
        """
        def _get_repo():
            gh_repo = self.github.get_repo(f"{owner}/{repo}")
            return GitHubRepositoryResponse(
                id=gh_repo.id,
                name=gh_repo.name,
                full_name=gh_repo.full_name,
                description=gh_repo.description,
                private=gh_repo.private,
                html_url=gh_repo.html_url,
                created_at=gh_repo.created_at.isoformat(),
                updated_at=gh_repo.updated_at.isoformat(),
            )

        return self._retry_on_exception(_get_repo)

    def get_issues(self, owner: str, repo: str, state: str = "all") -> Iterator[GitHubIssueResponse]:
        """Get repository issues.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state filter ("open", "closed", "all")

        Yields:
            GitHubIssueResponse: Issue data
        """
        def _get_issues():
            gh_repo = self.github.get_repo(f"{owner}/{repo}")
            issues = gh_repo.get_issues(state=state)
            for issue in issues:
                yield GitHubIssueResponse(
                    id=issue.id,
                    number=issue.number,
                    title=issue.title,
                    body=issue.body,
                    state=issue.state,
                    labels=[{"name": label.name} for label in issue.labels],
                    assignees=[{"login": assignee.login} for assignee in issue.assignees],
                    created_at=issue.created_at.isoformat(),
                    updated_at=issue.updated_at.isoformat(),
                    closed_at=issue.closed_at.isoformat() if issue.closed_at else None,
                )

        for issue in self._retry_on_exception(_get_issues):
            yield issue

    def get_projects(self, owner: str, repo: str) -> Iterator[GitHubProjectResponse]:
        """Get repository projects.

        Args:
            owner: Repository owner
            repo: Repository name

        Yields:
            GitHubProjectResponse: Project data
        """
        def _get_projects():
            gh_repo = self.github.get_repo(f"{owner}/{repo}")
            try:
                projects = gh_repo.get_projects()
                for project in projects:
                    yield GitHubProjectResponse(
                        id=project.id,
                        name=project.name,
                        body=project.body,
                        state=project.state,
                        number=project.number,
                        created_at=project.created_at.isoformat(),
                        updated_at=project.updated_at.isoformat(),
                    )
            except GithubException as e:
                if e.status == 404:
                    # Projects API not available for this repo
                    logger.warning(f"Projects API not available for {owner}/{repo}")
                    return
                raise

        for project in self._retry_on_exception(_get_projects):
            yield project

    def get_milestones(self, owner: str, repo: str, state: str = "all") -> Iterator[GitHubMilestoneResponse]:
        """Get repository milestones.

        Args:
            owner: Repository owner
            repo: Repository name
            state: Milestone state filter ("open", "closed", "all")

        Yields:
            GitHubMilestoneResponse: Milestone data
        """
        def _get_milestones():
            gh_repo = self.github.get_repo(f"{owner}/{repo}")
            milestones = gh_repo.get_milestones(state=state)
            for milestone in milestones:
                yield GitHubMilestoneResponse(
                    id=milestone.id,
                    number=milestone.number,
                    title=milestone.title,
                    description=milestone.description,
                    state=milestone.state,
                    due_on=milestone.due_on.isoformat() if milestone.due_on else None,
                    created_at=milestone.created_at.isoformat(),
                    updated_at=milestone.updated_at.isoformat(),
                    open_issues=milestone.open_issues,
                    closed_issues=milestone.closed_issues,
                )

        for milestone in self._retry_on_exception(_get_milestones):
            yield milestone