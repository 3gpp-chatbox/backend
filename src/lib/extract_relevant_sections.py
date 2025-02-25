# src/main.py
import os
from dotenv import load_dotenv
from google import genai
import src.lib.doc_processor as doc_processor


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


# Load the docx file inside data/
docx_file_path = "data/24501-j11.docx"

sections_to_exclude = [
    "annex",
    "appendix",
    "abbreviations",
    "scope",
    "references",
    "foreword",
]


# stripped_doc_path = doc_processor.remove_sections(
#     file_path=docx_file_path, excluded_sections=sections_to_exclude
# )

# doc = doc_processor.load_document(stripped_doc_path)

# Read the table of contents from the document toc.md
toc_file_path = "toc.md"

with open(toc_file_path, "r") as f:
    toc = f.read()

def get_relevant_sections(table_of_contents: str):
    prompt = f"""
             ROLE: You are an expert in 3GPP specifications. 
             --

             You are tasked with analyzing the table of contents of specific documents and extracting relevant sections that contains information about initial registration procedures.

           

             Return an array of section titles.

             --


             TASK: Analyze the table of contents of the document: 124.501 and extract the relevant sections that contain procedural flow information.

             CONTENT:

             {table_of_contents}
             """

    response = client.models.generate_content(model=pro_model, contents=prompt)
    return response


response = get_relevant_sections(toc)

print(response.text)

