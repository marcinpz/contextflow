"""
GitHub integration for ContextFlow.

This module provides functionality to collect and process GitHub data
including issues, projects, and milestones.
"""

from .models import (
    GitHubRepository,
    GitHubIssue,
    GitHubProject,
    GitHubMilestone,
    GitHubIssueResponse,
    GitHubProjectResponse,
    GitHubMilestoneResponse,
    GitHubRepositoryResponse,
)

__all__ = [
    "GitHubRepository",
    "GitHubIssue",
    "GitHubProject",
    "GitHubMilestone",
    "GitHubIssueResponse",
    "GitHubProjectResponse",
    "GitHubMilestoneResponse",
    "GitHubRepositoryResponse",
]