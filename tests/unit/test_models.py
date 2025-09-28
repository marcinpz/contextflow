"""Unit tests for Neo4j models."""

import pytest
from src.neo4j_integration.models import Context, Container, Component, Code


def test_context_model():
    """Test Context model creation and validation."""
    context = Context(name="Test Context", description="A test context")
    assert context.name == "Test Context"
    assert context.description == "A test context"

    # Test without description
    context2 = Context(name="Test Context 2")
    assert context2.name == "Test Context 2"
    assert context2.description is None


def test_container_model():
    """Test Container model creation and validation."""
    container = Container(
        name="Test Container",
        description="A test container",
        context_name="Test Context"
    )
    assert container.name == "Test Container"
    assert container.description == "A test container"
    assert container.context_name == "Test Context"


def test_component_model():
    """Test Component model creation and validation."""
    component = Component(
        name="Test Component",
        description="A test component",
        container_name="Test Container"
    )
    assert component.name == "Test Component"
    assert component.description == "A test component"
    assert component.container_name == "Test Container"


def test_code_model():
    """Test Code model creation and validation."""
    code = Code(
        name="Test Code",
        description="A test code entity",
        component_name="Test Component"
    )
    assert code.name == "Test Code"
    assert code.description == "A test code entity"
    assert code.component_name == "Test Component"