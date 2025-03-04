import sqlite3
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import json
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Optional


# Configure API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')
DB_NAME = 'section_content_0228.db'



# Define the structure of nodes in the graph
class Node(BaseModel):
    id: str
    type: str
    properties: Optional[Dict[str, str]] = {}  # Flexible properties (empty dictionary is acceptable)
    parameters: Optional[List[str]] = []  # Flexible parameters, can be empty

# Define the structure of edges in the graph
class Edge(BaseModel):
    from_node: str
    to_node: str
    action: str
    properties: Optional[Dict[str, str]] = {}  # Flexible properties (empty dictionary is acceptable)

# Define the top-level structure for the graph
class GraphModel(BaseModel):
    nodes: List[Node]  # List of nodes
    edges: List[Edge]  # List of edges




# Function to query sections table and locate the relevant section for procedure info
def find_section_with_procedure_info(procedure_query):
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query the sections table to get all section names and IDs
    cursor.execute("SELECT section_id, section_name FROM sections")
    sections = cursor.fetchall()
    
    # Prepare a prompt with the sections table data for LLM
    sections_text = "\n".join([f"Section ID: {sec[0]}, Section Name: {sec[1]}" for sec in sections])
    
    # Create the prompt for LLM
    prompt = f"""
    Here are the section names and IDs:

    {sections_text}

    I need help finding the specific section that is only about the procedure  "{procedure_query}".
    Please only return the section name that contains this procedure information.
    """

    # Ask the LLM to find the correct section
    response = model.generate_content(prompt).text.strip()
    
    # Close the connection
    conn.close()
    
    return response

# Function to query content of the selected section using section name
def get_section_content_by_name(section_name):
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query the content table using section name
    cursor.execute('SELECT content_chunk FROM content WHERE section_name = ?', (section_name,))
    content_chunk = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    return content_chunk[0] if content_chunk else None

# Function to extract procedure flow from content using LLM
def extract_procedure_flow(content, procedure_query):
    # Create the prompt for LLM to extract procedure flow
    prompt = f"""
    Here is the content of the section that is only about the procedure "{procedure_query}":

    {content}
 Remember, all your analysis should be based on the chunk text i provided, and you should not make any assumptions.
    

 analyze the text i provided,focus on that procedure,extract the information about procedure.Structure the procedure into a  **flow property graph JSON representation** using SON format.
    response  not contain anything but json code,

    **IMPORTANT: Return the responses in the exact format like below:**,
    below is example:
Core Components to Identify

□ States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or

IDs.

(this is an json example of a procedure example):

     {{
      "procedure_name": "procedure name here ",
  "description": " description here  ",
 
      "nodes": [
        {{
          "id": "UE_Powered_On",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "UE_Attaching",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "Attach_Request_Received",
          "type": "event",
          "properties": {{
            "message_type": "Attach Request"
          }},
          "parameters": ["IMSI", "TAI"]
        }}
      ],
      "edges": [
        {{
          "from": "UE_Powered_On",
          "to": "UE_Attaching",
          "action": "Send_Attach_Request",
          "properties": {{
            "parameters": ["IMSI", "TAI"],
            "metadata": {{
              "timestamp": "T0"
            }}
          }}
        }},
        {{
          "from": "UE_Attaching",
          "to": "MME_Processing",
          "event": "Attach_Request_Received",
          "properties": {{}}
        }}
      ]
    }}
    """
    
    # Ask the LLM to generate the flow property graph
    
    response = model.generate_content(prompt).text.strip()
    return response


def save_procedural_info_to_json(response, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(response)
    print(f"Procedural info saved to {file_path}")



def clean_json(file_path):
    """Remove Markdown-style triple backticks (```json ... ```) from the JSON file."""
    try:
        with open(file_path, "r") as f:
            raw_data = f.read()

        # Remove Markdown code block indicators (```json and ```)
        cleaned_data = raw_data.strip().replace("```json", "").replace("```", "").strip()

        # Overwrite the file with cleaned JSON
        with open(file_path, "w") as f:
            f.write(cleaned_data)

    except Exception as e:
        print(f"Error cleaning JSON: {e}")




def validate_json(file_path: str):
    """Validate JSON file after cleaning."""
    clean_json(file_path)  # Clean JSON before validation

    if not os.path.exists(file_path):
        print("Error: JSON file not found.")
        return

    try:
        # Open the cleaned JSON file and parse it
        with open(file_path, "r") as f:
            data = json.load(f)  # Try to load the cleaned JSON from file

        # Validate the cleaned JSON with Pydantic
        graph = GraphModel(**data)  # Use data read from file for Pydantic validation
        print("VALID JSON: Pydantic validation passed")
    
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: JSON decode error - {e}")
    except ValidationError as e:
        print(f"INVALID JSON: Pydantic validation error - {e}")






# Main function to execute the workflow
def main():
    # Step 1: Ask the LLM to find the section with procedure info
    procedure_query = "Initial registration initiation"
    section_name = find_section_with_procedure_info(procedure_query)
    
    print(f"Found Section: {section_name}")
    
    # Step 2: Get the content of the identified section by name
    section_content = get_section_content_by_name(section_name)
    
    if section_content:
        # Step 3: Ask the LLM to extract procedure flow from the section content
        response = extract_procedure_flow(section_content, procedure_query)
        
        save_procedural_info_to_json(response, "data.json")
        clean_json("data.json")
        validate_json("data.json")
        
        print(f"Flow graph saved to data.json")
    else:
        print("Section content not found.")

# Run the main function
if __name__ == "__main__":
    main()
