# Neo4j schema definitions for C4 modeling

from src.neo4j_integration.client import Neo4jClient


def create_schema(client: Neo4jClient) -> None:
    """Create C4 modeling schema in Neo4j.

    Creates constraints and indexes for Context, Container, Component, Code entities.
    """
    # Create constraints for unique names
    constraints = [
        "CREATE CONSTRAINT context_name_unique IF NOT EXISTS FOR (c:Context) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT container_name_unique IF NOT EXISTS FOR (c:Container) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT component_name_unique IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT code_name_unique IF NOT EXISTS FOR (c:Code) REQUIRE c.name IS UNIQUE",
    ]

    for constraint in constraints:
        client.run_query(constraint)

    # Create indexes for performance
    indexes = [
        "CREATE INDEX context_description IF NOT EXISTS FOR (c:Context) ON (c.description)",
        "CREATE INDEX container_description IF NOT EXISTS FOR (c:Container) ON (c.description)",
        "CREATE INDEX component_description IF NOT EXISTS FOR (c:Component) ON (c.description)",
        "CREATE INDEX code_description IF NOT EXISTS FOR (c:Code) ON (c.description)",
    ]

    for index in indexes:
        client.run_query(index)