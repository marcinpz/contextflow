"""
GitHub data collector for ContextFlow.

This module collects GitHub data (issues, projects, milestones) and stores
it in the Neo4j graph database.
"""

import logging
from typing import List, Optional
from neo4j import GraphDatabase

from .client import GitHubClient
from .models import (
    GitHubRepository,
    GitHubIssue,
    GitHubProject,
    GitHubMilestone,
)
from src.config.github_config import (
    GITHUB_REPOS,
    GITHUB_COLLECT_ISSUES,
    GITHUB_COLLECT_PROJECTS,
    GITHUB_COLLECT_MILESTONES,
    GITHUB_LABEL_REPOSITORY,
    GITHUB_LABEL_ISSUE,
    GITHUB_LABEL_PROJECT,
    GITHUB_LABEL_MILESTONE,
    REL_BELONGS_TO,
    REL_HOSTED_IN,
    REL_ASSIGNED_TO,
    REL_TARGETS,
)

logger = logging.getLogger(__name__)


class GitHubCollector:
    """Collector for GitHub data."""

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", neo4j_password: str = "password"):
        """Initialize the collector.

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.github_client = GitHubClient()

    def collect_repository(self, repo_full_name: str) -> GitHubRepository:
        """Collect repository data.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            GitHubRepository: Repository data
        """
        owner, repo = repo_full_name.split('/', 1)
        repo_response = self.github_client.get_repository(owner, repo)
        repository = repo_response.to_repository()

        # Store in Neo4j
        with self.neo4j_driver.session() as session:
            session.run(f"""
                MERGE (r:{GITHUB_LABEL_REPOSITORY} {{id: $id}})
                SET r.name = $name,
                    r.full_name = $full_name,
                    r.description = $description,
                    r.private = $private,
                    r.html_url = $html_url,
                    r.created_at = datetime($created_at),
                    r.updated_at = datetime($updated_at)
                """, {
                    "id": repository.id,
                    "name": repository.name,
                    "full_name": repository.full_name,
                    "description": repository.description,
                    "private": repository.private,
                    "html_url": repository.html_url,
                    "created_at": repository.created_at.isoformat(),
                    "updated_at": repository.updated_at.isoformat(),
                })

        logger.info(f"Collected repository: {repo_full_name}")
        return repository

    def collect_issues(self, repo_full_name: str) -> List[GitHubIssue]:
        """Collect issues for a repository.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            List[GitHubIssue]: List of issues
        """
        if not GITHUB_COLLECT_ISSUES:
            return []

        issues = []
        for issue_response in self.github_client.get_issues(repo_full_name, state="all"):
            issue = issue_response.to_issue()
            issues.append(issue)

            # Store in Neo4j
            with self.neo4j_driver.session() as session:
                session.run(f"""
                    MATCH (r:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                    MERGE (i:{GITHUB_LABEL_ISSUE} {{id: $id}})
                    SET i.number = $number,
                        i.title = $title,
                        i.body = $body,
                        i.state = $state,
                        i.labels = $labels,
                        i.assignees = $assignees,
                        i.created_at = datetime($created_at),
                        i.updated_at = datetime($updated_at),
                        i.closed_at = CASE WHEN $closed_at IS NOT NULL THEN datetime($closed_at) ELSE null END
                    MERGE (i)-[:{REL_BELONGS_TO}]->(r)
                    """, {
                        "repo_name": repo_full_name,
                        "id": issue.id,
                        "number": issue.number,
                        "title": issue.title,
                        "body": issue.body,
                        "state": issue.state,
                        "labels": issue.labels,
                        "assignees": issue.assignees,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    })

        logger.info(f"Collected {len(issues)} issues for {repo_full_name}")
        return issues

    def collect_projects(self, repo_full_name: str) -> List[GitHubProject]:
        """Collect projects for a repository.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            List[GitHubProject]: List of projects
        """
        if not GITHUB_COLLECT_PROJECTS:
            return []

        projects = []
        for project_response in self.github_client.get_projects(repo_full_name):
            project = project_response.to_project()
            projects.append(project)

            # Store in Neo4j
            with self.neo4j_driver.session() as session:
                session.run(f"""
                    MATCH (r:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                    MERGE (p:{GITHUB_LABEL_PROJECT} {{id: $id}})
                    SET p.name = $name,
                        p.body = $body,
                        p.state = $state,
                        p.number = $number,
                        p.created_at = datetime($created_at),
                        p.updated_at = datetime($updated_at),
                        p.columns = $columns
                    MERGE (p)-[:{REL_HOSTED_IN}]->(r)
                    """, {
                        "repo_name": repo_full_name,
                        "id": project.id,
                        "name": project.name,
                        "body": project.body,
                        "state": project.state,
                        "number": project.number,
                        "created_at": project.created_at.isoformat(),
                        "updated_at": project.updated_at.isoformat(),
                        "columns": project.columns,
                    })

        logger.info(f"Collected {len(projects)} projects for {repo_full_name}")
        return projects

    def collect_milestones(self, repo_full_name: str) -> List[GitHubMilestone]:
        """Collect milestones for a repository.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            List[GitHubMilestone]: List of milestones
        """
        if not GITHUB_COLLECT_MILESTONES:
            return []

        milestones = []
        for milestone_response in self.github_client.get_milestones(repo_full_name, state="all"):
            milestone = milestone_response.to_milestone()
            milestones.append(milestone)

            # Store in Neo4j
            with self.neo4j_driver.session() as session:
                session.run(f"""
                    MATCH (r:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                    MERGE (m:{GITHUB_LABEL_MILESTONE} {{id: $id}})
                    SET m.number = $number,
                        m.title = $title,
                        m.description = $description,
                        m.state = $state,
                        m.due_on = CASE WHEN $due_on IS NOT NULL THEN datetime($due_on) ELSE null END,
                        m.created_at = datetime($created_at),
                        m.updated_at = datetime($updated_at),
                        m.open_issues = $open_issues,
                        m.closed_issues = $closed_issues
                    MERGE (m)-[:{REL_BELONGS_TO}]->(r)
                    """, {
                        "repo_name": repo_full_name,
                        "id": milestone.id,
                        "number": milestone.number,
                        "title": milestone.title,
                        "description": milestone.description,
                        "state": milestone.state,
                        "due_on": milestone.due_on.isoformat() if milestone.due_on else None,
                        "created_at": milestone.created_at.isoformat(),
                        "updated_at": milestone.updated_at.isoformat(),
                        "open_issues": milestone.open_issues,
                        "closed_issues": milestone.closed_issues,
                    })

        logger.info(f"Collected {len(milestones)} milestones for {repo_full_name}")
        return milestones

    def collect_repository_data(self, repo_full_name: str):
        """Collect all data for a repository.

        Args:
            repo_full_name: Repository in format "owner/repo"
        """
        logger.info(f"Starting collection for repository: {repo_full_name}")

        # Collect repository
        self.collect_repository(repo_full_name)

        # Collect issues, projects, milestones
        self.collect_issues(repo_full_name)
        self.collect_projects(repo_full_name)
        self.collect_milestones(repo_full_name)

        logger.info(f"Completed collection for repository: {repo_full_name}")

    def close(self):
        """Close the Neo4j driver."""
        self.neo4j_driver.close()


def collect_github_data(repositories: Optional[List[str]] = None,
                       neo4j_uri: str = "bolt://localhost:7687",
                       neo4j_user: str = "neo4j",
                       neo4j_password: str = "password"):
    """Collect GitHub data for specified repositories.

    Args:
        repositories: List of repositories in "owner/repo" format.
                     If None, uses GITHUB_REPOS from config.
        neo4j_uri: Neo4j connection URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
    """
    repos = repositories or GITHUB_REPOS
    if not repos:
        logger.warning("No repositories specified for collection")
        return

    collector = GitHubCollector(neo4j_uri, neo4j_user, neo4j_password)

    try:
        for repo in repos:
            try:
                collector.collect_repository_data(repo)
            except Exception as e:
                logger.error(f"Failed to collect data for {repo}: {e}")
    finally:
        collector.close()