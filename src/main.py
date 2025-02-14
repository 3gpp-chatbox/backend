# src/main.py
import os
import getpass
from docx import Document as DocxDocument
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
import lib.doc_processor as doc_processor


# Load the Google API Key from the .env file
load_dotenv(override=True)

# Load the docx file inside data/
docx_file_path = "data/24501-j11.docx"

ollama = False

# Load the document
doc = doc_processor.load_document(docx_file_path)

doc_processor.process_specification(docx_file_path)


def initialize_llm():
    if ollama:
        print("Using Ollama")
        llm = ChatOllama(
            model="llama3.1",
            temperature=0,
            format="json",
        )
    else:
        print("Using Google Generative AI")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            format="json",
            # max_tokens=1000,
            # timeout=None,
            # max_retries=2,
        )

    return llm


"""
Test the LLM setup
"""


def test_llm(llm):
    ai_msg = llm.invoke("What model are you?")
    print(ai_msg)


llm = initialize_llm()

# test_llm(llm)

prompt = "Extract NAS procedures from the document"

llm_transformer = LLMGraphTransformer(llm=llm, additional_instructions=prompt)


"""
Set-up the Neo4j Graph
"""
# graph = Neo4jGraph()

# doc = load_doc(docx_file_path)


# graph_docs = llm_transformer.convert_to_graph_documents([Document(page_content=doc)])

# print(graph_docs[0])


# graph.add_graph_documents(
#     graph_docs,
#     baseEntityLabel=True,
#     include_source=True,
# )
