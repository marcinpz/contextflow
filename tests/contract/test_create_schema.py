"""Contract test for create_schema function."""

import pytest
from unittest.mock import Mock
from src.neo4j_integration.schema import create_schema
from src.neo4j_integration.client import Neo4jClient


@pytest.mark.contract
def test_create_schema_contract():
    """Test that create_schema function has correct contract."""
    # Function should exist and be callable
    assert callable(create_schema)

    # Mock client for testing contract
    mock_client = Mock(spec=Neo4jClient)

    # Function should accept client parameter and return None
    result = create_schema(mock_client)
    assert result is None

    # Verify that run_query was called (schema creation queries)
    assert mock_client.run_query.called