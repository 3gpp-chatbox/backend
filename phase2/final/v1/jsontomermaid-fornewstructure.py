import json

# Load restructured JSON
with open("restructured-refine.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Initialize Mermaid diagram
mermaid_code = "```mermaid\ngraph TD;\n"

# Add state nodes
for node in graph_data["nodes"]:
    node_id = node["id"]
    mermaid_code += f'  {node_id};\n'

# Add labeled transitions (edges)
for edge in graph_data["edges"]:
    from_node = edge["from"]
    to_node = edge["to"]
    label = edge.get("label", "")
    mermaid_code += f'  {from_node} -- "{label}" --> {to_node};\n'

# Close Mermaid block
mermaid_code += "```\n"

# Save to file
with open("mermaid-newstructure-refine.md", "w", encoding="utf-8") as f:
    f.write(mermaid_code)

print("Mermaid diagram saved to mermaid-newstructure.md!")
