import json
import re

# Load your JSON
with open("step3-enrich.json", "r") as f:
    transitions = json.load(f)

def format_node(name):
    """Convert state name to Mermaid-safe identifier (no quotes)."""
    return re.sub(r'\W+', '_', name)

def sanitize_label(text):
    """Replace double quotes with single quotes and sanitize text."""
    if not text:
        return ""
    # Replacing double quotes (") with single quotes (') and sanitizing newlines
    return text.replace('"', "'").replace("\n", " ").strip()

def make_edge_label(event, condition, action):
    parts = []
    if event:
        parts.append(f"event: {event}")
    if condition:
        parts.append(f"condition: {condition}")
    if action:
        parts.append(f"action: {action}")
    return "\\n".join(sanitize_label(p) for p in parts)

# Build Mermaid graph
lines = ["flowchart TD"]
for t in transitions:
    from_node = format_node(t["from"])
    to_node = format_node(t["to"])
    label = make_edge_label(t.get("event"), t.get("condition"), t.get("action"))
    lines.append(f"{from_node} -->|\"{label}\"| {to_node}")

# Save to file
with open("mermaid_output.mmd", "w") as f:
    f.write("\n".join(lines))

print("✅ Mermaid graph written to mermaid_output.mmd")
