# Neo4j schema definitions for C4 modeling

from src.neo4j_integration.client import Neo4jClient


def create_schema(client: Neo4jClient) -> None:
    """Create C4 modeling schema in Neo4j.

    Creates constraints, indexes, and relationships for Context, Container, Component, Code entities.
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


def create_c4_relationships(client: Neo4jClient) -> None:
    """Create C4 hierarchical relationships in Neo4j.

    Links Containers to Contexts, Components to Containers, Code to Components.
    """
    # Create BELONGS_TO relationships based on name references
    relationship_queries = [
        # Container -> Context relationships
        """
        MATCH (c:Container), (ctx:Context)
        WHERE c.context_name = ctx.name
        AND NOT (c)-[:BELONGS_TO]->(ctx)
        CREATE (c)-[:BELONGS_TO]->(ctx)
        """,
        # Component -> Container relationships
        """
        MATCH (comp:Component), (cont:Container)
        WHERE comp.container_name = cont.name
        AND NOT (comp)-[:BELONGS_TO]->(cont)
        CREATE (comp)-[:BELONGS_TO]->(cont)
        """,
        # Code -> Component relationships
        """
        MATCH (code:Code), (comp:Component)
        WHERE code.component_name = comp.name
        AND NOT (code)-[:BELONGS_TO]->(comp)
        CREATE (code)-[:BELONGS_TO]->(comp)
        """
    ]

    for query in relationship_queries:
        client.run_query(query)


def create_c4_diagram_data(client: Neo4jClient) -> dict:
    """Generate C4 diagram data from Neo4j database."""
    # Query all C4 elements and relationships
    queries = {
        "contexts": "MATCH (c:Context) RETURN c.name, c.description, c.technology",
        "containers": "MATCH (c:Container) RETURN c.name, c.description, c.technology, c.context_name",
        "components": "MATCH (c:Component) RETURN c.name, c.description, c.technology, c.container_name",
        "code": "MATCH (c:Code) RETURN c.name, c.description, c.technology, c.component_name",
        "relationships": """
        MATCH (source)-[r]->(target)
        WHERE type(r) IN ['USES', 'STORES', 'COMMUNICATES_WITH', 'DEPENDS_ON']
        RETURN labels(source)[0] as source_type, source.name as source_name,
               labels(target)[0] as target_type, target.name as target_name,
               r.description, r.technology, type(r) as interaction_type
        """
    }

    result = {}
    for key, query in queries.items():
        result[key] = client.run_query(query)

    return result