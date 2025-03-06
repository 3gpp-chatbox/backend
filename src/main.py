# src/main.py
import json
import os

from dotenv import load_dotenv
from google import genai

from src.schemas import FlowPropertyGraph

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


def token_counter(client, model, contents):
    """Count the number of tokens in the given contents"""
    response = client.models.count_tokens(model=model, contents=contents)

    return response


def generate_graph(client, model, contents):
    prompt = f"""
    You are tasked with analyzing a 3GPP specification document and creating a flow property graph representation of the procedural information contained within.

    # OBJECTIVE
    Extract the procedural flow from the 3GPP specification and represent it as a structured flow property graph that captures states, events, actions, and transitions.

    # DETAILED INSTRUCTIONS
    1. Identify the key components of the 3GPP procedure:
    - States: Different conditions of network elements (UE, AMF, SMF, etc.)
    - Events: Triggers that cause transitions between states
    - Actions: Operations performed by network elements
    - Messages: Protocol messages exchanged between entities
    - Parameters: Data elements exchanged or required during the procedure
    - Conditionals: Decision points and alternative paths in the procedure

    2. Create a flow property graph with:
    - Nodes representing States and Events
    - Edges representing Actions and Transitions
    - Properties capturing Parameters, Conditionals, and Metadata

    3. Include specific 3GPP protocol elements:
    - Network entities (UE, AMF, SMF, gNB, etc.)
    - Message types (Registration Request, Authentication Request, etc.)
    - Protocol timers and counters
    - Error handling and fallback procedures

    Now analyze the provided 3GPP specification text and create a comprehensive flow property graph following this format.

    The procedure target is initial registration procedure
    ---
    {contents}
    """

    # Updated API call using Pydantic schema
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": FlowPropertyGraph,
            "temperature": 0,
        },
    )

    with open("output/flow_graph2.json", "w") as f:
        # Parse the response into the Sections model
        response_text = response.text  # Gemini returns text, even with JSON mime type
        response_json = json.loads(response_text)  # Convert JSON string to dict
        response = FlowPropertyGraph(**response_json)  # Convert dict to Pydantic object
        json.dump(response_json, f, indent=4)

    return response


contents_path = "contents.md"


with open(contents_path, "r") as f:
    contents = f.read()


generate_graph(client, flash_model, contents)
