import json

def generate_mermaid_from_data(data):
    mermaid_code = "stateDiagram-v2\n"

    result = data["results"][0]  # Access the first result
    for state in result["states"]:
        mermaid_code += f"    [{state['name']}]\n"

    for transition in result["transitions"]:
        mermaid_code += f"    [{transition['from_state']}] --> [{transition['to_state']}]: {transition['trigger']}\n"

    return mermaid_code

with open('intermediate_results_3_783.json', 'r') as f:
    data = json.load(f)
mermaid_code = generate_mermaid_from_data(data)
print(mermaid_code)

with open("registration_flow.mermaid", "w") as f:
    f.write(mermaid_code)