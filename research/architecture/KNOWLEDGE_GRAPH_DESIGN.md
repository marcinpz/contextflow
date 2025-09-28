# Knowledge Graph Design for ContextFlow

## Overview

This document describes the knowledge graph architecture that powers ContextFlow's AI context enhancement. The knowledge graph serves as the central intelligence layer that connects code, documentation, project management, and organizational knowledge into a unified, queryable structure.

## Core Principles

### 1. Multi-Modal Knowledge Integration
The graph integrates multiple knowledge sources:
- **Structural knowledge**: Code dependencies, class hierarchies, method calls
- **Semantic knowledge**: Documentation, architectural decisions, business logic
- **Temporal knowledge**: Git history, change patterns, evolution over time
- **Contextual knowledge**: Project status, team decisions, current priorities

### 2. AI-First Query Patterns
Graph queries are designed for AI consumption:
- **Context injection**: Provide relevant context for specific queries
- **Impact analysis**: Understand cascading effects of changes
- **Pattern recognition**: Identify similar implementations and anti-patterns
- **Decision support**: Historical context for architectural choices

### 3. Scalable Architecture
- **Progressive complexity**: Start simple, evolve to advanced patterns
- **Performance optimization**: Efficient queries for real-time AI responses
- **Data consistency**: Maintain graph accuracy as codebase evolves

## Graph Schema Definition

### Node Types (Entities)

#### Code Entities
```cypher
// Classes, interfaces, enums
(:Class {
  name: "UserService",
  file_path: "src/main/java/com/example/UserService.java",
  package: "com.example",
  language: "java",
  created_at: datetime(),
  last_modified: datetime(),
  complexity_score: 0.85
})

// Methods and functions
(:Method {
  name: "findUserById",
  signature: "User findUserById(Long id)",
  class_name: "UserService",
  visibility: "public",
  line_start: 45,
  line_end: 52,
  complexity: 3
})

// Properties and fields
(:Property {
  name: "app.database.url",
  type: "String",
  default_value: "jdbc:postgresql://localhost:5432/app",
  sources: ["application.yml", "application-prod.yml"]
})
```

#### Documentation Entities
```cypher
// Architectural Decision Records
(:ADR {
  title: "Database Choice for User Data",
  decision: "PostgreSQL with read replicas",
  status: "accepted",
  date: date("2024-01-15"),
  author: "John Doe",
  tags: ["database", "scalability", "performance"]
})

// API Documentation
(:APIDoc {
  endpoint: "/api/users/{id}",
  method: "GET",
  description: "Retrieve user by ID",
  version: "v2",
  deprecated: false,
  last_updated: datetime()
})
```

#### Project Management Entities
```cypher
// Jira/GitHub Issues
(:Issue {
  key: "PROJ-123",
  title: "Implement user preferences feature",
  status: "In Progress",
  priority: "High",
  assignee: "Jane Smith",
  created_at: datetime(),
  updated_at: datetime(),
  labels: ["frontend", "backend", "database"]
})

// Pull Requests / Commits
(:PullRequest {
  number: 456,
  title: "Add user preferences API",
  status: "merged",
  author: "Jane Smith",
  created_at: datetime(),
  merged_at: datetime(),
  files_changed: 12,
  lines_added: 245,
  lines_deleted: 23
})
```

#### Configuration Entities
```cypher
// Configuration Properties
(:ConfigProperty {
  name: "app.cache.enabled",
  type: "boolean",
  default_value: "true",
  description: "Enable caching layer",
  environments: ["dev", "staging", "prod"],
  last_changed: datetime()
})

// Environment Variables
(:Environment {
  name: "production",
  variables: {
    "DB_HOST": "prod-db.example.com",
    "CACHE_SIZE": "1024"
  },
  last_deployed: datetime()
})
```

### Relationship Types

#### Structural Relationships
```cypher
// Code structure
(class:Class)-[:CONTAINS]->(method:Method)
(class:Class)-[:IMPLEMENTS]->(interface:Class)
(class:Class)-[:EXTENDS]->(parent:Class)
(method:Method)-[:CALLS]->(otherMethod:Method)

// Dependencies
(class:Class)-[:USES_PROPERTY {line: 15, annotation: "@Value"}]->(prop:ConfigProperty)
(method:Method)-[:ACCESSES]->(field:Property)
```

#### Semantic Relationships
```cypher
// Documentation links
(adr:ADR)-[:INFLUENCES]->(class:Class)
(apiDoc:APIDoc)-[:DOCUMENTS]->(method:Method)
(issue:Issue)-[:REQUIRES_CHANGE]->(class:Class)

// Business logic
(feature:Feature)-[:IMPLEMENTS]->(requirement:Requirement)
(class:Class)-[:REPRESENTS {domain: "User Management"}]->(businessEntity:BusinessEntity)
```

#### Temporal Relationships
```cypher
// Change history
(commit:Commit)-[:MODIFIED]->(class:Class)
(pr:PullRequest)-[:CHANGED]->(method:Method)
(issue:Issue)-[:WAS_RESOLVED_BY]->(pr:PullRequest)

// Evolution
(oldClass:Class)-[:RENAMED_TO {date: datetime()}]->(newClass:Class)
(oldMethod:Method)-[:REFACTORED_INTO {commit: "abc123"}]->(newMethods:Method)
```

#### Contextual Relationships
```cypher
// Project context
(issue:Issue)-[:BELONGS_TO {epic: "PROJ-100"}]->(epic:Issue)
(developer:Person)-[:OWNS]->(class:Class)
(team:Team)-[:MAINTAINS]->(service:Service)

// Cross-system links
(config:ConfigProperty)-[:OVERRIDDEN_IN]->(env:Environment)
(doc:Documentation)-[:REFERENCES]->(code:CodeEntity)
```

## Query Patterns for AI Context

### Structural Context Queries

#### Find All Dependencies of a Class
```cypher
MATCH (target:Class {name: $class_name})
OPTIONAL MATCH (target)<-[:USES_PROPERTY]-(using:Property)
OPTIONAL MATCH (target)<-[:CALLS]-(caller:Method)
OPTIONAL MATCH (target)<-[:IMPLEMENTS]-(implementor:Class)
OPTIONAL MATCH (target)<-[:EXTENDS]-(child:Class)
RETURN {
  class: target,
  used_by_properties: collect(using),
  called_by_methods: collect(caller),
  implemented_by: collect(implementor),
  extended_by: collect(child)
}
```

#### Impact Analysis for Property Change
```cypher
MATCH (prop:ConfigProperty {name: $property_name})
OPTIONAL MATCH (prop)<-[usage:USES_PROPERTY]-(code:CodeEntity)
OPTIONAL MATCH (prop)-[:OVERRIDDEN_IN]->(env:Environment)
OPTIONAL MATCH (prop)<-[:REFERENCES]-(doc:Documentation)
RETURN {
  property: prop,
  used_in_code: collect({entity: code, line: usage.line}),
  environment_overrides: collect(env),
  documented_in: collect(doc)
}
```

### Semantic Context Queries

#### Find Similar Implementation Patterns
```cypher
MATCH (target:Method {name: $method_name})
MATCH (similar:Method)
WHERE similar <> target
  AND similar.signature =~ $pattern_regex
  AND size((target)-[:CALLS]->()<-[:CALLS]-(similar)) > 2
RETURN similar, count(*) as similarity_score
ORDER BY similarity_score DESC
LIMIT 5
```

#### Historical Decision Context
```cypher
MATCH (current:Class {name: $class_name})
OPTIONAL MATCH (current)<-[:INFLUENCES]-(adr:ADR)
OPTIONAL MATCH (current)<-[:REQUIRES_CHANGE]-(issue:Issue)
OPTIONAL MATCH (current)<-[:MODIFIED]-(commit:Commit)
WHERE commit.date >= datetime() - duration('P90D')
RETURN {
  class: current,
  architectural_context: collect(adr),
  recent_issues: collect(issue),
  recent_changes: collect(commit)
}
```

### Temporal Context Queries

#### Evolution of a Component
```cypher
MATCH (entity:CodeEntity {name: $entity_name})
MATCH (entity)<-[change:MODIFIED]-(commit:Commit)
OPTIONAL MATCH (entity)<-[rename:RENAMED_TO]-(oldEntity:CodeEntity)
OPTIONAL MATCH (entity)-[refactor:REFACTORED_INTO]->(newEntities:CodeEntity)
RETURN entity, collect({
  commit: commit,
  change_type: change.change_type,
  date: commit.date
}) as changes,
collect(oldEntity) as previous_names,
collect(newEntities) as refactored_into
ORDER BY commit.date DESC
```

#### Recent Context for Current Work
```cypher
MATCH (developer:Person {name: $current_user})
OPTIONAL MATCH (developer)-[:ASSIGNED_TO]->(issue:Issue {status: "In Progress"})
OPTIONAL MATCH (issue)-[:REQUIRES_CHANGE]->(code:CodeEntity)
OPTIONAL MATCH (code)<-[:MODIFIED]-(recent:Commit)
WHERE recent.date >= datetime() - duration('P7D')
OPTIONAL MATCH (code)<-[:INFLUENCES]-(adr:ADR)
RETURN {
  current_tasks: collect(issue),
  affected_code: collect(code),
  recent_changes: collect(recent),
  relevant_decisions: collect(adr)
}
```

## Graph Algorithms for Intelligence

### Importance Ranking (PageRank)
Identify the most critical components in the system:

```cypher
CALL gds.pageRank.stream('CodeGraph', {
  nodeLabels: ['Class', 'Method'],
  relationshipTypes: ['CALLS', 'USES_PROPERTY', 'IMPLEMENTS'],
  maxIterations: 20,
  dampingFactor: 0.85
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name as entity_name,
       gds.util.asNode(nodeId).file_path as file,
       score as importance_score
ORDER BY score DESC
LIMIT 20
```

### Dependency Distance Analysis
Find how changes propagate through the system:

```cypher
MATCH (start:CodeEntity {name: $start_entity})
MATCH (end:CodeEntity {name: $end_entity})
MATCH path = shortestPath((start)-[*]-(end))
WHERE length(path) > 0
RETURN {
  start: start,
  end: end,
  path: [node in nodes(path) | node.name],
  distance: length(path),
  relationship_types: [rel in relationships(path) | type(rel)]
}
```

### Community Detection
Identify natural modules and architectural boundaries:

```cypher
CALL gds.louvain.stream('CodeGraph', {
  nodeLabels: ['Class'],
  relationshipTypes: ['CALLS', 'USES_PROPERTY', 'IMPLEMENTS'],
  includeIntermediateCommunities: false
})
YIELD nodeId, communityId, intermediateCommunityIds
RETURN communityId,
       collect(gds.util.asNode(nodeId).name) as members,
       size(collect(gds.util.asNode(nodeId))) as community_size
ORDER BY community_size DESC
```

### Change Impact Prediction
Predict which components are likely to be affected by changes:

```cypher
MATCH (changed:CodeEntity {name: $changed_entity})
CALL gds.betweenness.stream('CodeGraph', {
  nodeLabels: ['Class', 'Method'],
  relationshipTypes: ['CALLS', 'USES_PROPERTY']
})
YIELD nodeId, score
WHERE score > 0
RETURN gds.util.asNode(nodeId).name as entity,
       score as impact_score,
       exists((changed)-[*1..3]-(gds.util.asNode(nodeId))) as directly_connected
ORDER BY score DESC
LIMIT 15
```

## Multi-Layer Architecture

### Layer 1: Structural Layer (Neo4j)
- **Purpose**: Exact relationships and dependencies
- **Queries**: Precise graph traversals, dependency analysis
- **Strengths**: ACID compliance, complex relationship queries
- **Use Cases**: Impact analysis, refactoring support

### Layer 2: Semantic Layer (Qdrant Integration)
- **Purpose**: Meaning-based similarity and search
- **Queries**: Vector similarity, semantic search
- **Strengths**: Fuzzy matching, pattern recognition
- **Use Cases**: Finding similar code, documentation search

### Layer 3: Temporal Layer (Git Integration)
- **Purpose**: Historical context and evolution tracking
- **Queries**: Change history, evolution patterns
- **Strengths**: Time-based analysis, trend detection
- **Use Cases**: Understanding how code evolved, predicting future changes

### Layer 4: Contextual Layer (External Systems)
- **Purpose**: Business context and project status
- **Queries**: Current priorities, team assignments, business rules
- **Strengths**: Real-world relevance, decision context
- **Use Cases**: Task prioritization, stakeholder communication

## Query Federation Architecture

The knowledge graph serves as the central query coordinator:

```python
class KnowledgeGraphQueryEngine:
    def query_context(self, query: str, context: dict) -> dict:
        """
        Federated query across all layers for comprehensive context
        """

        # 1. Parse query intent
        intent = self.classify_query_intent(query)

        # 2. Structural layer - exact relationships
        structural_results = self.graph_db.query("""
            MATCH (entity:CodeEntity)
            WHERE entity.name =~ $intent.pattern
            MATCH (entity)-[r]-(related)
            RETURN entity, collect(related) as relationships
        """, intent=intent)

        # 3. Semantic layer - similar patterns
        semantic_results = self.vector_db.search(
            query=query,
            filter={"language": context.get("language")},
            limit=10
        )

        # 4. Temporal layer - recent changes
        temporal_results = self.graph_db.query("""
            MATCH (entity:CodeEntity)-[r:MODIFIED]-(commit:Commit)
            WHERE commit.date >= $recent_threshold
              AND entity.name =~ $intent.pattern
            RETURN entity, collect(commit) as recent_changes
        """, recent_threshold=datetime.now() - timedelta(days=30))

        # 5. Contextual layer - business relevance
        contextual_results = self.graph_db.query("""
            MATCH (entity:CodeEntity)
            OPTIONAL MATCH (entity)<-[:REQUIRES_CHANGE]-(issue:Issue {status: "In Progress"})
            OPTIONAL MATCH (entity)<-[:INFLUENCES]-(adr:ADR)
            WHERE entity.name =~ $intent.pattern
            RETURN entity, collect(issue) as active_issues, collect(adr) as decisions
        """)

        # 6. Fuse results with AI ranking
        return self.fuse_results({
            "structural": structural_results,
            "semantic": semantic_results,
            "temporal": temporal_results,
            "contextual": contextual_results
        }, query, context)
```

## Performance Optimization

### Indexing Strategy
```cypher
// Create indexes for common query patterns
CREATE INDEX idx_class_name FOR (c:Class) ON (c.name)
CREATE INDEX idx_method_signature FOR (m:Method) ON (m.signature)
CREATE INDEX idx_property_name FOR (p:ConfigProperty) ON (p.name)
CREATE INDEX idx_issue_status FOR (i:Issue) ON (i.status)

// Composite indexes for complex queries
CREATE INDEX idx_class_file FOR (c:Class) ON (c.name, c.file_path)
CREATE INDEX idx_method_complexity FOR (m:Method) ON (m.complexity, m.class_name)

// Full-text indexes for search
CREATE FULLTEXT INDEX idx_entity_search FOR (n:CodeEntity|Documentation) ON EACH [n.name, n.description]
```

### Query Optimization
```cypher
// Use query profiling to identify bottlenecks
PROFILE
MATCH (c:Class {name: $class_name})
MATCH (c)-[:CONTAINS]->(m:Method)
MATCH (m)-[:CALLS]->(other:Method)
RETURN c, collect(m) as methods, collect(other) as calls

// Optimize with early filtering
MATCH (c:Class)
WHERE c.name = $class_name
AND c.language = $language  // Filter early
MATCH (c)-[:CONTAINS]->(m:Method)
RETURN c, collect(m) as methods
```

### Caching Strategy
```python
class GraphCache:
    def __init__(self):
        self.query_cache = {}  # LRU cache for frequent queries
        self.entity_cache = {}  # Cache for entity lookups
        self.relationship_cache = {}  # Cache for relationship patterns

    def get_cached_context(self, entity_name: str, context_type: str) -> dict:
        """Get cached context with TTL"""
        cache_key = f"{entity_name}:{context_type}"
        if cache_key in self.query_cache:
            cached = self.query_cache[cache_key]
            if datetime.now() - cached['timestamp'] < timedelta(minutes=30):
                return cached['data']

        # Cache miss - query graph
        result = self.query_graph(entity_name, context_type)
        self.query_cache[cache_key] = {
            'data': result,
            'timestamp': datetime.now()
        }
        return result
```

## Evolution and Maintenance

### Schema Evolution
```cypher
// Add new properties to existing nodes
MATCH (c:Class)
WHERE NOT exists(c.complexity_score)
SET c.complexity_score = 0.5

// Migrate relationship types
MATCH (a)-[r:USES]->(b)
CREATE (a)-[:USES_PROPERTY {migrated: true}]->(b)
DELETE r
```

### Data Quality Assurance
```cypher
// Find orphaned nodes
MATCH (n)
WHERE NOT (n)--()
RETURN count(n) as orphaned_count

// Validate relationship consistency
MATCH (c:Class)-[r:CONTAINS]->(m:Method)
WHERE m.class_name <> c.name
RETURN c.name, m.name, m.class_name

// Check for duplicate entities
MATCH (c1:Class), (c2:Class)
WHERE c1.name = c2.name
  AND c1.file_path <> c2.file_path
  AND id(c1) < id(c2)
RETURN c1, c2
```

### Incremental Updates
```python
class GraphUpdater:
    def update_on_file_change(self, file_path: str, change_type: str):
        """Update graph incrementally when files change"""

        if change_type == "modified":
            # Update existing nodes
            self.update_file_entities(file_path)
        elif change_type == "deleted":
            # Remove nodes and relationships
            self.remove_file_entities(file_path)
        elif change_type == "created":
            # Add new nodes and relationships
            self.add_file_entities(file_path)

        # Update affected relationships
        self.update_relationships(file_path)

        # Invalidate relevant caches
        self.invalidate_caches(file_path)
```

## Implementation Roadmap

### Phase 1: Core Schema (2 weeks)
- [ ] Define basic node and relationship types
- [ ] Implement core Cypher queries
- [ ] Set up Neo4j with initial schema
- [ ] Create basic indexing

### Phase 2: AI Query Patterns (2 weeks)
- [ ] Implement context injection queries
- [ ] Add impact analysis algorithms
- [ ] Create query federation layer
- [ ] Performance optimization

### Phase 3: Multi-Layer Integration (3 weeks)
- [ ] Integrate Qdrant for semantic search
- [ ] Add temporal layer with Git history
- [ ] Implement contextual layer with Jira
- [ ] Advanced graph algorithms

### Phase 4: Production Optimization (2 weeks)
- [ ] Query performance tuning
- [ ] Caching implementation
- [ ] Data quality monitoring
- [ ] Incremental update system

This knowledge graph design provides the foundation for ContextFlow's AI context enhancement, enabling intelligent, context-aware assistance that understands the complex relationships within large codebases.