# GitHub Copilot Instructions for ContextFlow

## Project Context
This is a local knowledge system MVP integrating Neo4j, Qdrant, and MCP server.

## Coding Standards
- Use Python 3.11+
- Follow MCP protocol patterns from OpenAI SDK
- Implement proper error handling for database connections
- Use type hints consistently
- Design for local-first operation

## Architecture Patterns
- MCP tools should be atomic and well-documented
- Use dependency injection for database connections
- Implement proper logging throughout
- Follow Neo4j best practices for graph queries