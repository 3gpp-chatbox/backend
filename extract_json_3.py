
 #Primary authentication and key agreement procedure


#no need description,only json
import sqlite3
import os
from dotenv import load_dotenv
from google import genai
import json
from pydantic import ValidationError

load_dotenv()


from pydantic import BaseModel
from typing import List, Optional, Dict


# Load Environment Variables
load_dotenv()

# Configure Google Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")


# Define Node Structure
class Node(BaseModel):
    id: str
    type: str
    properties: Optional[Dict[str, str]] = {}
    parameters: Optional[List[str]] = []

# Define Edge Structure
class Edge(BaseModel):
    from_node: str
    to_node: str
    action: str
    properties: Optional[Dict[str, str]] = {}

# Define Graph Model
class GraphModel(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


def extract_procedural_info_from_text(section_name, text):
    """Extract procedural information into JSON format using Gemini API and schema validation."""

    prompt = f"""
    Below is the chunk text of a section:

    {text}

    Section Name: {section_name}

    Identify the procedure name based on the content.
    Extract procedural information and structure it into the **Flow Property Graph JSON format**.

    Respond **only** with JSON without any additional explanation.
    """

    response = model.generate_content(
        contents=prompt,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": GraphModel,
        },
    )

    # If Gemini successfully validates the JSON schema, return parsed JSON
    if response.parsed:
        return response.parsed
    else:
        return response.text  # Fallback if no JSON is parsed





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

procedural_info = process_section("5.5.1.2.2", db_path)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "data-2.json")
else:
    print(f"No content found for section {section_id_to_process}")



