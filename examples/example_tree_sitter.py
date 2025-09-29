#!/usr/bin/env python3
"""
Przykład użycia Tree-sitter do parsowania Java i ekstrakcji zależności
"""

from tree_sitter import Parser
import tree_sitter_java as ts_java
import tree_sitter_yaml as ts_yaml

class CodeParser:
    def __init__(self):
        # Inicjalizacja parserów
        self.java_parser = Parser()
        self.java_parser.set_language(ts_java.language())

        self.yaml_parser = Parser()
        self.yaml_parser.set_language(ts_yaml.language())

    def parse_java_file(self, file_path: str) -> dict:
        """Parsuje plik Java i wyciąga informacje o zależnościach"""
        with open(file_path, 'r') as f:
            code = f.read()

        tree = self.java_parser.parse(bytes(code, 'utf8'))

        dependencies = {
            'imports': [],
            'annotations': [],
            'field_injections': [],
            'method_calls': []
        }

        def traverse_tree(node):
            if node.type == 'import_declaration':
                # @import java.util.List;
                import_text = code[node.start_byte:node.end_byte].strip()
                dependencies['imports'].append(import_text)

            elif node.type == 'annotation':
                # @Value("${app.config.path}")
                annotation_text = code[node.start_byte:node.end_byte].strip()
                dependencies['annotations'].append(annotation_text)

            elif node.type == 'field_declaration':
                # private @Autowired UserService userService;
                field_text = code[node.start_byte:node.end_byte].strip()
                if '@Autowired' in field_text or '@Inject' in field_text:
                    dependencies['field_injections'].append(field_text)

            # Rekursywnie przeszukaj dzieci
            for child in node.children:
                traverse_tree(child)

        traverse_tree(tree.root_node)
        return dependencies

    def parse_yaml_file(self, file_path: str) -> dict:
        """Parsuje plik YAML i wyciąga property definitions"""
        with open(file_path, 'r') as f:
            content = f.read()

        tree = self.yaml_parser.parse(bytes(content, 'utf8'))

        properties = {}

        def traverse_yaml(node, path=""):
            if node.type == 'block_mapping_pair':
                # key: value
                key_node = node.children[0]
                value_node = node.children[1] if len(node.children) > 1 else None

                if key_node.type == 'flow_node':
                    key = content[key_node.start_byte:key_node.end_byte].strip()
                    current_path = f"{path}.{key}" if path else key

                    if value_node and value_node.type == 'flow_node':
                        value = content[value_node.start_byte:value_node.end_byte].strip()
                        properties[current_path] = value

                # Rekursywnie dla nested properties
                for child in node.children:
                    traverse_yaml(child, path)

        traverse_yaml(tree.root_node)
        return properties

# Przykład użycia
if __name__ == "__main__":
    parser = CodeParser()

    # Przykład parsowania Java
    java_deps = parser.parse_java_file("example.java")
    print("Java dependencies:", java_deps)

    # Przykład parsowania YAML
    yaml_props = parser.parse_yaml_file("application.yml")
    print("YAML properties:", yaml_props)