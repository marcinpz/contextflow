"""
GitHub integration configuration for ContextFlow.
"""

import os
from typing import List

# GitHub Personal Access Token
# Must have 'repo' scope for private repositories
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Repositories to monitor
# Format: "owner/repo"
GITHUB_REPOS: List[str] = [
    # Add your repositories here
    # "owner/repo1",
    # "owner/repo2",
]

# API rate limiting
GITHUB_API_TIMEOUT = 30  # seconds
GITHUB_MAX_RETRIES = 3
GITHUB_RETRY_DELAY = 1  # seconds, exponential backoff

# Data collection settings
GITHUB_COLLECT_ISSUES = True
GITHUB_COLLECT_PROJECTS = True
GITHUB_COLLECT_MILESTONES = True

# Neo4j labels for GitHub entities
GITHUB_LABEL_REPOSITORY = "GitHubRepository"
GITHUB_LABEL_ISSUE = "GitHubIssue"
GITHUB_LABEL_PROJECT = "GitHubProject"
GITHUB_LABEL_MILESTONE = "GitHubMilestone"

# Relationship types
REL_BELONGS_TO = "BELONGS_TO"
REL_HOSTED_IN = "HOSTED_IN"
REL_ASSIGNED_TO = "ASSIGNED_TO"
REL_TARGETS = "TARGETS"