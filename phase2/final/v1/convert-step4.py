import json

# Load your original JSON from file or directly assign to `data`
with open('v1-step4-enrich.json') as f:
    data = json.load(f)

nodes = data["graph"]["nodes"]
edges = data["graph"]["edges"]

# 1. Extract only state nodes
state_nodes = [node for node in nodes if node["type"] == "state"]
event_nodes = [node for node in nodes if node["type"] != "state"]  # Get non-state nodes for descriptions

# Create a lookup for event descriptions
event_descriptions = {node["id"]: node["description"] for node in event_nodes if "description" in node}

# 2. Build a lookup for event to trigger-from state
event_trigger_map = {}
for edge in edges:
    if edge["type"] == "trigger":
        event_trigger_map[edge["to"]] = edge["from"]

# 3. Now process condition edges to create transitions
fsm_edges = []
for edge in edges:
    if edge["type"] == "condition":
        event = edge["from"]
        if event in event_trigger_map:
            from_state = event_trigger_map[event]
            to_state = edge["to"]
            fsm_edges.append({
                "from": from_state,
                "to": to_state,
                "label": event,
                "description": event_descriptions.get(event, "")
            })

# 4. Create the final simplified FSM model
simplified_graph = {
    "nodes": state_nodes,
    "edges": fsm_edges
}

# 5. Save or print result
with open("restructured_graph.json", "w") as out:
    json.dump(simplified_graph, out, indent=2)

print("FSM-style graph generated as restructured_graph.json")