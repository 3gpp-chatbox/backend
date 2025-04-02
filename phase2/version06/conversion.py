import os
from dotenv import load_dotenv
from google import genai
import json

# Load the environment variables
load_dotenv()

flash_model = "gemini-2.0-flash"
pro_model = "gemini-2.0-pro-exp-02-05"

# Load the Google API Key from the .env file
load_dotenv(override=True)

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)

def generate_mermaid_from_json(section_name, json_data):
    """
    Converts a structured flow property graph (JSON) into Mermaid flowchart syntax.

    Parameters:
    - section_name (str): The name of the 3GPP procedure.
    - json_data (dict): The structured graph data containing nodes and edges.

    Returns:
    - Mermaid syntax (str)
    """

    prompt = f"""
Convert the provided JSON into **Mermaid syntax** for a 3GPP **Flow Property Graph**.

## **Graph Representation Rules**  
**Nodes** represent:  
✔ **States** (e.g., "Idle", "Registered", "Session Established")  
✔ **Events** (e.g., "UE sends Registration Request", "AMF sends Authentication Request")  

**Edges** represent:  
✔ **Triggers** (e.g., "UE sends message", "Timer expires")  
✔ **Conditions** (e.g., "If authentication successful", "If network available")  

💡 **Strict Rule**: Use **only** the provided JSON data from Step 1 and Step 2. Do **not** infer or add missing details.

Procedure Name: {section_name}

My provided JSON data:
{json.dumps(json_data, indent=2)}
"""  

    model_to_use = flash_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
        },
    )

    # Extract the text content from the response
    mermaid_syntax = response.text.strip() if hasattr(response, 'text') else str(response)

    return mermaid_syntax

def read_file_content(file_path):
    """Reads the content of a file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_mermaid_to_file(mermaid_syntax, file_path):
    """Saves the generated Mermaid syntax to a file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(mermaid_syntax)
    print(f"Mermaid syntax saved to {file_path}")

def process_json_file(input_file_path, section_name):
    """Processes the JSON content of a file and converts it into Mermaid syntax."""
    json_content = read_file_content(input_file_path)
    if json_content is None:
        return None

    # Parse JSON content into a Python dictionary
    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {input_file_path}")
        return None

    # Convert the JSON data into Mermaid flowchart syntax
    mermaid_syntax = generate_mermaid_from_json(section_name, json_data)
    return mermaid_syntax

# Example usage: Processing a JSON file
input_file_path = "v06-step3.simple.json"  # Path to your input JSON file
section_name = "Registration procedure for initial registration"  # Name of the procedure

mermaid_syntax = process_json_file(input_file_path, section_name)

if mermaid_syntax:
    save_mermaid_to_file(mermaid_syntax, "mermaid_flowchart.md")
else:
    print("Failed to generate Mermaid syntax")
