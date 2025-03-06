import json
import datetime

from src.schemas import FlowPropertyGraph


def generate_graph(
    client, model: str, contents: str, procedure_name: str, save_file=False
):
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

    The procedure target is **{procedure_name}**.
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

    if save_file:
        file_name = f"output/graphs/flash/{procedure_name.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(file_name, "w") as f:
            # Parse the response into the Sections model
            response_text = (
                response.text
            )  # Gemini returns text, even with JSON mime type
            response_json = json.loads(response_text)  # Convert JSON string to dict
            response = FlowPropertyGraph(
                **response_json
            )  # Convert dict to Pydantic object
            json.dump(response_json, f, indent=4)

    return response
