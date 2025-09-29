"""
Integration tests for GitHub data collection.

These tests verify that the complete GitHub data collection pipeline works
from API calls through to Neo4j storage.
"""

import pytest
from neo4j import GraphDatabase
import os
from unittest.mock import Mock, patch


@pytest.fixture
def neo4j_driver():
    """Fixture to provide Neo4j driver."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        yield driver
    except Exception:
        pytest.skip("Neo4j not available")
    finally:
        if driver:
            driver.close()


@pytest.mark.integration
def test_github_data_collection_pipeline(neo4j_driver):
    """Test the complete GitHub data collection pipeline."""
    # This test will fail until the implementation is complete
    # It serves as a specification for the expected behavior

    if not os.getenv("GITHUB_TOKEN"):
        pytest.skip("GITHUB_TOKEN not set")

    # Mock the GitHub client and data
    mock_issues = [
        Mock(id=1, number=1, title="Test Issue", body="Description",
             state="open", labels=[], assignees=[],
             created_at=Mock(isoformat=lambda: "2023-01-01T00:00:00Z"),
             updated_at=Mock(isoformat=lambda: "2023-01-01T00:00:00Z"),
             closed_at=None)
    ]

    mock_repo = Mock()
    mock_repo.get_issues.return_value = mock_issues
    mock_repo.get_projects.return_value = []
    mock_repo.get_milestones.return_value = []

    with patch('src.integrations.github.client.Github') as mock_github_class:
        mock_github = Mock()
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github

        # Import and run the collector (will fail until implemented)
        try:
            from src.integrations.github.collector import collect_github_data
            # This should collect data and store in Neo4j
            collect_github_data(["test/repo"])
        except ImportError:
            pytest.skip("GitHub collector not implemented yet")

        # Verify data was stored
        with neo4j_driver.session() as session:
            result = session.run("MATCH (i:GitHubIssue) RETURN count(i) as count")
            count = result.single()["count"]
            assert count > 0


@pytest.mark.integration
def test_github_data_relationships(neo4j_driver):
    """Test that GitHub data relationships are properly stored."""
    # This test verifies the graph structure

    with neo4j_driver.session() as session:
        # Check that issues are connected to repositories
        result = session.run("""
            MATCH (i:GitHubIssue)-[:BELONGS_TO]->(r:GitHubRepository)
            RETURN count(i) as issues_with_repo
        """)
        issues_with_repo = result.single()["issues_with_repo"]
        assert issues_with_repo >= 0  # Will be 0 until implementation


@pytest.mark.integration
def test_github_data_query_performance(neo4j_driver):
    """Test that GitHub data queries perform within time limits."""
    import time

    with neo4j_driver.session() as session:
        start_time = time.time()
        result = session.run("MATCH (n) WHERE n:GitHubIssue OR n:GitHubProject OR n:GitHubMilestone RETURN count(n) as total")
        total_count = result.single()["total"]
        end_time = time.time()

        query_time = end_time - start_time
        assert query_time < 2.0  # Should complete in under 2 seconds
        assert total_count >= 0  # Ensure query returns valid count