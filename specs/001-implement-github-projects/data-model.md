# Data Model: GitHub Integration

## Entities

### GitHubRepository
- **id**: Integer (GitHub repository ID)
- **name**: String (repository name)
- **full_name**: String (owner/name format)
- **description**: String (optional)
- **private**: Boolean
- **html_url**: String (GitHub URL)
- **created_at**: DateTime
- **updated_at**: DateTime

### GitHubIssue
- **id**: Integer (GitHub issue ID)
- **number**: Integer (issue number in repo)
- **title**: String
- **body**: String (markdown content)
- **state**: Enum (open, closed)
- **labels**: List<String> (label names)
- **assignees**: List<String> (GitHub usernames)
- **created_at**: DateTime
- **updated_at**: DateTime
- **closed_at**: DateTime (optional)

**Relationships**:
- BELONGS_TO → GitHubRepository
- ASSIGNED_TO → GitHubProject (with column property)
- TARGETS → GitHubMilestone

### GitHubProject
- **id**: Integer (GitHub project ID)
- **name**: String
- **body**: String (description)
- **state**: Enum (open, closed)
- **number**: Integer (project number)
- **created_at**: DateTime
- **updated_at**: DateTime
- **columns**: List<String> (column names)

**Relationships**:
- HOSTED_IN → GitHubRepository
- HAS_ISSUE ← GitHubIssue (with column property)

### GitHubMilestone
- **id**: Integer (GitHub milestone ID)
- **number**: Integer (milestone number)
- **title**: String
- **description**: String
- **state**: Enum (open, closed)
- **due_on**: Date (optional)
- **created_at**: DateTime
- **updated_at**: DateTime
- **open_issues**: Integer
- **closed_issues**: Integer

**Relationships**:
- BELONGS_TO → GitHubRepository
- HAS_ISSUE ← GitHubIssue

## Validation Rules
- Repository ID must be unique
- Issue number must be unique within repository
- Project/Milestone numbers must be unique within repository
- State enums must match GitHub values
- Dates must be valid ISO format

## State Transitions
- Issue: open → closed (no reopen support initially)
- Project: open → closed
- Milestone: open → closed