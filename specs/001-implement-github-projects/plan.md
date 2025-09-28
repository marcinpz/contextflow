
# Implementation Plan: Implement GitHub Projects/Issues/Milestones Management

**Branch**: `001-implement-github-projects` | **Date**: 2025-09-28 | **Spec**: specs/001-implement-github-projects/spec.md
**Input**: Feature specification from `/specs/001-implement-github-projects/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Implement GitHub API integration to collect projects, issues, and milestones data for ContextFlow's knowledge graph. This extends the existing integration pattern (similar to Jira) to include GitHub project management data, enabling AI assistants to understand project context and dependencies.

## Technical Context
**Language/Version**: Python 3.11
**Primary Dependencies**: GitHub REST API, PyGitHub library, Neo4j driver
**Storage**: Neo4j graph database
**Testing**: pytest with contract and integration tests
**Target Platform**: Linux server
**Project Type**: single (Python application)
**Performance Goals**: <2 second response time for GitHub data queries
**Constraints**: Respect GitHub API rate limits, handle authentication securely
**Scale/Scope**: Support multiple repositories, handle 1000+ issues per repository

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Context Engineering First**: Extends context collection to include GitHub project management data
✅ **Privacy-First Architecture**: All GitHub data processing occurs locally with secure token handling
✅ **Integration-Centric Design**: Follows existing pattern for external integrations (similar to Jira)
✅ **Performance-Optimized**: Targets sub-2 second query responses for GitHub data
✅ **AI-Agnostic Compatibility**: Provides data via MCP protocol compatible with all AI assistants
✅ **Security Requirements**: Implements secure authentication and audit logging for GitHub API access
✅ **Development Workflow**: Will follow test-first development with code reviews

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
src/
├── integrations/
│   └── github/
│       ├── models.py
│       ├── client.py
│       ├── collector.py
│       └── __init__.py
├── graph/
│   └── github_schema.py
├── mcp/
│   └── tools/
│       └── github_tools.py
└── config/
    └── github_config.py

tests/
├── contract/
│   └── test_github_api.py
├── integration/
│   └── test_github_collection.py
└── unit/
    └── test_github_models.py
```

**Structure Decision**: Single Python project structure with dedicated github integration module following existing patterns (similar to jira integration). Places GitHub-specific code in src/integrations/github/ with corresponding tests.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
    - GitHub API authentication method (token-based vs OAuth)
    - PyGitHub library capabilities and limitations
    - GitHub API rate limiting and best practices
    - Neo4j schema design for GitHub entities

2. **Generate and dispatch research agents**:
    ```
    Task: "Research GitHub API authentication methods for server-side applications"
    Task: "Evaluate PyGitHub library for GitHub data collection"
    Task: "Find best practices for GitHub API rate limit handling"
    Task: "Design Neo4j schema for GitHub issues, projects, and milestones"
    ```

3. **Consolidate findings** in `research.md` using format:
    - Decision: [what was chosen]
    - Rationale: [why chosen]
    - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
    - GitHubIssue: id, title, body, state, labels, assignees, created_at, updated_at
    - GitHubProject: id, name, body, state, columns
    - GitHubMilestone: id, title, description, due_on, state, open_issues, closed_issues
    - GitHubRepository: id, name, full_name, description, issues, projects, milestones
    - Relationships: Issue belongs to Repository, Issue can be in Project/Milestone

2. **Generate API contracts** from functional requirements:
    - GitHub REST API endpoints for issues, projects, milestones
    - Output OpenAPI schema to `/contracts/github-api.yaml`

3. **Generate contract tests** from contracts:
    - test_github_issues_api.py: Assert issue endpoint schemas
    - test_github_projects_api.py: Assert project endpoint schemas
    - test_github_milestones_api.py: Assert milestone endpoint schemas
    - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
    - Integration test: Collect GitHub issues and verify storage in Neo4j
    - Integration test: Query GitHub project data via MCP tools
    - Quickstart test: Configure GitHub integration and verify data collection

5. **Update agent file incrementally** (O(1) operation):
    - Run `.specify/scripts/bash/update-agent-context.sh opencode`
      **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
    - Add GitHub API integration details
    - Preserve manual additions between markers
    - Update recent changes (keep last 3)
    - Keep under 150 lines for token efficiency
    - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, AGENTS.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each GitHub entity → model creation task [P]
- Each API contract → contract test task [P]
- GitHub client implementation → service task
- Neo4j schema setup → graph task
- MCP tools for GitHub queries → tool task
- Integration tests from user stories

**Ordering Strategy**:
- TDD order: Contract tests before implementation
- Dependency order: Models → Client → Collector → Graph schema → MCP tools
- Mark [P] for parallel execution (independent model/test files)

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command)
- [x] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`*
