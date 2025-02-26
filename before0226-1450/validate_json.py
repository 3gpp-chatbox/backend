import json
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Optional


# Define the structure of nodes in the graph
class Node(BaseModel):
    id: str
    type: str
    properties: Optional[Dict[str, str]] = {}  # Flexible properties (empty dictionary is acceptable)
    parameters: Optional[List[str]] = []  # Flexible parameters, can be empty

# Define the structure of edges in the graph
class Edge(BaseModel):
    from_node: str
    to_node: str
    action: str
    properties: Optional[Dict[str, str]] = {}  # Flexible properties (empty dictionary is acceptable)

# Define the top-level structure for the graph
class GraphModel(BaseModel):
    nodes: List[Node]  # List of nodes
    edges: List[Edge]  # List of edges

def clean_json(file_path):
    """Remove Markdown-style triple backticks (```json ... ```) from the JSON file."""
    try:
        with open(file_path, "r") as f:
            raw_data = f.read()

        # Remove Markdown code block indicators (```json and ```)
        cleaned_data = raw_data.strip().replace("```json", "").replace("```", "").strip()

        # Overwrite the file with cleaned JSON
        with open(file_path, "w") as f:
            f.write(cleaned_data)

    except Exception as e:
        print(f"Error cleaning JSON: {e}")


def validate_json(file_path: str):
    """Validate JSON file after cleaning."""
    clean_json(file_path)  # Clean JSON before validation

    if not os.path.exists(file_path):
        print("Error: JSON file not found.")
        return

    try:
        # Open the cleaned JSON file and parse it
        with open(file_path, "r") as f:
            data = json.load(f)  # Try to load the cleaned JSON from file

        # Validate the cleaned JSON with Pydantic
        graph = GraphModel(**data)  # Use data read from file for Pydantic validation
        print("VALID JSON: Pydantic validation passed")
    
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: JSON decode error - {e}")
    except ValidationError as e:
        print(f"INVALID JSON: Pydantic validation error - {e}")

if __name__ == "__main__":
    JSON_FILE = "data.json"  # Path to your JSON file
    validate_json(JSON_FILE)  # Run the validation process
