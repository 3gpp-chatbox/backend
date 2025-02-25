
 #Primary authentication and key agreement procedure


#no need description,only json,validate the json format
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

import os
import json
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Define the Pydantic models
class Node(BaseModel):
    id: str
    type: str
    properties: Dict[str, Optional[str]] = Field(default_factory=dict)
    parameters: Optional[List[str]] = None

class Edge(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    action: Optional[str] = None
    event: Optional[str] = None
    properties: Dict[str, Optional[str]] = Field(default_factory=dict)

class ProcedureGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def preprocess_json_data(json_data):
    """Sanitize and correct the JSON data before validation."""
    for edge in json_data.get('edges', []):
        # Ensure parameters is a list of strings in the 'properties' field
        if "parameters" in edge.get("properties", {}):
            edge["properties"]["parameters"] = [
                str(param) for param in edge["properties"]["parameters"]
            ]
        # Ensure any missing fields like 'event' or 'action' are handled
        if "action" not in edge:
            edge["action"] = None
        if "event" not in edge:
            edge["event"] = None
    return json_data

def extract_procedural_info_from_text(section_name, text):
    """Extracts procedural information from the text and returns separate JSON and description outputs."""
    prompt = f"""
    Below is the chunk text of a section, read it carefully first:

    {text}

    Remember, all your analysis should be based on the chunk text, and you should not make any assumptions.
    
    This section is named: {section_name}, it is also the procedure name that this section is about, analyze text and focus on that procedure,extract the procedure information and use below pattern to mapping it:
    

     **flow property graph JSON representation**: Structure the procedure into a JSON format.

    **IMPORTANT: Return the responses in the exact format like below:**,comment out  ```json" and  ``` at the beginning and end of your response !!makesure your response start with left curly bracket "{" and end with right curly bracket "}"
  
     {{
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
          "to": "Attach_Request_Received",
          "event": "Attach_Request_Received",
          "properties": {{}}
        }}
      ]
    }}



    """

    response = model.generate_content(prompt).text.strip()
    return response



def retrieve_chunks_from_db(section_id, db_path="section_content_multiple_paragraphs.db"):
    """Retrieves content chunks and section name for a specific section_id from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT section_name, content_chunk FROM content WHERE section_id = ? ORDER BY chunk_id''', (section_id,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        return None, None

    section_name = results[0][0]
    chunks = [result[1] for result in results]
    full_text = "\n\n".join(chunks)

    return section_name, full_text

def save_procedural_info_to_json(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

def process_section(section_id, db_path="section_content_multiple_paragraphs.db"):
    section_name, chunk_text = retrieve_chunks_from_db(section_id, db_path)
    if section_name is None:
        return None #handle no result.
    procedural_info = extract_procedural_info_from_text(section_name, chunk_text) #pass section_name.

        # Preprocess the JSON data before validation
    try:
        # Attempt to load the response as JSON
        json_data = json.loads(procedural_info)
        
        # Preprocess to ensure the JSON structure is correct
        json_data = preprocess_json_data(json_data)
        
        # Return the preprocessed data to be saved or validated
        return json_data
        
    except json.JSONDecodeError:
        print("❌ Failed to decode the JSON data from AI response.")
        return None


    return procedural_info


def validate_json_file(file_path):
    """Checks if the JSON file exists and validates it using Pydantic."""
    if os.path.exists(file_path):
        print(f"✅ JSON file found: {file_path}")
        
        # Open the JSON file and attempt to load and validate it
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)

                     # Preprocess the data to ensure it's in the correct format
                json_data = preprocess_json_data(json_data)
                
                # Validate using Pydantic models
                validated_data = ProcedureGraph(**json_data)  # Validate with the Pydantic model

                # If validation passes, print success message
                print(f"✅ JSON validation successful for {file_path}")
        
        except json.JSONDecodeError:
            print(f"❌ Failed to decode JSON in file: {file_path}")
        except ValidationError as e:
            print(f"❌ Pydantic validation failed: {e}")
    else:
        print(f"❌ JSON file not found: {file_path}")


# Example usage: Processing section 5.5.1.2.2
section_id_to_process = "5.5.1.2.4"
db_path = "section_content_multiple_paragraphs.db"



procedural_info = process_section(section_id_to_process, db_path)

if procedural_info:
    json_file_path = "0225-json-test3.json"
    save_procedural_info_to_json(json.dumps(procedural_info), json_file_path)
    validate_json_file(json_file_path)
else:
    print(f"No content found for section {section_id_to_process}")







