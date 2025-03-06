# src/main.py
import json
import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

from src.lib.extract_content_data import generate_markdown
from src.lib.extract_property_graph import generate_graph
from src.lib.extract_relevant_sections import get_relevant_sections

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

if __name__ == "__main__":
    prompt_1_response = get_relevant_sections(toc)

    # Parse the response into the Sections model
    response_1_text = (
        prompt_1_response.text
    )  # Gemini returns text, even with JSON mime type
    response_as_dict = json.loads(response_1_text)  # Convert JSON string to dict

    prompt_1_response = Response(
        **response_as_dict
    ).sections  # Convert dict to Pydantic object

    # Generate markdown output of relevant sections
    relevant_chunks_md = generate_markdown(
        doc_id="24501-j11", target_headings=prompt_1_response
    )

    # Generate property graph
    prompt_2_response = generate_graph(
        client=client, model=flash_model, contents=relevant_chunks_md, save_file=True
    )
