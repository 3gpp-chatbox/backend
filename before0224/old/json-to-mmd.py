import json

# Your JSON data
json_data = '''
{
  "nodes": [
    {"id": "5GMM-DEREGISTERED", "type": "state"},
    {"id": "REGISTRATION_REQUEST_SENT", "type": "event"},
    {"id": "AMF_PROCESSING", "type": "state"},
    {"id": "REGISTRATION_ACCEPTED", "type": "event"},
    {"id": "5GMM-REGISTERED", "type": "state"},
    {"id": "REGISTRATION_REJECTED", "type": "event"},
    {"id": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION", "type": "state"}
  ],
  "edges": [
    {"from": "5GMM-DEREGISTERED", "to": "REGISTRATION_REQUEST_SENT", "action": "Send_REGISTRATION_REQUEST", "properties": {"registration_type": "initial"}},
    {"from": "REGISTRATION_REQUEST_SENT", "to": "AMF_PROCESSING", "event": "REGISTRATION_REQUEST_RECEIVED"},
    {"from": "AMF_PROCESSING", "to": "5GMM-REGISTERED", "action": "Send_REGISTRATION_ACCEPT", "condition": "Registration_Request_Accepted"},
    {"from": "AMF_PROCESSING", "to": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION", "action": "Send_REGISTRATION_REJECT", "condition": "Registration_Request_Rejected"},
    {"from": "5GMM-DEREGISTERED.ATTEMPTING-REGISTRATION", "to": "REGISTRATION_REQUEST_SENT", "action": "Retry_REGISTRATION_REQUEST", "condition": "Retry_Count < 5"}
  ]
}
'''

# Parse JSON
data = json.loads(json_data)

# Generate Mermaid syntax
mermaid_output = "stateDiagram-v2\n"

# Add nodes (states)
for node in data["nodes"]:
    mermaid_output += f"    {node['id']}\n"

# Add edges (transitions)
for edge in data["edges"]:
    from_node = edge["from"]
    to_node = edge["to"]
    action = edge.get("action", "")
    condition = edge.get("condition", "")
    event = edge.get("event", "")

    # Build the transition label
    label = []
    if action:
        label.append(f"{action}")
    if condition:
        label.append(f" : {condition}")
    if event:
        label.append(f" : {event}")

    mermaid_output += f"    {from_node} --> {to_node}"
    if label:
        mermaid_output += f" : {''.join(label)}"
    mermaid_output += "\n"

# Print the Mermaid output
print(mermaid_output)