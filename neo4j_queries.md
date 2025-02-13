# Neo4j Queries for 3GPP NAS Knowledge Graph

This document contains useful Cypher queries for exploring the 3GPP NAS knowledge graph in Neo4j Browser.

## Basic Graph Exploration

```cypher
// View all nodes and relationships (limited to 100 for performance)
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100;

// View entity types and their counts
MATCH (n:Entity)
RETURN n.type as EntityType, count(*) as Count
ORDER BY Count DESC;

// View all relationship types and their counts
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(*) as Count
ORDER BY Count DESC;
```

## Message Flows

```cypher
// View NAS message flows between network elements
MATCH path = (n:Entity)-[r:SENDS|RECEIVES]->(m:Entity)
WHERE n.type = 'NETWORK_ELEMENT' AND m.type = 'MESSAGE'
RETURN path
LIMIT 50;

// View specific message flows for UE
MATCH path = (ue:Entity {name: 'UE'})-[r:SENDS|RECEIVES]->(m:Entity)
WHERE m.type = 'MESSAGE'
RETURN path;

// View message flows with properties (timing, parameters)
MATCH (n:Entity)-[r]->(m:Entity)
WHERE m.type = 'MESSAGE' AND (EXISTS(r.timing) OR EXISTS(r.parameters))
RETURN n.name, type(r), m.name, r.timing, r.parameters;
```

## State Transitions

```cypher
// View all state transitions
MATCH path = (s1:Entity)-[r:TRANSITIONS_TO]->(s2:Entity)
WHERE s1.type = 'STATE' AND s2.type = 'STATE'
RETURN path;

// View state transitions with conditions
MATCH (s1:Entity)-[r:TRANSITIONS_TO]->(s2:Entity)
WHERE s1.type = 'STATE' AND EXISTS(r.conditions)
RETURN s1.name, s2.name, r.conditions;
```

## Procedures and Network Elements

```cypher
// View procedure flows
MATCH path = (n:Entity)-[r:INITIATES|PERFORMS]->(p:Entity)
WHERE n.type = 'NETWORK_ELEMENT' AND p.type = 'PROCEDURE'
RETURN path
LIMIT 50;

// View authentication-related patterns
MATCH path = (n:Entity)-[r:AUTHENTICATES]->(m:Entity)
RETURN path;

// View procedures with their messages
MATCH path = (p:Entity)-[r:USES]->(m:Entity)
WHERE p.type = 'PROCEDURE' AND m.type = 'MESSAGE'
RETURN path;
```

## Complex Patterns

```cypher
// Find complete registration flow
MATCH path = (ue:Entity {name: 'UE'})-[*1..5]->(m:Entity)
WHERE m.type = 'MESSAGE' AND any(r IN relationships(path) WHERE type(r) IN ['SENDS', 'RECEIVES'])
RETURN path;

// Find error handling patterns
MATCH path = (e:Entity)-[r1]->(a:Entity)-[r2]->(s:Entity)
WHERE e.type = 'EVENT' AND a.type = 'ACTION'
RETURN path;

// View protocol stack relationships
MATCH path = (p1:Entity)-[r]->(p2:Entity)
WHERE p1.type = 'PROTOCOL' AND p2.type IN ['MESSAGE', 'PROCEDURE']
RETURN path;
```

## Usage Tips

1. Access Neo4j Browser at `http://localhost:7474`
2. Log in with your Neo4j credentials
3. Copy and paste queries into the command bar
4. Click the play button or press Ctrl+Enter to run
5. Use the visualization tools:
   - Click and drag nodes to rearrange
   - Double-click nodes to expand relationships
   - Mouse wheel to zoom
   - Click nodes/relationships for properties
   - Use styling panel for customization

## Common Filters

Add these WHERE clauses to any query to filter results:

```cypher
// Filter by entity name
WHERE n.name CONTAINS 'Registration'

// Filter by multiple entity types
WHERE n.type IN ['MESSAGE', 'PROCEDURE']

// Filter relationships with specific properties
WHERE EXISTS(r.parameters)

// Limit path length
WHERE length(path) <= 3
``` 