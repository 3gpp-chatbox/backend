# Neo4j Queries for 3GPP Network Registration Analysis

## Complete Graph Visualization

```cypher
// View the complete graph with all nodes and relationships
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN *
```

## Network Element Queries

### View All Network Elements and Their Relationships
```cypher
MATCH (n1:NetworkElement)-[r]->(n2:NetworkElement)
RETURN n1, r, n2
```

### View Network Element Dependencies
```cypher
MATCH (n1:NetworkElement)-[r]->(n2:NetworkElement)
WITH n1, collect({target: n2.name, relationship: type(r)}) as dependencies
RETURN n1.name, dependencies
```

## State Transition Queries

### View State Transitions Flow
```cypher
MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
RETURN s1, r, s2
```

### View Complete Registration Flow with Conditions and Triggers
```cypher
MATCH path = (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
WHERE r.trigger IS NOT NULL OR r.condition IS NOT NULL
RETURN path
```

### Find All States for a Specific Network Element
```cypher
MATCH (ne:NetworkElement)-[r]-(s:State)
WHERE ne.name = 'UE'  // or 'AMF', 'SMF', etc.
RETURN ne, r, s
```

### View Registration States with Their Properties
```cypher
MATCH (s:State)
RETURN s.name, s.type, s.description
ORDER BY s.type
```

## Relationship Analysis

### Find Relationships Between Network Elements with Details
```cypher
MATCH (n1:NetworkElement)-[r]->(n2:NetworkElement)
RETURN n1.name, type(r), r.description, n2.name
```

### View Complete Network Element Interactions
```cypher
MATCH path = (n1:NetworkElement)-[*]->(n2:NetworkElement)
RETURN path
```

## State Transitions and Conditions

### Find Specific State Transitions with Conditions
```cypher
MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
WHERE r.condition IS NOT NULL
RETURN s1.name, r.trigger, r.condition, s2.name
```

## Statistics and Counts

### Count Different Types of Nodes and Relationships
```cypher
// Count nodes by type
MATCH (n)
RETURN labels(n) as Type, count(*) as Count;

// Count relationships by type
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count;
```

## Triggers and Timing

### Find All Triggers and Their Associated States
```cypher
MATCH (t:Trigger)-[r]->(s:State)
RETURN t.name, type(r), s.name
```

### View Timing Information for States
```cypher
MATCH (t:Timing)-[r]->(s:State)
RETURN t.description, s.name
```

## Complex Path Analysis

### Find Complex Paths in Registration Flow
```cypher
MATCH path = (start:State)-[*2..5]->(end:State)
WHERE start.type = 'INITIAL' AND end.type = 'FINAL'
RETURN path
```

### Find Critical Path in Registration
```cypher
MATCH path = (start:State)-[*]->(end:State)
WHERE start.type = 'INITIAL' AND end.type = 'FINAL'
WITH path, relationships(path) as rels
RETURN path
ORDER BY length(rels) ASC
LIMIT 1
```

### View Conditional State Changes
```cypher
MATCH (s1:State)-[r]->(s2:State)
WHERE r.condition IS NOT NULL
RETURN s1.name, r.condition, s2.name
ORDER BY s1.name
```

## Visualization Styling

Use these commands in Neo4j Browser to enhance visualization:

```cypher
:style
node.State {
    color: #58C1B2;
    diameter: 80px;
}
node.NetworkElement {
    color: #71B37C;
    diameter: 80px;
}
```

## Tips for Visualization
1. Use `CALL apoc.meta.graph()` to see the complete graph structure
2. In Neo4j Browser visualization tools you can:
   - Color nodes by labels
   - Size nodes by degree
   - Show relationship properties
   - Filter by relationship types
3. For large graphs, use LIMIT to restrict the number of results
4. Use WHERE clauses to filter specific nodes or relationships
5. Use the browser's built-in styling tools to customize the appearance 