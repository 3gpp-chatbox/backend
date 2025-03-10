
 #Primary authentication and key agreement procedure

import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Load from environment variable

model = genai.GenerativeModel('gemini-2.0-flash')



# Function to extract procedural flow from the chunk of text using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
    below is the thunk text of a section, read them carefully first:

    {text}

 remember, all you analysis and extract should be based on the thunk text, and you should not make any assumptions. 
this secion is mainly about one procedure, analyze text  and fine that main procedure, and then focus on that procedure,extract the procedure information  and use below pattern to mapping it (below is an example) finally,also Return key information and description .
 below is that example: 


Extracting the Model from 3GPP Specification

Core Components to Identify

□ States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or IDs.
JSON representation of property graph

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

    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()

import sqlite3

def retrieve_chunks_from_db(section_id, db_path="section_content_chunked_id.db"):
    """Retrieves content chunks for a specific section_id from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve chunks for the given section_id, ordered by chunk_id
    cursor.execute('''SELECT content_chunk FROM content WHERE section_id = ? ORDER BY chunk_id''', (section_id,))

    chunks = cursor.fetchall()
    conn.close()

    full_text = "\n\n".join(chunk[0] for chunk in chunks)  # Join with double newlines

    return full_text

def save_procedural_info_to_txt(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file: #added encoding.
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

def process_section(section_id, db_path="section_content_chunked_id.db"):
    chunk_text = retrieve_chunks_from_db(section_id, db_path)
    procedural_info = extract_procedural_info_from_text(chunk_text) #assuming extract_procedural_info_from_text is defined elsewhere.
    return procedural_info

# Example usage: Processing section 5.5.1.2.2
section_id_to_process = "5.5.1.2.2"
db_path = "section_content_chunked_id.db"

procedural_info = process_section(section_id_to_process, db_path)

save_procedural_info_to_txt(procedural_info, "procedure-5-5-1-2-2.txt")