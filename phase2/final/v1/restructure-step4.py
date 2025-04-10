import json

def restructure_fsm(input_data):
    """
    Generic FSM restructure that:
    - Keeps all state nodes
    - Converts event nodes to edge labels
    - Preserves all transitions regardless of pattern
    - Maintains all metadata
    """
    # Extract nodes and edges
    nodes = input_data.get("graph", {}).get("nodes", [])
    edges = input_data.get("graph", {}).get("edges", [])
    
    # Categorize nodes
    state_nodes = [n for n in nodes if n.get("type") == "state"]
    event_nodes = [n for n in nodes if n.get("type") != "state"]
    
    # Create lookup tables
    node_descriptions = {n["id"]: n.get("description", "") for n in nodes}
    event_descriptions = {n["id"]: n.get("description", "") for n in event_nodes}
    
    # Build transition map (state -> event -> state)
    transition_map = {}
    
    # First pass: map all possible state transitions
    for edge in edges:
        if edge["type"] == "trigger":
            # State -> Event
            from_state = edge["from"]
            event = edge["to"]
            transition_map.setdefault(from_state, {}).setdefault(event, [])
        elif edge["type"] == "condition":
            # Event -> State
            event = edge["from"]
            to_state = edge["to"]
            # Find all states that can lead to this event
            for from_state in transition_map:
                if event in transition_map[from_state]:
                    transition_map[from_state][event].append(to_state)
    
    # Second pass: handle any orphaned triggers (like failure cases)
    for edge in edges:
        if edge["type"] == "trigger":
            event = edge["to"]
            # If event doesn't lead anywhere, find a reasonable destination
            if not any(event in transitions for transitions in transition_map.values()):
                from_state = edge["from"]
                # Generic fallback: if no condition edge exists, assume self-transition
                transition_map.setdefault(from_state, {}).setdefault(event, [from_state])
    
    # Generate the new edge list
    fsm_edges = []
    for from_state, events in transition_map.items():
        for event, to_states in events.items():
            for to_state in to_states:
                fsm_edges.append({
                    "from": from_state,
                    "to": to_state,
                    "label": event,
                    "description": event_descriptions.get(event, node_descriptions.get(event, ""))
                })
    
    return {
        "nodes": state_nodes,
        "edges": fsm_edges
    }

# Example usage
if __name__ == "__main__":
    with open('v1-step4-enrich.json') as f:
        original_data = json.load(f)
    
    restructured = restructure_fsm(original_data)
    
    with open('restructured-refine.json', 'w') as f:
        json.dump(restructured, f, indent=2)
    
    print("Generic restructuring complete")