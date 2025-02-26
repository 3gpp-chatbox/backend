import json
import os
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Optional


import json
import os

JSON_FILE = "data.json"

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

def validate_json():
    """Validate JSON file after cleaning."""
    clean_json(JSON_FILE)  # Clean JSON before validation

    if not os.path.exists(JSON_FILE):
        print("Error: JSON file not found.")
        return

    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)  # Try to parse JSON
        print("VALID JSON")  # If successful, print valid message
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e}")  # Print validation error

if __name__ == "__main__":
    validate_json()
