# C4 diagram generation for ContextFlow

from typing import Dict, List, Any
from .client import Neo4jClient


class C4DiagramGenerator:
    """Generate C4 architecture diagrams from Neo4j data."""

    def __init__(self, client: Neo4jClient):
        self.client = client

    def generate_context_diagram(self) -> str:
        """Generate C4 Context level diagram in Mermaid format."""
        query = """
        MATCH (c:Context)
        OPTIONAL MATCH (c)-[:BELONGS_TO*]->(containers:Container)
        RETURN c.name as context_name, c.description as context_desc,
               collect(DISTINCT containers.name) as container_names
        """

        results = self.client.run_query(query)

        mermaid = ["graph TB"]
        mermaid.append("    %% C4 Context Diagram")

        for record in results:
            context_name = record["context_name"]
            context_desc = record.get("context_desc", "")
            containers = record.get("container_names", [])

            # Add context node
            mermaid.append(f'    {context_name}["{context_name}"]')

            # Add container relationships
            for container in containers:
                if container:
                    mermaid.append(f'    {container} --> {context_name}')

        return "\n".join(mermaid)

    def generate_container_diagram(self, context_name: str = None) -> str:
        """Generate C4 Container level diagram."""
        if context_name:
            query = """
            MATCH (ctx:Context {name: $context_name})
            MATCH (c:Container)-[:BELONGS_TO]->(ctx)
            OPTIONAL MATCH (c)<-[:BELONGS_TO]-(comp:Component)
            RETURN c.name as container_name, c.description as container_desc,
                   c.technology as tech, collect(DISTINCT comp.name) as components
            """
            params = {"context_name": context_name}
        else:
            query = """
            MATCH (c:Container)
            OPTIONAL MATCH (c)<-[:BELONGS_TO]-(comp:Component)
            RETURN c.name as container_name, c.description as container_desc,
                   c.technology as tech, collect(DISTINCT comp.name) as components
            """
            params = {}

        results = self.client.run_query(query, params)

        mermaid = ["graph TB"]
        mermaid.append("    %% C4 Container Diagram")

        for record in results:
            container_name = record["container_name"]
            container_desc = record.get("container_desc", "")
            tech = record.get("tech", "")
            components = record.get("components", [])

            # Format: [Container: Technology]
            label = f"{container_name}"
            if tech:
                label += f": {tech}"

            mermaid.append(f'    {container_name}["{label}"]')

            # Add component relationships
            for component in components:
                if component:
                    mermaid.append(f'    {component} --> {container_name}')

        return "\n".join(mermaid)

    def generate_component_diagram(self, container_name: str = None) -> str:
        """Generate C4 Component level diagram."""
        if container_name:
            query = """
            MATCH (cont:Container {name: $container_name})
            MATCH (c:Component)-[:BELONGS_TO]->(cont)
            OPTIONAL MATCH (c)<-[:BELONGS_TO]-(code:Code)
            RETURN c.name as component_name, c.description as component_desc,
                   c.technology as tech, collect(DISTINCT code.name) as code_elements
            """
            params = {"container_name": container_name}
        else:
            query = """
            MATCH (c:Component)
            OPTIONAL MATCH (c)<-[:BELONGS_TO]-(code:Code)
            RETURN c.name as component_name, c.description as component_desc,
                   c.technology as tech, collect(DISTINCT code.name) as code_elements
            """
            params = {}

        results = self.client.run_query(query, params)

        mermaid = ["graph TB"]
        mermaid.append("    %% C4 Component Diagram")

        for record in results:
            component_name = record["component_name"]
            component_desc = record.get("component_desc", "")
            tech = record.get("tech", "")
            code_elements = record.get("code_elements", [])

            label = f"{component_name}"
            if tech:
                label += f": {tech}"

            mermaid.append(f'    {component_name}["{label}"]')

            # Add code relationships
            for code in code_elements:
                if code:
                    mermaid.append(f'    {code} --> {component_name}')

        return "\n".join(mermaid)

    def generate_relationship_diagram(self) -> str:
        """Generate diagram showing relationships between C4 elements."""
        query = """
        MATCH (source)-[r]->(target)
        WHERE type(r) IN ['USES', 'STORES', 'COMMUNICATES_WITH', 'DEPENDS_ON']
        RETURN labels(source)[0] as source_type, source.name as source_name,
               labels(target)[0] as target_type, target.name as target_name,
               type(r) as relationship_type, r.description as desc
        """

        results = self.client.run_query(query)

        mermaid = ["graph TD"]
        mermaid.append("    %% C4 Relationships Diagram")

        # Track nodes to avoid duplicates
        nodes = set()

        for record in results:
            source_name = record["source_name"]
            target_name = record["target_name"]
            rel_type = record["relationship_type"]
            desc = record.get("desc", "")

            # Add nodes if not already added
            if source_name not in nodes:
                mermaid.append(f'    {source_name}["{source_name}"]')
                nodes.add(source_name)

            if target_name not in nodes:
                mermaid.append(f'    {target_name}["{target_name}"]')
                nodes.add(target_name)

            # Add relationship
            label = rel_type
            if desc:
                label += f": {desc}"

            mermaid.append(f'    {source_name} -->|{label}| {target_name}')

        return "\n".join(mermaid)</content>
</xai:function_call name="write">
<parameter name="filePath">src/neo4j_integration/c4_builder.py