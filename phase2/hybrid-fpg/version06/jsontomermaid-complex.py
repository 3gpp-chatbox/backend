import json

# Load JSON data from a file
with open("v06-step3-complex.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Initialize Mermaid diagram
mermaid_code = "```mermaid\ngraph TD;\n"

# Add nodes
node_map = {}  # Store node descriptions and conditions
for node in graph_data["nodes"]:
    node_id = node["id"]
    name = node.get("name", f"Node_{node_id}") # use node id as name if name field is missing.
    description = node.get("description", name) # use name if description field is missing.
    condition = node.get("condition", "")  # Get condition if it exists
    if condition:
        description += f" ({condition})"  # Append condition to description
    node_map[node_id] = description
    mermaid_code += f'    {node_id}["{description}"];\n'

# Add edges
for edge in graph_data["edges"]:
    from_node = edge["from"]
    to_node = edge["to"]
    edge_label = edge.get("description", edge.get("relation", ""))

    # If the source node is a decision, add condition to edge label
    source_node = next(
        (n for n in graph_data["nodes"] if n["id"] == from_node), None
    )
    if source_node and source_node["type"] == "decision":
        condition = edge.get("condition", "")
        if condition:
            edge_label = condition

    mermaid_code += f'    {from_node} -->|{edge_label}| {to_node};\n'

# Close the Mermaid code block
mermaid_code += "```\n"

# Save to file
with open("mermaid-complex-flashmodel.md", "w", encoding="utf-8") as f:
    f.write(mermaid_code)

print("Mermaid diagram saved to mermaid-complex.md!")