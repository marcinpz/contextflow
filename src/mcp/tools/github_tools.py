"""
MCP tools for GitHub data queries.

This module provides Model Context Protocol tools for querying GitHub data
stored in Neo4j, making it available to AI assistants.
"""

from typing import Any, Dict, List
from neo4j import GraphDatabase

from src.config.github_config import (
    GITHUB_LABEL_REPOSITORY,
    GITHUB_LABEL_ISSUE,
    GITHUB_LABEL_PROJECT,
    GITHUB_LABEL_MILESTONE,
    REL_BELONGS_TO,
    REL_HOSTED_IN,
    REL_ASSIGNED_TO,
    REL_TARGETS,
)


class GitHubTools:
    """MCP tools for GitHub data access."""

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", neo4j_password: str = "password"):
        """Initialize GitHub tools.

        Args:
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        """Close the Neo4j driver."""
        self.driver.close()

    def find_issues_by_repo(self, repo_name: str, state: str = "all", limit: int = 10) -> Dict[str, Any]:
        """Find issues in a specific repository.

        Args:
            repo_name: Repository full name (owner/repo)
            state: Issue state filter ("open", "closed", "all")
            limit: Maximum number of issues to return

        Returns:
            Dict with issues data
        """
        with self.driver.session() as session:
            if state == "all":
                state_filter = ""
            else:
                state_filter = f"AND i.state = '{state}'"

            query = f"""
                MATCH (i:{GITHUB_LABEL_ISSUE})-[r:{REL_BELONGS_TO}]->(repo:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                WHERE {state_filter.lstrip('AND ')}
                RETURN i {{
                    .id,
                    .number,
                    .title,
                    .state,
                    .labels,
                    .assignees,
                    .created_at,
                    .updated_at
                }} as issue
                ORDER BY i.updated_at DESC
                LIMIT $limit
                """
            result = session.run(query, {"repo_name": repo_name, "limit": limit})

            issues = [record["issue"] for record in result]

            return {
                "repository": repo_name,
                "issues": issues,
                "count": len(issues),
                "filter": {"state": state, "limit": limit}
            }

    def find_open_issues_with_labels(self, labels: List[str], repo_name: str = None, limit: int = 10) -> Dict[str, Any]:
        """Find open issues with specific labels.

        Args:
            labels: List of label names to search for
            repo_name: Optional repository filter
            limit: Maximum number of issues to return

        Returns:
            Dict with issues data
        """
        with self.driver.session() as session:
            repo_filter = ""
            params = {"labels": labels, "limit": limit}

            if repo_name:
                repo_filter = f"MATCH (i)-[:{REL_BELONGS_TO}]->(r:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})"
                params["repo_name"] = repo_name

            query = f"""
                MATCH (i:{GITHUB_LABEL_ISSUE})
                {repo_filter}
                WHERE i.state = 'open'
                AND any(label IN i.labels WHERE label IN $labels)
                RETURN i {{
                    .id,
                    .number,
                    .title,
                    .state,
                    .labels,
                    .assignees,
                    .created_at,
                    .updated_at
                }} as issue,
                CASE WHEN $repo_name IS NOT NULL
                     THEN $repo_name
                     ELSE [(i)-[:{REL_BELONGS_TO}]->(r) | r.full_name][0]
                END as repository
                ORDER BY i.updated_at DESC
                LIMIT $limit
                """
            result = session.run(query, params)

            issues = []
            for record in result:
                issue = dict(record["issue"])
                repo = record["repository"]
                if repo:
                    issue["repository"] = str(repo)
                issues.append(issue)

            return {
                "issues": issues,
                "count": len(issues),
                "filter": {"labels": labels, "repository": repo_name, "limit": limit}
            }

    def get_project_board(self, repo_name: str, project_number: int = None) -> Dict[str, Any]:
        """Get project board information.

        Args:
            repo_name: Repository full name (owner/repo)
            project_number: Optional project number filter

        Returns:
            Dict with project data
        """
        with self.driver.session() as session:
            project_filter = ""
            params = {"repo_name": repo_name}

            if project_number:
                project_filter = "AND p.number = $project_number"
                params["project_number"] = project_number

            result = session.run(f"""
                MATCH (p:{GITHUB_LABEL_PROJECT})-[r:{REL_HOSTED_IN}]->(repo:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                WHERE {project_filter.lstrip('AND ')}
                OPTIONAL MATCH (p)<-[assigned:{REL_ASSIGNED_TO}]-(i:{GITHUB_LABEL_ISSUE})
                RETURN p {{
                    .id,
                    .name,
                    .body,
                    .state,
                    .number,
                    .columns,
                    issues: collect(DISTINCT i {{
                        .id,
                        .number,
                        .title,
                        .state,
                        column: assigned.column
                    }})
                }} as project
                ORDER BY p.number
                """, params)

            projects = [record["project"] for record in result]

            return {
                "repository": repo_name,
                "projects": projects,
                "count": len(projects)
            }

    def get_milestone_progress(self, repo_name: str, milestone_number: int = None) -> Dict[str, Any]:
        """Get milestone progress information.

        Args:
            repo_name: Repository full name (owner/repo)
            milestone_number: Optional milestone number filter

        Returns:
            Dict with milestone data
        """
        with self.driver.session() as session:
            milestone_filter = ""
            params = {"repo_name": repo_name}

            if milestone_number:
                milestone_filter = "AND m.number = $milestone_number"
                params["milestone_number"] = milestone_number

            result = session.run(f"""
                MATCH (m:{GITHUB_LABEL_MILESTONE})-[r:{REL_BELONGS_TO}]->(repo:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})
                WHERE {milestone_filter.lstrip('AND ')}
                OPTIONAL MATCH (m)<-[:{REL_TARGETS}]-(i:{GITHUB_LABEL_ISSUE})
                RETURN m {{
                    .id,
                    .number,
                    .title,
                    .description,
                    .state,
                    .due_on,
                    .created_at,
                    .updated_at,
                    .open_issues,
                    .closed_issues,
                    issues: collect(DISTINCT i {{
                        .id,
                        .number,
                        .title,
                        .state
                    }})
                }} as milestone
                ORDER BY m.number
                """, params)

            milestones = [record["milestone"] for record in result]

            return {
                "repository": repo_name,
                "milestones": milestones,
                "count": len(milestones)
            }

    def search_issues_by_text(self, query: str, repo_name: str = None, limit: int = 10) -> Dict[str, Any]:
        """Search issues by text content.

        Args:
            query: Search query string
            repo_name: Optional repository filter
            limit: Maximum number of results

        Returns:
            Dict with matching issues
        """
        with self.driver.session() as session:
            repo_filter = ""
            params = {"query": f".*{query}.*", "limit": limit}

            if repo_name:
                repo_filter = f"MATCH (i)-[:{REL_BELONGS_TO}]->(r:{GITHUB_LABEL_REPOSITORY} {{full_name: $repo_name}})"
                params["repo_name"] = repo_name

            # Note: This is a simple text search. In production, consider using full-text indexes
            result = session.run(f"""
                MATCH (i:{GITHUB_LABEL_ISSUE})
                {repo_filter}
                WHERE i.title =~ $query OR i.body =~ $query
                RETURN i {{
                    .id,
                    .number,
                    .title,
                    .body,
                    .state,
                    .labels,
                    .created_at,
                    .updated_at
                }} as issue,
                CASE WHEN $repo_name IS NOT NULL
                     THEN $repo_name
                     ELSE [(i)-[:{REL_BELONGS_TO}]->(r) | r.full_name][0]
                END as repository
                ORDER BY i.updated_at DESC
                LIMIT $limit
                """, params)

            issues = []
            for record in result:
                issue = record["issue"]
                issue["repository"] = record["repository"]
                issues.append(issue)

            return {
                "query": query,
                "issues": issues,
                "count": len(issues),
                "filter": {"repository": repo_name, "limit": limit}
            }


# MCP Tool definitions for integration
GITHUB_MCP_TOOLS = [
    {
        "name": "find_issues_by_repo",
        "description": "Find issues in a specific GitHub repository",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {"type": "string", "description": "Repository full name (owner/repo)"},
                "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "all"},
                "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100}
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "find_open_issues_with_labels",
        "description": "Find open issues with specific labels",
        "input_schema": {
            "type": "object",
            "properties": {
                "labels": {"type": "array", "items": {"type": "string"}},
                "repo_name": {"type": "string", "description": "Optional repository filter"},
                "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100}
            },
            "required": ["labels"]
        }
    },
    {
        "name": "get_project_board",
        "description": "Get GitHub project board information",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {"type": "string", "description": "Repository full name (owner/repo)"},
                "project_number": {"type": "integer", "description": "Optional project number"}
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_milestone_progress",
        "description": "Get milestone progress information",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {"type": "string", "description": "Repository full name (owner/repo)"},
                "milestone_number": {"type": "integer", "description": "Optional milestone number"}
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "search_issues_by_text",
        "description": "Search issues by text content",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "repo_name": {"type": "string", "description": "Optional repository filter"},
                "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100}
            },
            "required": ["query"]
        }
    }
]