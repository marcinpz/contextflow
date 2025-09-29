# Neo4j models for C4 architecture entities

from typing import Optional, List
from pydantic import BaseModel


class Context(BaseModel):
    """C4 Context entity - represents the system boundary."""
    name: str
    description: Optional[str] = None
    technology: Optional[str] = None  # e.g., "Web Application", "Mobile App"


class Container(BaseModel):
    """C4 Container entity - represents applications or data stores."""
    name: str
    description: Optional[str] = None
    technology: Optional[str] = None  # e.g., "Spring Boot Application", "PostgreSQL Database"
    context_name: str  # Reference to parent Context


class Component(BaseModel):
    """C4 Component entity - represents logical components within containers."""
    name: str
    description: Optional[str] = None
    technology: Optional[str] = None  # e.g., "REST API", "Message Queue"
    container_name: str  # Reference to parent Container


class Code(BaseModel):
    """C4 Code entity - represents implementation details."""
    name: str
    description: Optional[str] = None
    technology: Optional[str] = None  # e.g., "Java Class", "Python Module"
    component_name: str  # Reference to parent Component


class C4Relationship(BaseModel):
    """Represents relationships between C4 elements."""
    source_type: str  # "Context", "Container", "Component", "Code"
    source_name: str
    target_type: str
    target_name: str
    description: Optional[str] = None
    technology: Optional[str] = None  # e.g., "HTTP", "JDBC", "REST API"
    interaction_type: Optional[str] = None  # e.g., "Uses", "Stores", "Sends"


class C4Diagram(BaseModel):
    """Complete C4 diagram representation."""
    contexts: List[Context] = []
    containers: List[Container] = []
    components: List[Component] = []
    code_elements: List[Code] = []
    relationships: List[C4Relationship] = []