# src/main.py
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
import json
from src.lib.extract_content_data import generate_markdown

flash_model = "gemini-2.0-flash"
pro_model = "gemini-2.0-pro-exp-02-05"
old_pro_model = "gemini-1.5-pro"

# Load the Google API Key from the .env file
load_dotenv(override=True)

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)

# Read the table of contents from the document toc.md
toc_file_path = "toc_mini.md"


class Response(BaseModel):
    sections: list[str]


with open(toc_file_path, "r") as f:
    toc = f.read()


def get_relevant_sections(table_of_contents: str):
    prompt2 = f"""
                ROLE: You are an expert in 3GPP specifications.
                TASK: Analyze the table of contents of 3GPP TS 24.501 provided below and identify the sections that contain information necessary to design a flow diagram of the initial registration procedure. In this flow diagram:
                Nodes represent 5GMM states (e.g., 5GMM-DEREGISTERED, 5GMM-REGISTERED-INITIATED) and events (e.g., message sending, procedure initiation).

                Edges represent actions (e.g., sending a message) and transitions (e.g., state changes) between nodes.

                Properties include parameters (e.g., message contents), conditions (e.g., success or failure criteria), and metadata (e.g., timers, abnormal cases).

                Instructions:
                Return sections that specifically detail the initial registration procedure, its associated states, events, actions, transitions, and properties.

                If a section has subsections and all are relevant to the flow diagram’s components, return the parent section only.

                Always return the full section name exactly as written in the table of contents.

                Exclude sections that are too general (e.g., covering multiple procedures) unless they contain specific subsections unique to initial registration’s flow.

             STRICT HIERARCHICAL SELECTION RULE:
                - If you include a parent section in your response, DO NOT include any of its descendant sections.
                - A section is a descendant if its number starts with the parent section's number followed by a decimal point or underscore.
                - For example, if "5.5.1_registration_procedure" is included, then "5.5.1.2", "5.5.1.2.1", etc. must be excluded.


            EXAMPLES OF CORRECT SELECTION:
                BAD:
                "sections": [
                "5.5.1_registration_procedure",
                "5.5.1.2_registration_procedure_for_initial_registration",
                "5.5.1.2.1_general"
                ]

                GOOD:
                "sections": [
                "5.5.1_registration_procedure"
                ]


            CONTENT:
            {table_of_contents}
            """

    response = client.models.generate_content(
        model=flash_model,
        contents=prompt2,
        config={
            "response_mime_type": "application/json",
            "response_schema": Response,
            "temperature": 0,
        },
    )
    return response


def token_counter(client, model, contents):
    """Count the number of tokens in the given contents"""
    response = client.models.count_tokens(model=model, contents=contents)

    return response


response = get_relevant_sections(toc)
# Parse the response into the Sections model
response_json = response.text  # Gemini returns text, even with JSON mime type
sections_data = json.loads(response_json)  # Convert JSON string to dict
response = Response(**sections_data)  # Convert dict to Pydantic object

final_contents = generate_markdown(doc_id=1, target_headings=response.sections)


tokens_used = token_counter(client, flash_model, final_contents)

print(tokens_used)
