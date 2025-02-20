import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Load from environment variable
  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to extract procedural flow from the chunk of text using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
    the following section is registration procedure for initial registration:

    {text}

    i want you to extract the procedural flow information from the above section and return it in a structured format.below is an example for you to thinking and help you to understand the format:

    The LTE Attach Procedure allows a User Equipment (UE) to register with

          the network to receive services.

         □ This procedure involves multiple steps and interactions between the UE

        and the Mobility Management Entity (MME).



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

step2 JSON representation of property graph
(two screenshots content shows below) 
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




plaintext

[UE_Powered_On] --(Action: Send_Attach_Request)-->[UE_Attaching] --(Event: Attach_Request_Received)-->[MME_Processing] --(Action: Initiate_Authentication)-->[UE_Authenticating] --(Event: Authentication_Challenge)-->[UE_Securing] --(Action: Complete_Authentication)-->

[MME_Securing] --(Event: Security_Mode_Command)-->

[UE_Attached] --(Action: Send_Attach_Complete)-->





Step 3: Incorporating Conditionals and Parameters

Conditionals:

Decisions based on IMSI validation, security capabilities, etc.

Represented as properties or separate nodes in the graph.

Example Conditional:

If the authentication succeeds, proceed to security mode setup.

If it fails, reject the attach request.

Parameters and Metadata:

Parameters like !MSL Temporary.Mobile Subscriber Identity (fMSI), Tracking Area Identity (TAI).

Metadata such as timestamps, message identifiers.

(below is screenshot content)

Graph Representation:

plaintext

Copy code

[UE_Authenticating] --(Condition: Auth_Success)--> [UE_Securing]

[UE_Authenticating] --(Condition: Auth_Failure)-->

[Attach_Rejected]



    Based on the above, analyze and extract the information from the given chunk.
    """ 

    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to retrieve document chunks from the database
def retrieve_chunks_from_db(start_id, end_id, db_path="path_to_your_db.sqlite"):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve chunks within the given ID range
    cursor.execute('''SELECT chunk_text FROM document_chunks WHERE chunk_id BETWEEN ? AND ?''', (start_id, end_id))

    # Fetch all matching chunks
    chunks = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Join the chunks together into one large text block
    full_text = "\n".join(chunk[0] for chunk in chunks)

    return full_text


# Function to save extracted procedural info as plain text
def save_procedural_info_to_txt(procedural_info, file_path):
    with open(file_path, "w") as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

# Main function to process the document section
def process_section(start_id, end_id, db_path="path_to_your_db.sqlite"):
    # Step 1: Retrieve the chunks for the desired section (e.g., 5.5.1.2 to 5.5.1.3)
    chunk_text = retrieve_chunks_from_db(start_id, end_id, db_path)

    # Step 2: Extract procedural flow from the retrieved chunks
    procedural_info = extract_procedural_info_from_text(chunk_text)

    return procedural_info

# Example usage: Processing section 5.5.1.2 to 5.5.1.3 (IDs 625 to 765 in your database)
start_chunk_id = 625  # Start chunk ID (example)
end_chunk_id = 765    # End chunk ID (example)
db_path = "path_to_your_db.sqlite"  # Path to your SQLite database

# Process the section
procedural_info = process_section(625, 765, 'document_chunks.db')

# Print the extracted procedural info
# print("Extracted Procedural Information:\n")
# print(procedural_info)

save_procedural_info_to_txt(procedural_info, "output2.txt")  # For plain text