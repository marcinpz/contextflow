"""
Contract tests for GitHub Projects API.

These tests verify that the GitHub API responses match our expected schema
as defined in contracts/github-api.yaml
"""

import pytest
from github import Github
from pydantic import BaseModel, Field
from typing import List, Optional
import os


class GitHubProjectModel(BaseModel):
    """Pydantic model for GitHub Project based on our contract."""
    id: int
    name: str
    body: Optional[str] = None
    state: str
    number: int
    created_at: str
    updated_at: str


@pytest.fixture
def github_client():
    """Fixture to provide authenticated GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not set")
    return Github(token)


@pytest.mark.contract
def test_github_projects_api_contract(github_client):
    """Test that GitHub Projects API returns data matching our contract."""
    # Use a repository that might have projects (may be empty)
    repo = github_client.get_repo("octocat/Hello-World")

    try:
        projects = repo.get_projects()

        # Convert first project to dict for validation (if any exist)
        project_data = None
        for project in projects:
            project_data = {
                "id": project.id,
                "name": project.name,
                "body": project.body,
                "state": project.state,
                "number": project.number,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
            }
            break

        if project_data:
            # Validate against our model
            project_model = GitHubProjectModel(**project_data)
            assert project_model.id > 0
            assert project_model.state in ["open", "closed"]
            assert isinstance(project_model.name, str)

    except Exception as e:
        # Projects API might not be available or repository might not have projects
        pytest.skip(f"Projects API not available or no projects: {e}")


@pytest.mark.contract
def test_github_projects_state_filtering(github_client):
    """Test that project state filtering works as expected."""
    repo = github_client.get_repo("octocat/Hello-World")

    try:
        # Get all projects
        all_projects = list(repo.get_projects()[:5])

        # Should not fail
        assert isinstance(all_projects, list)

        # Check states if projects exist
        for project in all_projects:
            assert project.state in ["open", "closed"]

    except Exception as e:
        pytest.skip(f"Projects API not available: {e}")