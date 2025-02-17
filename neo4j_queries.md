# Neo4j Queries for 3GPP Protocol Analysis

## Overall Graph Visualization

### 1. View Complete Graph Structure
```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100;
```

### 2. View Node Types Distribution
```cypher
MATCH (n)
RETURN DISTINCT labels(n) as NodeType, count(*) as Count
ORDER BY Count DESC;
```

### 3. View Relationship Types Distribution
```cypher
MATCH ()-[r]->()
RETURN DISTINCT type(r) as RelationType, count(*) as Count
ORDER BY Count DESC;
```

## Protocol State Machine

### 1. View All State Transitions
```cypher
MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
RETURN s1.name, type(r), s2.name, r.confidence
ORDER BY r.confidence DESC;
```

### 2. View State Machine for Specific Protocol
```cypher
MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
WHERE s1.type = $protocol_type  // e.g., 'EMM', '5GMM'
RETURN s1.name, type(r), s2.name, r.conditions
ORDER BY s1.name;
```

### 3. Find Most Connected States
```cypher
MATCH (s:State)
OPTIONAL MATCH (s)-[r]-()
RETURN s.name, s.type, count(r) as connections
ORDER BY connections DESC
LIMIT 10;
```

## Procedure Analysis

### 1. View Complete Procedure Flow
```cypher
MATCH path = (start:Action)-[r:TRIGGERS|IMPACTS*1..5]->(end:State)
WHERE start.name CONTAINS 'procedure'
RETURN path
LIMIT 10;
```

### 2. Analyze Specific Procedure (e.g., Registration)
```cypher
MATCH path = (a:Action)-[r*1..5]-(n)
WHERE a.name CONTAINS 'Registration'
RETURN path
LIMIT 20;
```

### 3. Find Procedure Prerequisites
```cypher
MATCH (a:Action)-[:HAS_PREREQUISITE]->(p:Prerequisite)
WHERE a.name CONTAINS 'procedure'
RETURN a.name, collect(p.text) as prerequisites;
```

## Event Analysis

### 1. View Event Triggers and Impacts
```cypher
MATCH (a:Action)-[:TRIGGERS]->(e:Event)-[:IMPACTS]->(s:State)
RETURN a.name as Action, e.name as Event, s.name as ResultingState
ORDER BY a.name;
```

### 2. Find Event Chains
```cypher
MATCH path = (e1:Event)-[r*1..3]->(e2:Event)
RETURN path
LIMIT 10;
```

### 3. Analyze Event Conditions
```cypher
MATCH (e:Event)-[:HAS_CONDITION]->(c:Condition)
RETURN e.name, collect(c.text) as conditions
ORDER BY e.name;
```

## Parameter Analysis

### 1. View Parameter Dependencies
```cypher
MATCH (p1:Parameter)-[:DEPENDS_ON]->(p2:Parameter)
RETURN p1.name, p2.name, p1.type, p2.type
ORDER BY p1.name;
```

### 2. Find Parameters Used in Procedures
```cypher
MATCH (a:Action)-[:USES_PARAMETER]->(p:Parameter)
WHERE a.name CONTAINS 'procedure'
RETURN a.name, collect(p.name) as parameters;
```

### 3. Analyze Mandatory Parameters
```cypher
MATCH (p:Parameter)
WHERE p.mandatory = true
RETURN p.name, p.type, p.value_range
ORDER BY p.type;
```

## Complex Path Analysis

### 1. Find All Paths Between States
```cypher
MATCH path = shortestPath((s1:State)-[*1..5]->(s2:State))
WHERE s1.name <> s2.name
RETURN path
LIMIT 10;
```

### 2. Analyze Procedure Success Paths
```cypher
MATCH path = (start:Action)-[:TRIGGERS|IMPACTS*1..5]->(success:State)
WHERE start.name CONTAINS 'procedure'
  AND success.name CONTAINS 'SUCCESS'
RETURN path
LIMIT 10;
```

### 3. Find Common Failure Scenarios
```cypher
MATCH path = (start:Action)-[:TRIGGERS|IMPACTS*1..5]->(failure:State)
WHERE start.name CONTAINS 'procedure'
  AND failure.name CONTAINS 'FAIL'
RETURN path
LIMIT 10;
```

## Temporal Analysis

### 1. View Recent Changes
```cypher
MATCH (n)
WHERE exists(n.created_at)
RETURN n.name, n.created_at
ORDER BY n.created_at DESC
LIMIT 10;
```

### 2. Find Updated Procedures
```cypher
MATCH (a:Action)
WHERE a.name CONTAINS 'procedure'
  AND exists(a.updated_at)
RETURN a.name, a.updated_at
ORDER BY a.updated_at DESC;
```

## Confidence Analysis

### 1. High Confidence Relationships
```cypher
MATCH (n1)-[r]->(n2)
WHERE exists(r.confidence) AND r.confidence > 0.8
RETURN n1.name, type(r), n2.name, r.confidence
ORDER BY r.confidence DESC;
```

### 2. Low Confidence Relationships
```cypher
MATCH (n1)-[r]->(n2)
WHERE exists(r.confidence) AND r.confidence < 0.6
RETURN n1.name, type(r), n2.name, r.confidence
ORDER BY r.confidence ASC;
```

## Visualization Tips

1. For better visualization in Neo4j Browser:
   - Use the `LIMIT` clause to restrict the number of nodes
   - Use different colors for different node types
   - Use different relationship types for visual distinction

2. For exporting to Mermaid:
   - Use the path-based queries
   - Limit the depth of relationships
   - Focus on specific procedures or state machines

3. For large graphs:
   - Start with high-confidence relationships
   - Focus on specific protocols or procedures
   - Use path length limits to prevent overwhelming visualizations