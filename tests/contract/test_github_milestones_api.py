"""
Contract tests for GitHub Milestones API.

These tests verify that the GitHub API responses match our expected schema
as defined in contracts/github-api.yaml
"""

import pytest
from github import Github
from pydantic import BaseModel, Field
from typing import Optional
import os


class GitHubMilestoneModel(BaseModel):
    """Pydantic model for GitHub Milestone based on our contract."""
    id: int
    number: int
    title: str
    description: Optional[str] = None
    state: str
    due_on: Optional[str] = None
    created_at: str
    updated_at: str
    open_issues: int
    closed_issues: int


@pytest.fixture
def github_client():
    """Fixture to provide authenticated GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not set")
    return Github(token)


@pytest.mark.contract
def test_github_milestones_api_contract(github_client):
    """Test that GitHub Milestones API returns data matching our contract."""
    # Use a repository that might have milestones
    repo = github_client.get_repo("octocat/Hello-World")

    milestones = repo.get_milestones(state="all")

    # Convert first milestone to dict for validation (if any exist)
    milestone_data = None
    for milestone in milestones:
        milestone_data = {
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
        }
        break

    if milestone_data:
        # Validate against our model
        milestone_model = GitHubMilestoneModel(**milestone_data)
        assert milestone_model.id > 0
        assert milestone_model.state in ["open", "closed"]
        assert milestone_model.open_issues >= 0
        assert milestone_model.closed_issues >= 0


@pytest.mark.contract
def test_github_milestones_state_filtering(github_client):
    """Test that milestone state filtering works as expected."""
    repo = github_client.get_repo("octocat/Hello-World")

    # Test different states
    open_milestones = list(repo.get_milestones(state="open")[:5])
    closed_milestones = list(repo.get_milestones(state="closed")[:5])
    all_milestones = list(repo.get_milestones(state="all")[:10])

    # All milestones should contain open and closed
    assert len(all_milestones) >= len(open_milestones) + len(closed_milestones) - 5  # Allow some overlap

    # Check states
    for milestone in open_milestones:
        assert milestone.state == "open"
    for milestone in closed_milestones:
        assert milestone.state == "closed"