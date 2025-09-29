# Code indexer using Tree-sitter for parsing source code

from typing import Dict, List, Any, Optional
import os
import re

try:
    from tree_sitter import Parser
    import tree_sitter_python as ts_python
    import tree_sitter_javascript as ts_javascript
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    print("Warning: Tree-sitter not available, using fallback parsing")


class CodeIndexer:
    """Indexes source code to extract classes, functions, and modules."""

    def __init__(self):
        self.parsers = {}
        if TREE_SITTER_AVAILABLE:
            self._setup_parsers()
        else:
            print("Using regex-based fallback for code indexing")

    def _setup_parsers(self):
        """Initialize Tree-sitter parsers for supported languages."""
        try:
            self.parsers['python'] = Parser(ts_python.language())
        except Exception as e:
            print(f"Warning: Python parser not available: {e}")

        try:
            self.parsers['javascript'] = Parser(ts_javascript.language())
        except Exception as e:
            print(f"Warning: JavaScript parser not available: {e}")

    def index_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Index a single file and extract code entities.

        Args:
            file_path: Path to the file to index

        Returns:
            Dictionary with extracted entities or None if unsupported
        """
        if not os.path.exists(file_path):
            return None

        ext = os.path.splitext(file_path)[1].lower()
        language = self._get_language_from_extension(ext)

        if not language:
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            if TREE_SITTER_AVAILABLE and language in self.parsers:
                # Use Tree-sitter parsing
                tree = self.parsers[language].parse(bytes(code, 'utf8'))
                entities = self._extract_entities(tree, code, language)
            else:
                # Use regex fallback
                entities = self._extract_entities_fallback(code, language)

            return {
                'file_path': file_path,
                'language': language,
                'entities': entities
            }
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return None

    def _get_language_from_extension(self, ext: str) -> Optional[str]:
        """Map file extension to language."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'javascript',  # TypeScript treated as JavaScript for now
        }
        return ext_map.get(ext)

    def _extract_entities(self, tree, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract code entities from the parse tree."""
        entities = []

        def traverse(node, parent=None):
            if language == 'python':
                entities.extend(self._extract_python_entities(node, code, parent))
            elif language == 'javascript':
                entities.extend(self._extract_javascript_entities(node, code, parent))

            for child in node.children:
                traverse(child, node)

        traverse(tree.root_node)
        return entities

    def _extract_python_entities(self, node, code: str, parent) -> List[Dict[str, Any]]:
        """Extract Python-specific entities."""
        entities = []

        if node.type == 'class_definition':
            # Extract class name
            class_name = None
            for child in node.children:
                if child.type == 'identifier':
                    class_name = code[child.start_byte:child.end_byte]
                    break

            if class_name:
                entities.append({
                    'type': 'class',
                    'name': class_name,
                    'start_line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1,
                })

        elif node.type == 'function_definition':
            # Extract function name
            func_name = None
            for child in node.children:
                if child.type == 'identifier':
                    func_name = code[child.start_byte:child.end_byte]
                    break

            if func_name:
                entities.append({
                    'type': 'function',
                    'name': func_name,
                    'start_line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1,
                })

        return entities

    def _extract_javascript_entities(self, node, code: str, parent) -> List[Dict[str, Any]]:
        """Extract JavaScript-specific entities."""
        entities = []

        if node.type == 'class_declaration':
            # Extract class name
            class_name = None
            for child in node.children:
                if child.type == 'identifier':
                    class_name = code[child.start_byte:child.end_byte]
                    break

            if class_name:
                entities.append({
                    'type': 'class',
                    'name': class_name,
                    'start_line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1,
                })

        elif node.type == 'function_declaration':
            # Extract function name
            func_name = None
            for child in node.children:
                if child.type == 'identifier':
                    func_name = code[child.start_byte:child.end_byte]
                    break

            if func_name:
                entities.append({
                    'type': 'function',
                    'name': func_name,
                    'start_line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1,
                })

        return entities

    def _extract_entities_fallback(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract entities using regex patterns as fallback."""
        entities = []

        if language == 'python':
            # Simple regex patterns for Python
            # Class definitions
            class_pattern = r'^class\s+(\w+)'
            for match in re.finditer(class_pattern, code, re.MULTILINE):
                line_num = code[:match.start()].count('\n') + 1
                entities.append({
                    'type': 'class',
                    'name': match.group(1),
                    'start_line': line_num,
                    'end_line': line_num
                })

            # Function definitions
            func_pattern = r'^def\s+(\w+)'
            for match in re.finditer(func_pattern, code, re.MULTILINE):
                line_num = code[:match.start()].count('\n') + 1
                entities.append({
                    'type': 'function',
                    'name': match.group(1),
                    'start_line': line_num,
                    'end_line': line_num
                })

        elif language == 'javascript':
            # Simple patterns for JavaScript
            class_pattern = r'^class\s+(\w+)'
            for match in re.finditer(class_pattern, code, re.MULTILINE):
                line_num = code[:match.start()].count('\n') + 1
                entities.append({
                    'type': 'class',
                    'name': match.group(1),
                    'start_line': line_num,
                    'end_line': line_num
                })

            func_pattern = r'^function\s+(\w+)|\bconst\s+(\w+)\s*=\s*\('
            for match in re.finditer(func_pattern, code, re.MULTILINE):
                func_name = match.group(1) or match.group(2)
                if func_name:
                    line_num = code[:match.start()].count('\n') + 1
                    entities.append({
                        'type': 'function',
                        'name': func_name,
                        'start_line': line_num,
                        'end_line': line_num
                    })

        return entities

    def index_directory(self, directory: str, extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Index all files in a directory.

        Args:
            directory: Directory path to index
            extensions: List of file extensions to include (optional)

        Returns:
            List of indexed files with their entities
        """
        if extensions is None:
            extensions = ['.py', '.js', '.ts']

        indexed_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    result = self.index_file(file_path)
                    if result:
                        indexed_files.append(result)

        return indexed_files