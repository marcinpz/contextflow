"""
MCP Server for ContextFlow.

Provides AI assistants with tools to query knowledge graphs and search code.
"""

from mcp.server import Server
from typing import List, Dict, Any
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from neo4j_integration.client import connect_to_neo4j, Neo4jClient
from src.mcp.tools.github_tools import GitHubTools

server = Server("contextflow-mcp")

class ContextFlowTools:
    """ContextFlow MCP tools."""

    def __init__(self):
        self.neo4j_client: Neo4jClient = None
        self.github_tools: GitHubTools = None

    def initialize(self):
        """Initialize connections to backend services."""
        try:
            self.neo4j_client = connect_to_neo4j()
            self.github_tools = GitHubTools()
        except Exception as e:
            print(f"Failed to initialize ContextFlow tools: {e}")
            self.neo4j_client = None
            self.github_tools = None

# Global instance
tools = ContextFlowTools()

@server.tool()
def query_graph(cypher_query: str) -> str:
    """
    Execute a Cypher query against the Neo4j knowledge graph.

    Args:
        cypher_query: Cypher query to execute

    Returns:
        Query results as formatted string
    """
    if not tools.neo4j_client:
        return "Error: Neo4j client not initialized"

    try:
        result = tools.neo4j_client.run_query(cypher_query)
        records = list(result)

        if not records:
            return "No results found"

        # Format results
        output = f"Query executed successfully. Found {len(records)} records:\n\n"

        for i, record in enumerate(records[:10]):  # Limit to first 10
            output += f"Record {i+1}:\n"
            for key, value in record.items():
                output += f"  {key}: {value}\n"
            output += "\n"

        if len(records) > 10:
            output += f"... and {len(records) - 10} more records\n"

        return output

    except Exception as e:
        return f"Error executing query: {str(e)}"

@server.tool()
def find_repo_issues(repo_name: str, state: str = "all", limit: int = 10) -> str:
    """
    Find issues in a GitHub repository.

    Args:
        repo_name: Repository full name (owner/repo)
        state: Issue state ("open", "closed", "all")
        limit: Maximum issues to return

    Returns:
        Formatted list of issues
    """
    if not tools.github_tools:
        return "Error: GitHub tools not initialized"

    try:
        result = tools.github_tools.find_issues_by_repo(repo_name, state, limit)

        if not result.get("issues"):
            return f"No issues found for repository '{repo_name}'"

        output = f"Found {len(result['issues'])} issues in repository '{repo_name}':\n\n"

        for issue in result["issues"]:
            output += f"#{issue['number']} - {issue['title']}\n"
            output += f"  State: {issue['state']}\n"
            if issue.get('labels'):
                output += f"  Labels: {', '.join(issue['labels'])}\n"
            output += "\n"

        return output

    except Exception as e:
        return f"Error finding repository issues: {str(e)}"

@server.tool()
def search_code_context(search_term: str, file_types: List[str] = None) -> str:
    """
    Search for code context and dependencies.

    Args:
        search_term: Term to search for (class name, function, etc.)
        file_types: File extensions to search in (optional)

    Returns:
        Code search results
    """
    # Placeholder for code search using Tree-sitter
    # This would integrate with the code indexing from Phase 1
    return f"Code search for '{search_term}' not yet implemented. Coming in Tree-sitter integration."

if __name__ == "__main__":
    print("🚀 Starting ContextFlow MCP Server...")
    tools.initialize()

    print("Available tools:")
    print("- query_graph: Execute Cypher queries against Neo4j")
    print("- find_repo_issues: Find GitHub issues by repository")
    print("- search_code_context: Search code using Tree-sitter")

    server.run()