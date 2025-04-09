import json

# Load JSON data from a file
with open("v1-step11-correct-5th.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Initialize Mermaid diagram
mermaid_code = "```mermaid\ngraph TD;\n"

# Add nodes
node_map = {}  # Store node descriptions
for node in graph_data["graph"]["nodes"]:  # Directly access "nodes" from the top level
    node_id = node["id"]
    
    
    mermaid_code += f'  {node_id};\n'

# Add edges
for edge in graph_data["graph"]["edges"]:  # Directly access "edges" from the top level
    from_node = edge["from"]  # Use "from" from JSON (not "from_node")
    to_node = edge["to"]
   
    mermaid_code += f'  {from_node} --> {to_node};\n'

# Close the Mermaid code block
mermaid_code += "```\n"

# Save to file
with open("mermaid.md", "w", encoding="utf-8") as f:
    f.write(mermaid_code)

print("Mermaid diagram saved to mermaid.md!")
