"""Contract test for install_neo4j function."""

import pytest
from src.neo4j_integration.install import install_neo4j


@pytest.mark.contract
def test_install_neo4j_contract():
    """Test that install_neo4j function has correct contract."""
    # Function should exist and be callable
    assert callable(install_neo4j)

    # Function should return a boolean
    result = install_neo4j()
    assert isinstance(result, bool)