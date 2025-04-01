
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
    def convert_json_to_mermaid(section_name, json_data):
    """
    Converts structured flow property graph JSON into Mermaid flowchart syntax.

    Parameters:
    - section_name (str): The name of the 3GPP procedure.
    - json_data (dict): The structured graph data containing nodes and edges.

    Returns:
    - Mermaid syntax (str)
    """

    prompt = f"""
Convert the provided JSON into **Mermaid syntax** for a 3GPP **Flow Property Graph**.

---

## **🔹 Flow Property Graph Structure**
- **Nodes represent execution steps, decisions, timers, and state changes.**
- **Entities (UE, AMF, etc.) are properties within nodes, NOT separate nodes.**
- **Edges define execution flow, dependencies, and property modifications.**

---

## **🔹 Conversion Rules**
🔹 **Nodes:**  
   - **Process Steps** → Rectangular (`[Step Name]`)  
   - **Decisions** → Diamond (`{{Decision Condition}}`)  
   - **Timers** → Cylindrical (`([Timer Name])`), with start/stop/reset actions  
   - **State Changes** → Parallelogram (`[/State Change/]`)  
   - **Start/End** → Circular (`((Start/End))`)  

🔹 **Edges (Arrows):**  
   - **Sequential Execution** → `A --> B`  
   - **Conditional Flow** → `A --|Condition|--> B`  
   - **Retry on Failure** → `A --|Retry Condition|--> B`  
   - **Dependency (Step must wait for another)** → `A --|depends on|--> B`  
   - **Modifying (Message/state change affects another step)** → `A --|modifies|--> B`  

🔹 **Timers:**  
   - `([T3510])` represents the timer.  
   - `A -->|Starts Timer| ([T3510])` shows timer activation.  
   - `([T3510]) --|Expires|--> C` represents expiry leading to an event.  

---

## **🔹 Example Mermaid Output**
```mermaid
graph TD;
  A((Start)) -->|UE sends REGISTRATION REQUEST| B[Process: Send Registration Request]
  B -->|Starts Timer| C([T3510])
  C --|Expires|--> D{{Retry or Fail?}}
  D --|Retry|--> B
  D --|Fail|--> E[Rejection]
  E -->((End))



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

