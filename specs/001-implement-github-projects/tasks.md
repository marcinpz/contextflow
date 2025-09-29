# Tasks: Implement GitHub Projects/Issues/Milestones Management

**Input**: Design documents from `/specs/001-implement-github-projects/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
    → If not found: ERROR "No implementation plan found"
    → Extract: tech stack, libraries, structure
2. Load optional design documents:
    → data-model.md: Extract entities → model tasks
    → contracts/: Each file → contract test task
    → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
    → Setup: project init, dependencies, linting
    → Tests: contract tests, integration tests
    → Core: models, services, CLI commands
    → Integration: DB, middleware, logging
    → Polish: unit tests, performance, docs
4. Apply task rules:
    → Different files = mark [P] for parallel
    → Same file = sequential (no [P])
    → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
    → All contracts have tests?
    → All entities have models?
    → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Install PyGitHub and dependencies
- [ ] T002 [P] Configure GitHub authentication in config/github_config.py

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T003 [P] Contract test GitHub issues API in tests/contract/test_github_issues_api.py
- [ ] T004 [P] Contract test GitHub projects API in tests/contract/test_github_projects_api.py
- [ ] T005 [P] Contract test GitHub milestones API in tests/contract/test_github_milestones_api.py
- [ ] T006 [P] Integration test GitHub data collection in tests/integration/test_github_collection.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T007 [P] GitHubIssue model in src/integrations/github/models.py
- [ ] T008 [P] GitHubProject model in src/integrations/github/models.py
- [ ] T009 [P] GitHubMilestone model in src/integrations/github/models.py
- [ ] T010 [P] GitHubRepository model in src/integrations/github/models.py
- [ ] T011 GitHub API client in src/integrations/github/client.py
- [ ] T012 GitHub data collector in src/integrations/github/collector.py
- [ ] T013 Neo4j schema for GitHub entities in src/graph/github_schema.py

## Phase 3.4: Integration
- [ ] T014 MCP tools for GitHub queries in src/mcp/tools/github_tools.py
- [ ] T015 GitHub configuration module in src/config/github_config.py

## Phase 3.5: Polish
- [ ] T016 [P] Unit tests for GitHub models in tests/unit/test_github_models.py
- [ ] T017 Performance tests for GitHub queries (<2 seconds)
- [ ] T018 [P] Update documentation for GitHub integration

## Dependencies
- Tests (T003-T006) before implementation (T007-T015)
- Models (T007-T010) before client (T011)
- Client before collector (T012)
- Schema (T013) before MCP tools (T014)
- Implementation before polish (T016-T018)

## Parallel Example
```
# Launch T003-T006 together:
Task: "Contract test GitHub issues API in tests/contract/test_github_issues_api.py"
Task: "Contract test GitHub projects API in tests/contract/test_github_projects_api.py"
Task: "Contract test GitHub milestones API in tests/contract/test_github_milestones_api.py"
Task: "Integration test GitHub data collection in tests/integration/test_github_collection.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
    - Each contract file → contract test task [P]
    - Each endpoint → implementation task

2. **From Data Model**:
    - Each entity → model creation task [P]
    - Relationships → service layer tasks

3. **From User Stories**:
    - Each story → integration test [P]
    - Quickstart scenarios → validation tasks

4. **Ordering**:
    - Setup → Tests → Models → Services → Endpoints → Polish
    - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task