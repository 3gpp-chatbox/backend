
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
    
    This section is named: {section_name},  this section is about a procedure(section name may be key word of the procedure or procedure name), find the procedure name and analyze and focus on that procedure,extract the procedure information and use below pattern to mapping it:
    

     **flow property graph JSON representation**: Structure the procedure into a JSON format.  comment out  ```json" and  ``` at the beginning and end of your response !! make sure your response start with left curly bracket "{" and end with right curly bracket "}",response  not contain anything but json code,

    **IMPORTANT: Return the responses in the exact format like below:**,
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
    return procedural_info

# Example usage: Processing section 5.5.1.2.2
section_id_to_process = "5.5.1.2.2"
db_path = "section_content_multiple_paragraphs.db"

procedural_info = process_section("5.5.1.2.3", db_path)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "data.json")
else:
    print(f"No content found for section {section_id_to_process}")



