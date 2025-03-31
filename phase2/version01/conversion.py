
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
    prompt = f"""
convert the provided JSON code to Mermaid syntax for a flow property graph.

I need the flow property graph to include detailed relationships between nodes. A flow property graph should highlight state transitions, events, and properties involved in the procedure. This includes metadata like conditions, actions, timers, etc.

### Here’s what I need:

**Nodes:**
- Represent entities (e.g., states, processes, timers, or decisions).
- For example: UE, AMF, T3510 timers, etc.

**Edges:**
- Represent transitions between nodes.
- Each edge should include properties such as:
  - Event triggers
  - Conditions
  - Actions or events causing the transition
  - Type of transition (sequential, conditional, retry)

**Flow Properties:**
- Include additional metadata like state changes, conditions, timers, retries, etc.

**Simplify the Nodes:**
- Each node should have the name of the process or entity (not all details).
- Detailed descriptions can be shown on the edges or tooltips.

**Clarify the Edges:**
- Each edge should contain information about the transition, conditions, retry logic, or timer usage.

### Example Output Format: (output in Mermaid syntax)

Please convert my provided JSON code to a flow property graph in the following Mermaid format.

My provided JSON code:
{text}
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
input_file_path = "v01-step3.json"  # Path to your input text file
section_name = "Registration procedure for initial registration"  # Name of the section/procedure

procedural_info = process_text_file(input_file_path, section_name)

if procedural_info:
    save_procedural_info_to_md(procedural_info, "mermaid.md")
else:
    print("Failed to extract procedural information")

