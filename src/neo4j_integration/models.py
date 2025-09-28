# Neo4j models for C4 architecture entities

from typing import Optional
from pydantic import BaseModel


class Context(BaseModel):
    """C4 Context entity."""
    name: str
    description: Optional[str] = None


class Container(BaseModel):
    """C4 Container entity."""
    name: str
    description: Optional[str] = None
    context_name: str  # Reference to parent Context


class Component(BaseModel):
    """C4 Component entity."""
    name: str
    description: Optional[str] = None
    container_name: str  # Reference to parent Container


class Code(BaseModel):
    """C4 Code entity."""
    name: str
    description: Optional[str] = None
    component_name: str  # Reference to parent Component