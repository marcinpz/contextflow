# Neo4j client for graph operations

from neo4j import GraphDatabase, Query
from typing import Optional


class Neo4jClient:
    """Client for Neo4j graph database operations."""

    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the database connection."""
        self._driver.close()

    def run_query(self, query: str, parameters: Optional[dict] = None):
        """Run a Cypher query."""
        with self._driver.session() as session:
            return session.run(Query(query), parameters or {})


def connect_to_neo4j(uri: str = "bolt://localhost:7687",
                    user: str = "neo4j",
                    password: str = "password") -> Neo4jClient:
    """Connect to Neo4j database.

    Args:
        uri: Neo4j connection URI
        user: Neo4j username
        password: Neo4j password

    Returns:
        Connected Neo4jClient instance
    """
    return Neo4jClient(uri, user, password)