"""Unit tests for code indexer."""

import pytest
import tempfile
import os
from src.code_indexer.indexer import CodeIndexer


def test_code_indexer_initialization():
    """Test that CodeIndexer initializes correctly."""
    indexer = CodeIndexer()
    assert indexer.parsers is not None
    # Parsers may not be available if tree-sitter setup fails
    # The indexer should still work with fallback


def test_index_python_file():
    """Test indexing a Python file."""
    indexer = CodeIndexer()

    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
class TestClass:
    def __init__(self):
        pass

    def test_method(self):
        return "test"

def standalone_function():
    return True
""")
        temp_file = f.name

    try:
        result = indexer.index_file(temp_file)
        assert result is not None
        assert result['language'] == 'python'
        assert result['file_path'] == temp_file

        entities = result['entities']
        assert len(entities) >= 2  # At least class and function

        # Check for TestClass
        class_entity = next((e for e in entities if e['name'] == 'TestClass'), None)
        assert class_entity is not None
        assert class_entity['type'] == 'class'

        # Check for standalone_function
        func_entity = next((e for e in entities if e['name'] == 'standalone_function'), None)
        assert func_entity is not None
        assert func_entity['type'] == 'function'

    finally:
        os.unlink(temp_file)


def test_index_unsupported_file():
    """Test indexing an unsupported file type."""
    indexer = CodeIndexer()

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is just text")
        temp_file = f.name

    try:
        result = indexer.index_file(temp_file)
        assert result is None
    finally:
        os.unlink(temp_file)


def test_index_directory():
    """Test indexing a directory."""
    indexer = CodeIndexer()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a Python file
        py_file = os.path.join(temp_dir, 'test.py')
        with open(py_file, 'w') as f:
            f.write("def hello():\n    return 'world'")

        # Create a text file (should be ignored)
        txt_file = os.path.join(temp_dir, 'test.txt')
        with open(txt_file, 'w') as f:
            f.write("ignore me")

        results = indexer.index_directory(temp_dir)
        assert len(results) == 1
        assert results[0]['language'] == 'python'