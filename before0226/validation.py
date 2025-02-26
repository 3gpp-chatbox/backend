import json
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Optional


# Define the Pydantic models
class Node(BaseModel):
    id: str
    type: str
    properties: Dict[str, Optional[str]] = Field(default_factory=dict)
    parameters: Optional[List[str]] = None

class Edge(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    action: Optional[str] = None
    event: Optional[str] = None
    properties: Dict[str, Optional[str]] = Field(default_factory=dict)

class ProcedureGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


def preprocess_json_data(json_data):
    """Sanitize and correct the JSON data before validation."""
    for edge in json_data.get('edges', []):
        # Ensure parameters is a list of strings in the 'properties' field
        if "parameters" in edge.get("properties", {}):
            edge["properties"]["parameters"] = [
                str(param) for param in edge["properties"]["parameters"]
            ]
        # Ensure any missing fields like 'event' or 'action' are handled
        if "action" not in edge:
            edge["action"] = None
        if "event" not in edge:
            edge["event"] = None
    return json_data


def validate_json_file(file_path):
    """Checks if the JSON file exists and validates it using Pydantic."""
    if os.path.exists(file_path):
        print(f"✅ JSON file found: {file_path}")
        
        # Open the JSON file and attempt to load and validate it
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)

                # Preprocess the data to ensure it's in the correct format
                json_data = preprocess_json_data(json_data)
                
                # Validate using Pydantic models
                validated_data = ProcedureGraph(**json_data)  # Validate with the Pydantic model

                # If validation passes, print success message
                print(f"✅ JSON validation successful for {file_path}")
        
        except json.JSONDecodeError:
            print(f"❌ Failed to decode JSON in file: {file_path}")
        except ValidationError as e:
            print(f"❌ Pydantic validation failed: {e}")
    else:
        print(f"❌ JSON file not found: {file_path}")


# Manually provide the JSON file path here
json_file_path = "0225-json-test4.json"

# Validate the JSON file
validate_json_file(json_file_path)
