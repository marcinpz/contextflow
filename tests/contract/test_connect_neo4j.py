"""Contract test for connect_to_neo4j function."""

import pytest
from src.neo4j_integration.client import connect_to_neo4j, Neo4jClient


@pytest.mark.contract
def test_connect_to_neo4j_contract():
    """Test that connect_to_neo4j function has correct contract."""
    # Function should exist and be callable
    assert callable(connect_to_neo4j)

    # Function should return a Neo4jClient instance
    result = connect_to_neo4j(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    assert isinstance(result, Neo4jClient)