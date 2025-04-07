import json

def read_json_file(file_path):
    """Reads content from a JSON file and returns the parsed JSON object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to remove "description" from states and actions
def remove_description(data):
    # Remove 'description' from states
    for state in data.get('states', []):
        if 'description' in state:
            del state['description']
    
    # Remove 'description' from actions (if necessary)
    for action in data.get('actions', []):
        if 'description' in action:
            del action['description']
    
    # Return the modified data
    return data

# Load Step 1 result from file
step1_result = read_json_file("v1-step1.json")

# Remove "description" from Step 1 result
if step1_result:
    modified_step1 = remove_description(step1_result)


    # Optionally, save to a new file
    with open('v1-step1-nodescription.json', 'w') as f:
        json.dump(modified_step1, f, indent=2)
