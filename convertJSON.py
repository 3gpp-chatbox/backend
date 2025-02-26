import json

# Read the JSON file
try:
    with open('processed_data/registration_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Start Mermaid flowchart definition
    mermaid_code = "graph TD;\n"
    
    # Track unique items to avoid duplicates
    states_added = set()
    elements_added = set()
    transitions_added = set()
    relationships_added = set()

    # Process each result in the results array
    if 'results' in data:
        for result in data['results']:
            # Add States as Nodes
            if 'states' in result:
                for state in result['states']:
                    state_id = state["name"].replace(" ", "_")
                    if state_id not in states_added:
                        mermaid_code += f'  {state_id}["{state["name"]} ({state["type"]})"];\n'
                        states_added.add(state_id)

            # Add Network Elements as Nodes
            if 'network_elements' in result:
                for element in result['network_elements']:
                    element_id = element["name"].replace(" ", "_")
                    if element_id not in elements_added:
                        mermaid_code += f'  {element_id}["{element["name"]} ({element["type"]})"];\n'
                        elements_added.add(element_id)

            # Add Transitions
            if 'transitions' in result:
                for transition in result['transitions']:
                    from_state = transition["from_state"].replace(" ", "_")
                    to_state = transition["to_state"].replace(" ", "_")
                    transition_id = f"{from_state}->{to_state}"
                    if transition_id not in transitions_added:
                        mermaid_code += f'  {from_state} -->|{transition["trigger"]}| {to_state};\n'
                        transitions_added.add(transition_id)

            # Add Network Element Relationships
            if 'network_element_relationships' in result:
                for relationship in result['network_element_relationships']:
                    elem1 = relationship["element1"].replace(" ", "_")
                    elem2 = relationship["element2"].replace(" ", "_")
                    rel_id = f"{elem1}->{elem2}"
                    if rel_id not in relationships_added:
                        mermaid_code += f'  {elem1} -->|{relationship["relationship"]}| {elem2};\n'
                        relationships_added.add(rel_id)

        # Save as .md file
        with open("flow_diagram.md", "w", encoding='utf-8') as file:
            file.write("```mermaid\n" + mermaid_code + "```\n")

        print("✅ Mermaid flow diagram saved in flow_diagram.md")
        print(f"Added {len(states_added)} states, {len(elements_added)} elements, "
              f"{len(transitions_added)} transitions, and {len(relationships_added)} relationships.")

    else:
        print("No 'results' field found in the JSON data")

except FileNotFoundError:
    print("registration_analysis.json file not found in processed_data directory")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
