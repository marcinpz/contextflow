#!/usr/bin/env python3
"""
MCP Server używający Tree-sitter do analizy kodu i dostarczania kontekstu AI
"""

from mcp import Tool
from mcp.server import Server
import os
from typing import List, Dict, Any

# Import naszego parsera
from example_tree_sitter import CodeParser

server = Server("code-context-analyzer")

class CodeContextManager:
    def __init__(self):
        self.parser = CodeParser()
        self.cache = {}  # Cache dla parsed files

    def find_property_usage(self, property_name: str, search_paths: List[str]) -> List[Dict]:
        """Znajdź wszystkie użycia danej property w kodzie"""
        results = []

        for path in search_paths:
            if os.path.isfile(path) and path.endswith('.java'):
                if path not in self.cache:
                    self.cache[path] = self.parser.parse_java_file(path)

                deps = self.cache[path]

                # Szukaj w annotations
                for annotation in deps['annotations']:
                    if property_name in annotation:
                        results.append({
                            'file': path,
                            'type': 'annotation',
                            'content': annotation,
                            'line': self._estimate_line_number(path, annotation)
                        })

        return results

    def find_class_dependencies(self, class_name: str, search_paths: List[str]) -> List[Dict]:
        """Znajdź wszystkie zależności danej klasy"""
        results = []

        for path in search_paths:
            if os.path.isfile(path) and path.endswith('.java'):
                if path not in self.cache:
                    self.cache[path] = self.parser.parse_java_file(path)

                deps = self.cache[path]

                # Szukaj w imports
                for import_stmt in deps['imports']:
                    if class_name in import_stmt:
                        results.append({
                            'file': path,
                            'type': 'import',
                            'content': import_stmt,
                            'line': self._estimate_line_number(path, import_stmt)
                        })

                # Szukaj w field injections
                for field in deps['field_injections']:
                    if class_name in field:
                        results.append({
                            'file': path,
                            'type': 'field_injection',
                            'content': field,
                            'line': self._estimate_line_number(path, field)
                        })

        return results

    def _estimate_line_number(self, file_path: str, text: str) -> int:
        """Szacuje numer linii dla danego tekstu (uproszczona wersja)"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    if text.strip() in line.strip():
                        return i
        except:
            pass
        return 0

# Globalna instancja
context_manager = CodeContextManager()

@server.tool()
def find_property_usage(property_name: str, search_paths: List[str]) -> str:
    """
    Znajdź wszystkie miejsca w kodzie gdzie używana jest dana property

    Args:
        property_name: Nazwa property (np. "app.database.url")
        search_paths: Lista ścieżek do przeszukania

    Returns:
        Lista plików i linii gdzie property jest używana
    """
    results = context_manager.find_property_usage(property_name, search_paths)

    if not results:
        return f"Nie znaleziono użycia property '{property_name}' w podanych ścieżkach"

    output = f"Znaleziono {len(results)} użyć property '{property_name}':\n\n"
    for result in results:
        output += f"📁 {result['file']}:{result['line']}\n"
        output += f"   {result['type']}: {result['content']}\n\n"

    return output

@server.tool()
def find_class_dependencies(class_name: str, search_paths: List[str]) -> str:
    """
    Znajdź wszystkie zależności danej klasy w kodzie

    Args:
        class_name: Nazwa klasy (np. "UserService")
        search_paths: Lista ścieżek do przeszukania

    Returns:
        Lista plików gdzie klasa jest używana
    """
    results = context_manager.find_class_dependencies(class_name, search_paths)

    if not results:
        return f"Nie znaleziono zależności klasy '{class_name}' w podanych ścieżkach"

    output = f"Znaleziono {len(results)} zależności klasy '{class_name}':\n\n"
    for result in results:
        output += f"📁 {result['file']}:{result['line']}\n"
        output += f"   {result['type']}: {result['content']}\n\n"

    return output

@server.tool()
def analyze_file_context(file_path: str) -> str:
    """
    Przeanalizuj plik i wyciągnij wszystkie zależności i kontekst

    Args:
        file_path: Ścieżka do pliku do analizy

    Returns:
        Szczegółowa analiza zależności w pliku
    """
    if not os.path.exists(file_path):
        return f"Plik {file_path} nie istnieje"

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.java':
        deps = context_manager.parser.parse_java_file(file_path)

        output = f"📄 Analiza pliku {file_path}:\n\n"
        output += f"📦 Imports: {len(deps['imports'])}\n"
        for imp in deps['imports'][:5]:  # Pierwsze 5
            output += f"   • {imp}\n"
        if len(deps['imports']) > 5:
            output += f"   ... i {len(deps['imports']) - 5} więcej\n\n"

        output += f"🏷️  Annotations: {len(deps['annotations'])}\n"
        for ann in deps['annotations'][:3]:
            output += f"   • {ann}\n"
        if len(deps['annotations']) > 3:
            output += f"   ... i {len(deps['annotations']) - 3} więcej\n\n"

        output += f"💉 Field Injections: {len(deps['field_injections'])}\n"
        for field in deps['field_injections']:
            output += f"   • {field}\n"

        return output

    elif ext in ['.yml', '.yaml']:
        props = context_manager.parser.parse_yaml_file(file_path)

        output = f"📄 Analiza pliku {file_path}:\n\n"
        output += f"⚙️  Properties: {len(props)}\n"
        for key, value in list(props.items())[:10]:  # Pierwsze 10
            output += f"   • {key}: {value}\n"
        if len(props) > 10:
            output += f"   ... i {len(props) - 10} więcej\n"

        return output

    else:
        return f"Nieobsługiwany typ pliku: {ext}"

if __name__ == "__main__":
    print("🚀 Uruchamianie MCP Code Context Analyzer...")
    print("Dostępne narzędzia:")
    print("- find_property_usage")
    print("- find_class_dependencies")
    print("- analyze_file_context")
    print("\nAby przetestować: python -m mcp.client")

    server.run()