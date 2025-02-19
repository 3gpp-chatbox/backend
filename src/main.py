# src/main.py
import os
import getpass
from dotenv import load_dotenv
from google import genai
from docling.document_converter import DocumentConverter
import lib.doc_converter as doc_converter
import lib.doc_processor as doc_processor


flash_model = "gemini-2.0-flash"
pro_model = "gemini-2.0-pro-exp-02-05"

# Load the Google API Key from the .env file
load_dotenv(override=True)

# Get API key from environment
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

client = genai.Client(api_key=api_key)

# ## call the converter function to convert docx to markdown
result = doc_converter.convert_to_markdown("data/stripped/24501-j11.docx")

def token_counter(client, model, contents):
    """Count the number of tokens in the given contents"""
    response = client.models.count_tokens(
        model=model,
        contents=contents
    )
    
    return response


# chat = client.chats.create(model=pro_model)

# response = chat.send_message(
#     message='Tell me a story in 100 words')




file = client.files.upload(file='data/stripped/24501-j11.txt')

prompt = f"""
The file uploaded is extracted from the 3GPP specification 24.501. Please analyze the content and provide a structured representation of the procedural flow information.

Extract the procedural flow information from the above section and return it in a structured format.below is an example for you to thinking and help you to understand the format:

The LTE Attach Procedure allows a User Equipment (UE) to register with

        the network to receive services.

        This procedure involves multiple steps and interactions between the UE

        and the Mobility Management Entity (MME).


Disclaimer: This example is a simplified representation. For detailed and specific implementations, refer to the official 3GPP specifications and consult with telecommunications professionals.


Step 1: Extracting the Model from 3GPP Specification

Core Components to Identify

States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or

IDs.




Step1: Key Steps in the procedure:


Initial UE State: UE is powered on and not attached to any network.Attach Request: UE sends an Attach Request message to the MME.Authentication: MME initiates authentication procedures.

Security Mode Command: MME sets up security parameters.Attach Accept: MME sends an Attach Accept message to UE.Attach Complete: UE confirms with an Attach Complete message.Final UE State: UE is attached to the network and can access services.

Step 2: Representing the Model as a Flow Property Graph


A property graph consists of nodes (vertices) and edges, where both can have properties. This structure is suitable for representing complex relationships and flows.

Creating Nodes and Edges:

Nodes represent States and Events.


Edges represent Actions and Transitions, capturing the Flow of

Execution.

Properties include Parameters, Conditionals, and Metadata.




Step 2: Attach procedure Nodes and Edges

State Nodes:UE_Powered_On UE_Attaching UE_Authenticating UE_Securing UE_Attached

Event Nodes:

Attach_Request_Received Authentication_Challenge Security_Mode_Command Attach_Accept_Received Attach_Complete_Sent Graph Edges:

Edges connect nodes to represent transitions triggered by

aciions or events.

Edge properties capture parameters, conditionals, and

metadata

step 2: JSON representation of property graph
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



Based on the above, analyze and extract the information from the given text and provide a structured representation of the procedural flow information.
""" 

response = client.models.generate_content(
    model = pro_model,
    contents = [ prompt,file]
)




# doc = doc_processor.load_document("data/24501-j11.docx")
# doc_processor.remove_paragraphs(doc, ["annex", "appendix", "abbreviations", "scope", "references", "foreword"])
