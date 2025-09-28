"""
Data models for GitHub integration.

These models represent the GitHub entities that ContextFlow collects and stores.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GitHubRepository(BaseModel):
    """Model for GitHub Repository entity."""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool = False
    html_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GitHubIssue(BaseModel):
    """Model for GitHub Issue entity."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str = Field(..., pattern="^(open|closed)$")
    labels: List[str] = Field(default_factory=list)
    assignees: List[str] = Field(default_factory=list)  # GitHub usernames
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GitHubProject(BaseModel):
    """Model for GitHub Project entity."""
    id: int
    name: str
    body: Optional[str] = None
    state: str = Field(..., pattern="^(open|closed)$")
    number: int
    created_at: datetime
    updated_at: datetime
    columns: List[str] = Field(default_factory=list)  # Column names

    class Config:
        from_attributes = True


class GitHubMilestone(BaseModel):
    """Model for GitHub Milestone entity."""
    id: int
    number: int
    title: str
    description: Optional[str] = None
    state: str = Field(..., pattern="^(open|closed)$")
    due_on: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    open_issues: int = Field(..., ge=0)
    closed_issues: int = Field(..., ge=0)

    class Config:
        from_attributes = True


# Collection models for API responses
class GitHubIssueResponse(BaseModel):
    """Response model for GitHub API issue data."""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    labels: List[dict] = Field(default_factory=list)  # Raw label objects
    assignees: List[dict] = Field(default_factory=list)  # Raw assignee objects
    created_at: str  # ISO string
    updated_at: str
    closed_at: Optional[str] = None

    def to_issue(self) -> GitHubIssue:
        """Convert to GitHubIssue model."""
        return GitHubIssue(
            id=self.id,
            number=self.number,
            title=self.title,
            body=self.body,
            state=self.state,
            labels=[label.get("name", "") for label in self.labels],
            assignees=[assignee.get("login", "") for assignee in self.assignees],
            created_at=datetime.fromisoformat(self.created_at.replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(self.updated_at.replace('Z', '+00:00')),
            closed_at=datetime.fromisoformat(self.closed_at.replace('Z', '+00:00')) if self.closed_at else None,
        )


class GitHubProjectResponse(BaseModel):
    """Response model for GitHub API project data."""
    id: int
    name: str
    body: Optional[str] = None
    state: str
    number: int
    created_at: str
    updated_at: str

    def to_project(self) -> GitHubProject:
        """Convert to GitHubProject model."""
        return GitHubProject(
            id=self.id,
            name=self.name,
            body=self.body,
            state=self.state,
            number=self.number,
            created_at=datetime.fromisoformat(self.created_at.replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(self.updated_at.replace('Z', '+00:00')),
            columns=[],  # Columns would need separate API call
        )


class GitHubMilestoneResponse(BaseModel):
    """Response model for GitHub API milestone data."""
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

    def to_milestone(self) -> GitHubMilestone:
        """Convert to GitHubMilestone model."""
        return GitHubMilestone(
            id=self.id,
            number=self.number,
            title=self.title,
            description=self.description,
            state=self.state,
            due_on=datetime.fromisoformat(self.due_on.replace('Z', '+00:00')) if self.due_on else None,
            created_at=datetime.fromisoformat(self.created_at.replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(self.updated_at.replace('Z', '+00:00')),
            open_issues=self.open_issues,
            closed_issues=self.closed_issues,
        )


class GitHubRepositoryResponse(BaseModel):
    """Response model for GitHub API repository data."""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool
    html_url: str
    created_at: str
    updated_at: str

    def to_repository(self) -> GitHubRepository:
        """Convert to GitHubRepository model."""
        return GitHubRepository(
            id=self.id,
            name=self.name,
            full_name=self.full_name,
            description=self.description,
            private=self.private,
            html_url=self.html_url,
            created_at=datetime.fromisoformat(self.created_at.replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(self.updated_at.replace('Z', '+00:00')),
        )