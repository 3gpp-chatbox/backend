# src/main.py
import os
import getpass
from docx import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load the docx file inside data/
docx_file_path = "data/24501-j11.docx"

# Load the Google API Key from the .env file
load_dotenv()

"""
Load the docx file and return the document object
"""
def load_doc(path):
    try:
        print(f"Loading document from {path}")
        doc = Document(docx_file_path)

        return doc

    except FileNotFoundError:
        print(f"File not found: {docx_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


"""
Initialize the LLM
"""
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=1000,
    timeout=None,
    max_retries=2,
)

"""
Test the LLM setup
"""
def test_llm():
    ai_msg = llm.invoke("Hello, how are you?")
    print(ai_msg)

# test_llm()

llm_transformer = LLMGraphTransformer(llm=llm)
