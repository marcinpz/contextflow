# Jira data models

from typing import Optional, List
from pydantic import BaseModel


class JiraIssue(BaseModel):
    """Jira issue model."""
    key: str
    summary: str
    description: Optional[str] = None
    issue_type: str
    status: str
    assignee: Optional[str] = None
    reporter: str
    created: str
    updated: str
    labels: List[str] = []
    priority: Optional[str] = None
    parent_key: Optional[str] = None  # For stories linked to epics


class JiraProject(BaseModel):
    """Jira project model."""
    key: str
    name: str
    description: Optional[str] = None
    project_type: str