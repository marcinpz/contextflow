# Quickstart: GitHub Integration Testing

## Prerequisites
- GitHub Personal Access Token with `repo` scope
- Neo4j instance running locally
- ContextFlow environment configured

## Configuration
1. Set GitHub token in environment:
   ```bash
   export GITHUB_TOKEN=your_personal_access_token
   ```

2. Configure repositories to monitor in `config/github_config.py`:
   ```python
   GITHUB_REPOS = [
       "owner/repo1",
       "owner/repo2"
   ]
   ```

## Test Data Collection
1. Run GitHub collector:
   ```bash
   python -m src.integrations.github.collector
   ```

2. Verify data in Neo4j:
   ```cypher
   MATCH (r:GitHubRepository) RETURN r.name, count(*)
   MATCH (i:GitHubIssue) RETURN i.title, i.state LIMIT 5
   ```

## Test MCP Tools
1. Start MCP server with GitHub tools enabled
2. Query for issues:
   ```
   Find all open issues in repository owner/repo
   ```
3. Query for projects:
   ```
   Show project board for repository owner/repo
   ```

## Expected Results
- Repository nodes created in Neo4j
- Issue nodes linked to repositories
- Project and milestone nodes with relationships
- MCP tools return formatted GitHub data
- Response time < 2 seconds for queries