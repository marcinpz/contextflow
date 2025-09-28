# ContextFlow Agent Instructions

## Build/Lint/Test Commands
- **Install**: `uv pip install -e .` (when code exists)
- **Lint**: `ruff check .` (when code exists)
- **Type Check**: `mypy .` (when code exists)
- **Test**: `pytest` (when code exists)
- **Single Test**: `pytest tests/test_file.py::TestClass::test_method`

## Code Style Guidelines
- **Python**: 3.11+, type hints required, follow MCP protocol patterns
- **Imports**: Standard library first, then third-party, then local
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Error Handling**: Use try/except with specific exceptions, log errors
- **Formatting**: 4 spaces indentation, 88 char line length
- **Documentation**: Docstrings for public functions, type hints for parameters

## MCP Tools for Development
- **Issue Generation**: Use MCP GitHub tools to create issues from requirements
- **Task Planning**: Generate structured task lists and break down complex features
- **Work Tracking**: Create milestones and track progress across development phases
- **Code Review**: Use MCP for automated code analysis and review comments

## Testing Guidelines
- **Performance Testing**: Compare AI agent effectiveness with/without ContextFlow MCP tools
- **Accuracy Validation**: Verify dependency detection completeness and correctness
- **Integration Testing**: Ensure MCP tools work with Claude Desktop, Cursor, and other clients
- **Metrics Tracking**: Use TESTING.md for detailed testing procedures and expected improvements

## Architecture Patterns
- MCP tools must be atomic and well-documented
- Use dependency injection for database connections
- Implement proper logging throughout the application
- Follow Neo4j best practices for graph queries
