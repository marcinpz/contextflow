# Examples Directory

This directory contains example implementations and test files for ContextFlow.

## Files

### Code Examples
- `tree_sitter_parser.py` - Tree-sitter based code parser for Java and YAML files
- `mcp_code_analyzer.py` - MCP server implementation providing AI context tools

### Test Data
- `UserService.java` - Sample Spring service with dependency injections and property usage
- `application.yml` - Sample Spring Boot configuration with nested properties

## Purpose

These examples demonstrate:
1. How to use Tree-sitter for accurate code parsing
2. How to implement MCP tools for AI context enhancement
3. Real-world code patterns that ContextFlow should analyze
4. Integration between code parsing and MCP server functionality

## Usage

```bash
# Test the parser
python tree_sitter_parser.py

# Test MCP server (requires MCP client)
python mcp_code_analyzer.py
```

## Testing

See `../TESTING.md` for comprehensive testing procedures using these examples.