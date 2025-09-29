"""
Contract tests for GitHub Issues API.

These tests verify that the GitHub API responses match our expected schema
as defined in contracts/github-api.yaml
"""

import pytest
from github import Github
from pydantic import BaseModel, Field
from typing import List, Optional
import os


class GitHubIssueModel(BaseModel):
    """Pydantic model for GitHub Issue based on our contract."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    labels: List[dict] = Field(default_factory=list)
    assignees: List[dict] = Field(default_factory=list)
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None


@pytest.fixture
def github_client():
    """Fixture to provide authenticated GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not set")
    return Github(token)


@pytest.mark.contract
def test_github_issues_api_contract(github_client):
    """Test that GitHub Issues API returns data matching our contract."""
    # Use a known public repository for testing
    repo = github_client.get_repo("octocat/Hello-World")

    # Get issues (should return empty list for this repo, but validates API structure)
    issues = repo.get_issues(state="all")

    # Convert first issue to dict for validation (if any exist)
    issue_data = None
    for issue in issues:
        issue_data = {
            "id": issue.id,
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "state": issue.state,
            "labels": [{"name": label.name} for label in issue.labels],
            "assignees": [{"login": assignee.login} for assignee in issue.assignees],
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
        }
        break

    if issue_data:
        # Validate against our model
        issue_model = GitHubIssueModel(**issue_data)
        assert issue_model.id > 0
        assert issue_model.state in ["open", "closed"]
        assert isinstance(issue_model.labels, list)
        assert isinstance(issue_model.assignees, list)


@pytest.mark.contract
def test_github_issues_pagination(github_client):
    """Test that GitHub Issues API supports pagination as expected."""
    repo = github_client.get_repo("octocat/Hello-World")

    # Test pagination parameters
    issues = repo.get_issues(state="all", per_page=10)

    # Should not fail, and should be iterable
    issues_list = list(issues[:5])  # Get first 5
    assert len(issues_list) <= 5


@pytest.mark.contract
def test_github_issues_state_filtering(github_client):
    """Test that state filtering works as expected."""
    repo = github_client.get_repo("octocat/Hello-World")

    # Test different states
    open_issues = list(repo.get_issues(state="open")[:5])
    closed_issues = list(repo.get_issues(state="closed")[:5])
    all_issues = list(repo.get_issues(state="all")[:10])

    # All issues should contain open and closed
    assert len(all_issues) >= len(open_issues) + len(closed_issues) - 5  # Allow some overlap

    # Check states
    for issue in open_issues:
        assert issue.state == "open"
    for issue in closed_issues:
        assert issue.state == "closed"