"""Integration test for C4 schema creation."""

import pytest
from src.neo4j_integration.client import connect_to_neo4j
from src.neo4j_integration.schema import create_schema


@pytest.mark.integration
def test_c4_schema_creation():
    """Test that C4 schema can be created in Neo4j."""
    # Connect to Neo4j
    client = connect_to_neo4j(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    # Create schema
    create_schema(client)

    # Verify schema exists by querying
    # This would check that Context, Container, Component, Code labels exist
    # and relationships are defined
    # For now, just ensure no exceptions
    pass