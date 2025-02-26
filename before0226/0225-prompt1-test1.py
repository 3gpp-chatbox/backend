
 #Primary authentication and key agreement procedure

import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

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

def extract_procedural_info_from_text(section_name, text):
    """Extracts procedural information from the text and returns separate JSON and description outputs."""
    prompt = f"""
    Below is the chunk text of a section, read it carefully first:

    {text}

    Remember, all your analysis should be based on the chunk text, and you should not make any assumptions.
    
    This section is named: {section_name}, it is also the procedure name that this section is about, analyze text and focus on that procedure,extract the procedure information and use below pattern to mapping it:
    
    1. **Description, key information, and procedure name**: Provide a textual explanation.
    2. **flow property graph JSON representation**: Structure the procedure into a JSON format.

    **IMPORTANT: Return the responses in the exact format like below:**
    
    --START OF DESCRIPTION--
  **Procedure Name:** Initial Registration Initiation

**Description:** The procedure is initiated by the UE when in the 5GMM-DEREGISTERED state under various conditions. It involves the UE sending a REGISTRATION REQUEST message to the AMF and handling different IEs based on UE capabilities, network conditions, and service requirements.

**Key Information:**

*   **Initial State:** 5GMM-DEREGISTERED
*   **Trigger:**  One of the following conditions is met: initial registration for 5GS services, emergency services, SMS over NAS, mobility from GERAN/UTRAN to NG-RAN, initial registration for onboarding/disaster roaming services, or resuming normal services.
*   **Message Sent:** REGISTRATION REQUEST
*   **Timer Actions:** Start timer T3510, Stop timer T3502 (if running), Stop timer T3511 (if running).
*   **Key Information Elements (IEs) Handling:** 5GS mobile identity, UE status, last visited registered TAI, 5GS update type, MICO indication, Requested DRX parameters, Requested NB-N1 mode DRX parameters, Requested extended DRX parameters, LADN indication, requested NSSAI, 5GMM capability, Payload container type, NAS message container, Additional information requested, Requested WUS assistance information, Requested PEIPS assistance information, UE determined PLMN with disaster condition IE, Service-level-AA container IE, AUN3 indication IE, N5GC indication IE
    --END OF DESCRIPTION--

    --START OF JSON--
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
    --END OF JSON--
    """

    response = model.generate_content(prompt).text.strip()
    return response

def process_ai_response(response):
    """Splits AI response into separate description and JSON outputs."""
    description_part = ""
    json_part = ""

    # Extract description
    if "--START OF DESCRIPTION--" in response and "--END OF DESCRIPTION--" in response:
        description_part = response.split("--START OF DESCRIPTION--")[1].split("--END OF DESCRIPTION--")[0].strip()

    # Extract JSON
    if "--START OF JSON--" in response and "--END OF JSON--" in response:
        json_part = response.split("--START OF JSON--")[1].split("--END OF JSON--")[0].strip()

    return description_part, json_part

def save_to_file(content, file_path):
    """Saves content to a text file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(content)
    print(f"Saved to {file_path}")

def process_section(section_id, db_path="section_content_multiple_paragraphs.db"):
    """Retrieves section text, processes it with AI, and saves results separately."""
    section_name, chunk_text = retrieve_chunks_from_db(section_id, db_path)
    if section_name is None:
        return None

    ai_response = extract_procedural_info_from_text(section_name, chunk_text)
    description, json_output = process_ai_response(ai_response)

    # Save separately
    if description:
        save_to_file(description, "0225-description.txt")

    if json_output:
        save_to_file(json_output, "0225-json.txt")

# Example usage
section_id_to_process = "5.5.1.2.2"
process_section(section_id_to_process)
