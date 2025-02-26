# src/main.py
import os
from dotenv import load_dotenv
from google import genai
import src.lib.doc_processor as doc_processor
from pydantic import BaseModel


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


class Sections(BaseModel):
    sections: list[str]


def get_relevant_sections(table_of_contents: str):
    prompt = f"""
                ROLE: You are an expert in 3GPP specifications.

                ---

                TASK: Analyze the table of contents of 3GPP TS 24.501 provided below and identify the sections that contain the detailed description of the initial registration procedure. Based on the section titles, determine which sections are specifically about the initial registration process.

                - If a section has subsections and all of them are relevant to the initial registration procedure, return the parent section instead of listing the subsections.
                - If only some subsections of a section are relevant, return only those specific subsections.
                - Always return the section number followed by its name exactly as written in the table of contents.
                - For example:
                - If the table of contents includes "5.5_Registration_Procedures" with subsections "5.5.1_General" and "5.5.2_Initial Registration", return "5.5.2_Initial Registration".
                - If "5.5.2_Initial_Registration" has subsections "5.5.2.1_Overview" and "5.5.2.2_Procedure", and all are relevant, return "5.5.2_Initial_Registration".
                - If only "5.5.2.1_Overview" is relevant, return "5.5.2.1_Overview".

                ---

                CONTENT:
                {table_of_contents}
               """

    response = client.models.generate_content(
        model=flash_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Sections,
        },
    )
    return response


stripped_doc_path = doc_processor.remove_sections(
    file_path=docx_file_path, excluded_sections=sections_to_exclude
)

# Load the stripped document
doc = doc_processor.load_document(stripped_doc_path)


# Extract sections from the document
section_tree = doc_processor.extract_section_tree(doc)

toc = doc_processor.extract_table_of_contents(section_tree)

response = get_relevant_sections(toc)

print("response\n------------------------------")
print(response.text)
