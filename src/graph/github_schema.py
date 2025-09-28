"""
Neo4j schema definitions for GitHub data.

This module contains Cypher queries to set up constraints and indexes
for GitHub entities in the Neo4j database.
"""

from neo4j import GraphDatabase
from src.config.github_config import (
    GITHUB_LABEL_REPOSITORY,
    GITHUB_LABEL_ISSUE,
    GITHUB_LABEL_PROJECT,
    GITHUB_LABEL_MILESTONE,
)


def create_github_schema(driver):
    """Create Neo4j schema for GitHub data.

    Args:
        driver: Neo4j driver instance
    """
    with driver.session() as session:
        # Create constraints for unique IDs
        constraints = [
            f"CREATE CONSTRAINT {GITHUB_LABEL_REPOSITORY}_id IF NOT EXISTS FOR (r:{GITHUB_LABEL_REPOSITORY}) REQUIRE r.id IS UNIQUE",
            f"CREATE CONSTRAINT {GITHUB_LABEL_ISSUE}_id IF NOT EXISTS FOR (i:{GITHUB_LABEL_ISSUE}) REQUIRE i.id IS UNIQUE",
            f"CREATE CONSTRAINT {GITHUB_LABEL_PROJECT}_id IF NOT EXISTS FOR (p:{GITHUB_LABEL_PROJECT}) REQUIRE p.id IS UNIQUE",
            f"CREATE CONSTRAINT {GITHUB_LABEL_MILESTONE}_id IF NOT EXISTS FOR (m:{GITHUB_LABEL_MILESTONE}) REQUIRE m.id IS UNIQUE",
        ]

        # Create indexes for common queries
        indexes = [
            f"CREATE INDEX {GITHUB_LABEL_REPOSITORY}_full_name IF NOT EXISTS FOR (r:{GITHUB_LABEL_REPOSITORY}) ON (r.full_name)",
            f"CREATE INDEX {GITHUB_LABEL_ISSUE}_number IF NOT EXISTS FOR (i:{GITHUB_LABEL_ISSUE}) ON (i.number)",
            f"CREATE INDEX {GITHUB_LABEL_ISSUE}_state IF NOT EXISTS FOR (i:{GITHUB_LABEL_ISSUE}) ON (i.state)",
            f"CREATE INDEX {GITHUB_LABEL_PROJECT}_number IF NOT EXISTS FOR (p:{GITHUB_LABEL_PROJECT}) ON (p.number)",
            f"CREATE INDEX {GITHUB_LABEL_MILESTONE}_number IF NOT EXISTS FOR (m:{GITHUB_LABEL_MILESTONE}) ON (m.number)",
            f"CREATE INDEX {GITHUB_LABEL_MILESTONE}_state IF NOT EXISTS FOR (m:{GITHUB_LABEL_MILESTONE}) ON (m.state)",
        ]

        # Execute constraints
        for constraint in constraints:
            try:
                session.run(constraint)
            except Exception as e:
                print(f"Warning: Could not create constraint: {e}")

        # Execute indexes
        for index in indexes:
            try:
                session.run(index)
            except Exception as e:
                print(f"Warning: Could not create index: {e}")


def setup_github_schema(neo4j_uri: str = "bolt://localhost:7687",
                        neo4j_user: str = "neo4j",
                        neo4j_password: str = "password"):
    """Set up GitHub schema in Neo4j.

    Args:
        neo4j_uri: Neo4j connection URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
    """
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    try:
        create_github_schema(driver)
        print("GitHub schema setup completed")
    finally:
        driver.close()


if __name__ == "__main__":
    # Run schema setup when executed directly
    setup_github_schema()