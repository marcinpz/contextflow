# Tasks: Neo4j Integration for Knowledge Graph

**Input**: Design documents from `/specs/004-neo4j-integration/`
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
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create neo4j_integration module structure
- [ ] T002 Add neo4j-driver and docker dependencies to pyproject.toml
- [ ] T003 [P] Configure linting for neo4j_integration module

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test for install_neo4j in tests/contract/test_install_neo4j.py
- [ ] T005 [P] Contract test for create_schema in tests/contract/test_create_schema.py
- [ ] T006 [P] Contract test for connect_to_neo4j in tests/contract/test_connect_neo4j.py
- [ ] T007 [P] Integration test for C4 schema creation in tests/integration/test_c4_schema.py
- [ ] T008 [P] Integration test for graph queries in tests/integration/test_graph_queries.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T009 [P] Context entity model in src/neo4j_integration/models.py
- [ ] T010 [P] Container entity model in src/neo4j_integration/models.py
- [ ] T011 [P] Component entity model in src/neo4j_integration/models.py
- [ ] T012 [P] Code entity model in src/neo4j_integration/models.py
- [ ] T013 Neo4jClient class in src/neo4j_integration/client.py
- [ ] T014 Schema creation functions in src/neo4j_integration/schema.py
- [ ] T015 Neo4j installation script in src/neo4j_integration/install.py
- [ ] T016 Connection management in src/neo4j_integration/client.py

## Phase 3.4: Integration
- [ ] T017 Docker integration for Neo4j container
- [ ] T018 Error handling for Neo4j operations
- [ ] T019 Logging for graph operations

## Phase 3.5: Polish
- [ ] T020 [P] Unit tests for models in tests/unit/test_models.py
- [ ] T021 Performance tests for queries
- [ ] T022 [P] Update README with Neo4j setup instructions
- [ ] T023 Run quickstart validation

## Dependencies
- Tests (T004-T008) before implementation (T009-T016)
- T009-T012 blocks T013, T017
- T013 blocks T016
- Implementation before polish (T020-T023)

## Parallel Example
```
# Launch T004-T008 together:
Task: "Contract test for install_neo4j in tests/contract/test_install_neo4j.py"
Task: "Contract test for create_schema in tests/contract/test_create_schema.py"
Task: "Contract test for connect_to_neo4j in tests/contract/test_connect_neo4j.py"
Task: "Integration test for C4 schema creation in tests/integration/test_c4_schema.py"
Task: "Integration test for graph queries in tests/integration/test_graph_queries.py"
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

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task