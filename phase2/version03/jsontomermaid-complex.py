import json

# Load JSON data from a file
with open("v03-step3-complex-newmodel.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    graph_data = data["graph"]  # Access the 'graph' key

# Initialize Mermaid diagram
mermaid_code = "```mermaid\ngraph TD;\n"

# Add nodes
node_map = {}  # Store node descriptions
for node in graph_data["nodes"]:
    node_id = node["id"]
    description = node.get("description", node_id)
    node_map[node_id] = description
    mermaid_code += f'  {node_id}["{description}"];\n'

# Add edges
for edge in graph_data["edges"]:
    from_node = edge["from"]
    to_node = edge["to"]
    label = ""

    # Try getting a label from possible properties
    props = edge.get("properties", {})
    for key in ["trigger", "condition", "error_type"]:
        if key in props:
            label = props[key]
            break  # Use the first matching property as label

    mermaid_code += f'  {from_node} -->|{label}| {to_node};\n'

# Close the Mermaid code block
mermaid_code += "```\n"

# Save to file
with open("mermaid-complex-newmodel.md", "w", encoding="utf-8") as f:
    f.write(mermaid_code)

print("Mermaid diagram saved to mermaid-complexx.md!")
