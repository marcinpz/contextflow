# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **MCP Knowledge Index** project - a local knowledge system MVP for developers in large organizations. The system integrates code repositories, Jira tickets, documentation (Confluence, SharePoint, Teams), and architectural decision records (ADR/RFC) to provide AI assistants with comprehensive project context.

## Architecture

The system follows a multi-component architecture:

- **MCP Server**: Provides tools/interfaces for AI to query the knowledge system
- **Neo4j Graph DB**: Stores relationships between code, projects, decisions, and team structures (C4 model)
- **Vector Database (Qdrant)**: Handles document embeddings for semantic search
- **Code Index (Tree-sitter/ctags)**: Parses and indexes source code symbols and structure
- **Watchdog**: Monitors file changes for automatic index updates

## Development Commands

Since this is an early-stage project without established build tools yet, here are the expected commands based on the MVP plan:

### Setup and Dependencies
```bash
# Install Python dependencies (when requirements.txt is created)
pip install -r requirements.txt

# Or using uv (recommended for modern Python projects)
uv pip install -r requirements.txt

# Start local Neo4j instance
docker run --name neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/password neo4j

# Start Qdrant vector database
docker run -p 6333:6333 qdrant/qdrant
```

### Development Workflow
```bash
# Run the MCP server (when implemented)
python -m mcp_knowledge_index

# Test MCP tools integration
python -m pytest tests/ -v

# Index code repositories (when implemented)
python scripts/index_repo.py /path/to/repository

# Ingest Jira data (when implemented)
python scripts/jira_ingestor.py
```

### Code Quality
```bash
# Format code with ruff
ruff format .

# Lint code
ruff check .

# Type checking (if using mypy)
mypy src/
```

## Implementation Phases

**Phase 1** (Current): Core MCP server + Neo4j integration + Tree-sitter code indexing
**Phase 2**: Vector DB integration for document search and best practices recommendations  
**Phase 3**: Confluence/SharePoint/Teams integration with document lifecycle tracking
**Phase 4**: Full C4 model implementation with automated updates via webhooks

## Key Technical Decisions

- **Local-first approach**: All components run locally for privacy and control
- **Open source stack**: Neo4j Community, Qdrant, Tree-sitter, Python MCP SDK
- **MCP integration**: Follows OpenAI's Model Context Protocol for AI tool integration
- **Graph-based knowledge**: Uses Neo4j to model relationships between code, teams, and decisions
- **Semantic search**: Qdrant handles document embeddings for contextual search

## Project Structure (Expected)

```
src/
├── mcp_server/          # MCP server implementation
├── indexers/            # Code and document indexers
├── graph/              # Neo4j graph operations
├── vector/             # Qdrant vector operations
└── ingestors/          # Data ingestion from Jira, Confluence, etc.
scripts/                # Automation and setup scripts
tests/                  # Test suite
docs/                   # Technical documentation
```

## Integration Points

- **Jira**: Epic/story ingestion and relationship mapping
- **GitHub**: Repository monitoring and webhook integration
- **Documentation platforms**: Confluence, SharePoint, Teams content indexing
- **AI assistants**: GitHub Copilot, OpenAI, Claude via MCP protocol

## Context for AI Development

When working with this codebase, consider:
- This is a knowledge management system designed to provide AI with comprehensive project context
- The C4 model (Code, Component, Container, System) is central to the architecture
- Privacy is paramount - everything runs locally
- The system should help AI understand deprecated vs. current documentation
- Integration with existing developer workflows (Jira stories → code context) is key