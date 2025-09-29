"""
Unit tests for GitHub data models.
"""

import pytest
from datetime import datetime
from src.integrations.github.models import (
    GitHubRepository,
    GitHubIssue,
    GitHubProject,
    GitHubMilestone,
    GitHubIssueResponse,
    GitHubProjectResponse,
    GitHubMilestoneResponse,
    GitHubRepositoryResponse,
)


class TestGitHubModels:
    """Test GitHub data models."""

    def test_github_repository_model(self):
        """Test GitHubRepository model creation and validation."""
        repo = GitHubRepository(
            id=123,
            name="test-repo",
            full_name="owner/test-repo",
            description="A test repository",
            private=False,
            html_url="https://github.com/owner/test-repo",
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 2)
        )

        assert repo.id == 123
        assert repo.name == "test-repo"
        assert repo.full_name == "owner/test-repo"
        assert repo.private is False

    def test_github_issue_model(self):
        """Test GitHubIssue model creation and validation."""
        issue = GitHubIssue(
            id=456,
            number=1,
            title="Test Issue",
            body="This is a test issue",
            state="open",
            labels=["bug", "help wanted"],
            assignees=["user1", "user2"],
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 2),
            closed_at=None
        )

        assert issue.id == 456
        assert issue.number == 1
        assert issue.state == "open"
        assert "bug" in issue.labels
        assert len(issue.assignees) == 2

    def test_github_issue_invalid_state(self):
        """Test GitHubIssue model rejects invalid states."""
        with pytest.raises(ValueError):
            GitHubIssue(
                id=456,
                number=1,
                title="Test Issue",
                state="invalid",  # Invalid state
                created_at=datetime(2023, 1, 1),
                updated_at=datetime(2023, 1, 2)
            )

    def test_github_project_model(self):
        """Test GitHubProject model creation."""
        project = GitHubProject(
            id=789,
            name="Test Project",
            body="Project description",
            state="open",
            number=1,
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 2),
            columns=["To Do", "In Progress", "Done"]
        )

        assert project.id == 789
        assert project.name == "Test Project"
        assert project.state == "open"
        assert len(project.columns) == 3

    def test_github_milestone_model(self):
        """Test GitHubMilestone model creation."""
        milestone = GitHubMilestone(
            id=101,
            number=1,
            title="Sprint 1",
            description="First sprint",
            state="open",
            due_on=datetime(2023, 2, 1),
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 2),
            open_issues=5,
            closed_issues=2
        )

        assert milestone.id == 101
        assert milestone.title == "Sprint 1"
        assert milestone.open_issues == 5
        assert milestone.closed_issues == 2

    def test_github_issue_response_conversion(self):
        """Test conversion from GitHubIssueResponse to GitHubIssue."""
        response = GitHubIssueResponse(
            id=456,
            number=1,
            title="Test Issue",
            body="Description",
            state="open",
            labels=[{"name": "bug"}],
            assignees=[{"login": "user1"}],
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-02T00:00:00Z",
            closed_at=None
        )

        issue = response.to_issue()

        assert issue.id == 456
        assert issue.title == "Test Issue"
        assert issue.state == "open"
        assert issue.labels == ["bug"]
        assert issue.assignees == ["user1"]
        assert issue.closed_at is None

    def test_github_repository_response_conversion(self):
        """Test conversion from GitHubRepositoryResponse to GitHubRepository."""
        response = GitHubRepositoryResponse(
            id=123,
            name="test-repo",
            full_name="owner/test-repo",
            description="Test repo",
            private=False,
            html_url="https://github.com/owner/test-repo",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-02T00:00:00Z"
        )

        repo = response.to_repository()

        assert repo.id == 123
        assert repo.name == "test-repo"
        assert repo.full_name == "owner/test-repo"
        assert repo.private is False