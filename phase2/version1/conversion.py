
import os
from dotenv import load_dotenv
from google import genai
import json

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

def extract_procedural_info_from_text(section_name, text):
    prompt = f""" {section_name}  convert my provided json code to mermaid syntax.
I am referring to a flow property graph rather than a standard flowchart, which should include more specific details about the relationships between nodes. A flow property graph often highlights the state transitions between entities, events, and properties involved in a procedure, and it includes more metadata (like conditions, actions, timers, etc.) in the transitions (edges).

Let’s clarify the specific structure I need for a flow property graph:

Nodes will represent entities (such as states, processes, timers, or decisions).

Edges will represent transitions between those nodes, and each edge will have properties that describe the conditions, actions, or events triggering the transitions.

For a flow property graph, I need to represent:

Entities/States (Nodes): Representing states, processes, and timers (such as UE, AMF, timers like T3510, etc.).

Transitions (Edges): The relationships between these entities, including event triggers, conditions, and actions on the edges.

Flow Properties: Include metadata like the state change, conditions, or timers in the edge itself.

Simplify the Nodes: Each node should ideally contain the name of the process, not all its details. The detailed description can be shown on the edges or with tooltips if necessary.

Clarify the Edges: The edges should contain information such as the condition, whether it’s a sequential or conditional transition, or any associated timers.

My provided JSON code: 

{text}"""

    
    model_to_use = flash_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
        },
    )

    # Extract the text content from the response
    procedural_info = response.text.strip() if hasattr(response, 'text') else str(response)

    return procedural_info

def read_text_file(file_path):
    """Reads content from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_procedural_info_to_md(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

def process_text_file(input_file_path, section_name):
    """Processes content from a text file instead of database."""
    text_content = read_text_file(input_file_path)
    if text_content is None:
        return None
        
    procedural_info = extract_procedural_info_from_text(section_name, text_content)
    return procedural_info

# Example usage: Processing a text file
input_file_path = "step3.json"  # Path to your input text file
section_name = "Registration procedure for initial registration"  # Name of the section/procedure

procedural_info = process_text_file(input_file_path, section_name)

if procedural_info:
    save_procedural_info_to_md(procedural_info, "mermaid.md")
else:
    print("Failed to extract procedural information")

