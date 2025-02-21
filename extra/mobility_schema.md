# Mobility Management Knowledge Graph Schema

## Nodes (Entities)

### 1. UE (User Equipment)
- Properties:
  - id (unique)
  - status
  - registration_time
  - connection_state
  - security_context
  - 5g_guti
  - location

### 2. AMF (Access and Mobility Management Function)
- Properties:
  - amf_id (unique)
  - amf_region
  - amf_set
  - capacity
  - status
  - served_areas
  - load_level

### 3. Registration
- Properties:
  - id (unique)
  - type
  - status
  - timestamp
  - result
  - cause
  - follow_on_request
  - update_type

### 4. NetworkArea
- Properties:
  - area_code (unique)
  - plmn_id
  - tac
  - cell_id
  - access_type
  - coverage_level
  - congestion_level

### 5. MobilityEvent
- Properties:
  - id (unique)
  - event_type
  - trigger
  - timestamp
  - source_area
  - target_area
  - result
  - cause

### 6. Connection
- Properties:
  - id (unique)
  - state
  - type
  - quality
  - establishment_cause
  - release_cause
  - duration
  - pdu_sessions

## Relationships

1. `(UE)-[:REGISTERED_WITH]->(AMF)`
   - Properties:
     - timestamp
     - type
     - status

2. `(UE)-[:LOCATED_IN]->(NetworkArea)`
   - Properties:
     - timestamp
     - entry_time
     - exit_time

3. `(AMF)-[:SERVES_AREA]->(NetworkArea)`
   - Properties:
     - capacity
     - load_level
     - status

4. `(UE)-[:INVOLVED_IN]->(MobilityEvent)`
   - Properties:
     - timestamp
     - result
     - cause

5. `(UE)-[:HAS_CONNECTION]->(Connection)`
   - Properties:
     - establishment_time
     - status
     - quality

## Example Queries

### 1. Find UE Location
```cypher
MATCH (u:UE)-[r:LOCATED_IN]->(n:NetworkArea)
WHERE u.id = $ue_id
RETURN n.area_code, n.plmn_id, r.timestamp
```

### 2. Track UE Movement History
```cypher
MATCH (u:UE)-[r:LOCATED_IN]->(n:NetworkArea)
WHERE u.id = $ue_id
RETURN n.area_code, r.timestamp
ORDER BY r.timestamp DESC
LIMIT 10
```

### 3. Get AMF Load
```cypher
MATCH (a:AMF)-[r:SERVES_AREA]->(n:NetworkArea)
WHERE a.amf_id = $amf_id
RETURN a.load_level, COUNT(n) as area_count
```

### 4. Find Registration History
```cypher
MATCH (u:UE)-[r:REGISTERED_WITH]->(a:AMF)
WHERE u.id = $ue_id
RETURN a.amf_id, r.timestamp, r.type
ORDER BY r.timestamp DESC
```

### 5. Get Recent Mobility Events
```cypher
MATCH (u:UE)-[:INVOLVED_IN]->(m:MobilityEvent)
WHERE u.id = $ue_id
RETURN m.event_type, m.timestamp, m.source_area, m.target_area
ORDER BY m.timestamp DESC
LIMIT 5
```

## Usage Notes

1. All timestamps are stored in ISO 8601 format
2. Area codes follow 3GPP specifications
3. Event types are standardized according to 3GPP TS 24.501
4. Load levels are represented as percentages (0-100)
5. Connection states follow 5G-NR state definitions 