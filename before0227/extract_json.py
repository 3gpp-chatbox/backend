
 #Primary authentication and key agreement procedure


#no need description,only json
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

import os
import json
from pydantic import ValidationError

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')


def extract_procedural_info_from_text(section_name, text):
    """Extracts procedural information from the text and returns separate JSON and description outputs."""
    prompt = f"""
    Below is the chunk text of a section, read it carefully first:

    {text}

    Remember, all your analysis should be based on the chunk text, and you should not make any assumptions.
    
    This section is named: {section_name},  Identify the procedure name based on the section name and content. If the procedure name is explicitly mentioned, use it. If not, infer it from keywords related to the process described.
Extract information about the procedure and structure it into the **Flow Property Graph JSON format**.


     **flow property graph JSON representation**: Structure the procedure into a JSON format. response  not contain anything but json code,

    **IMPORTANT: Return the responses in the exact format like below:**,
<below is example for you to think of the extraction flow>: 
Selected Procedure: LTE Attach Procedure

The LTE Attach Procedure allows a User Equipment (UE) to register with

the network to receive services.

□ This procedure involves multiple steps and interactions between the UE

and the Mobility Management Entity (MME).

口

Disclaimer: This example is a simplified representation. For detailed and specific implementations, refer to the official 3GPP specifications and consult with telecommunications professionals.




Step 1: Extracting the Model from 3GPP Specification

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




Step1: Key Steps in the LTE Attach Procedure:

·

Initial UE State: UE is powered on and not attached to any network.□ Attach Request: UE sends an Attach Request message to the MME.口 Authentication: MME initiates authentication procedures.

□ Security Mode Command: MME sets up security parameters.Attach Accept: MME sends an Attach Accept message to UE.Attach Complete: UE confirms with an Attach Complete message.Final UE State: UE is attached to the network and can access services.

口

口



Step 2: Representing the Model as a Flow Property Graph

口

A property graph consists of nodes (vertices) and edges, where both can have properties. This structure is suitable for representing complex relationships and flows.

Creating Nodes and Edges:

Nodes represent States and Events.

口

Edges represent Actions and Transitions, capturing the Flow of

Execution.

□ Properties include Parameters, Conditionals, and Metadata.




Step 2: Attach procedure Nodes and Edges

State Nodes:UE_Powered_On UE_Attaching UE_Authenticating UE_Securing UE_Attached

Event Nodes:

Attach_Request_Received Authentication_Challenge Security_Mode_Command Attach_Accept_Received Attach_Complete_Sent Graph Edges:

Edges connect nodes to represent transitions triggered by

aciions or events.

Edge properties capture parameters, conditionals, and

metadatá.

(this is an json example of a procedure example):

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
          "to": "MME_Processing",
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
    return procedural_info

# Example usage: Processing section 5.5.1.2.2
section_id_to_process = "5.5.1.2.2"
db_path = "section_content_multiple_paragraphs.db"

procedural_info = process_section("5.5.1.2.2", db_path)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "data.json")
else:
    print(f"No content found for section {section_id_to_process}")



