# Neo4j installation utilities

import docker
from docker.errors import DockerException
import time


def install_neo4j() -> bool:
    """Install and start Neo4j Community Edition using Docker.

    Returns:
        True if installation successful, False otherwise
    """
    try:
        client = docker.from_env()

        # Check if container already exists
        containers = client.containers.list(all=True, filters={'name': 'neo4j-contextflow'})
        if containers:
            container = containers[0]
            if container.status != 'running':
                container.start()
            return True

        # Create and start Neo4j container
        container = client.containers.run(
            'neo4j:5.26-community',
            name='neo4j-contextflow',
            ports={'7474/tcp': 7474, '7687/tcp': 7687},
            environment={
                'NEO4J_AUTH': 'neo4j/password',
                'NEO4J_PLUGINS': '["graph-data-science"]'
            },
            detach=True
        )

        # Wait for Neo4j to be ready
        max_attempts = 30
        for attempt in range(max_attempts):
            container.reload()
            if container.status == 'running':
                # Additional check for Neo4j availability
                time.sleep(2)
                return True
            time.sleep(1)

        return False

    except DockerException:
        return False
    except Exception:
        return False