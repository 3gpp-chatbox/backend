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
        )

    return llm


# Load document and check if it loaded successfully
doc = doc_processor.load_document(docx_file_path)

# Extract sections from the document
sections = doc_processor.extract_section_tree(doc)

print(f"\nFound {len(sections)} top-level sections:")

print(f"Section 4 heading: {sections[4].heading}\nSection 4 content: {" ".join(sections[4].content)}")


# for section in sections:
#     print(f"\nSection: {section.heading} (Level {section.level})")
#     print(f"Number of subsections: {len(section.subsections)}")
#     print(f"Content paragraphs: {len(section.content)}")
#     print("-" * 80)

# # Extract procedures if needed
# procedures = doc_processor.extract_procedure_sections(doc)
# if procedures:
#     print(f"\nFound {len(procedures)} procedure sections:")
#     for proc in procedures:
#         print(f"\nProcedure: {proc['heading']} (Level {proc['level']})")
#         print(f"Content paragraphs: {len(proc['content'])}")
#         print(f"Subsections: {len(proc['subsections'])}")
#         print("-" * 80)

# Process the document in procedure-based chunks
# for procedure_chunk in doc_processor.proucess_procedures_in_chunks(docx_file_path):
#     # Create a document for each procedure section
#     procedure_doc = Document(
#         page_content=f"# {procedure_chunk['heading']}\n" + 
#         "\n".join(para['text'] for para in procedure_chunk['content'])
#     )
    
#     # Initialize LLM if not already done
#     if 'llm' not in locals():
#         llm = initialize_llm()
#         llm_transformer = LLMGraphTransformer(
#             llm=llm,
#             additional_instructions="""
#             Extract the following from the 3GPP procedure:
#             1. Procedure name and type
#             2. Triggering events or conditions
#             3. Steps in the procedure
#             4. State transitions
#             5. Related procedures or dependencies
            
#             Create nodes for:
#             - Procedures
#             - States
#             - Events/Triggers
            
#             Create relationships for:
#             - Procedure steps sequence
#             - State transitions
#             - Trigger relationships
#             """
#         )
    
#     # Process each procedure chunk
#     print(f"\nProcessing procedure: {procedure_chunk['heading']}")
#     try:
#         # Convert procedure to graph documents
#         graph_docs = llm_transformer.convert_to_graph_documents([procedure_doc])
        
#         # Initialize Neo4j graph if not already done
#         if 'graph' not in locals():
#             graph = Neo4jGraph()
        
#         # Add procedure to graph
#         graph.add_graph_documents(
#             graph_docs,
#             baseEntityLabel=True,
#             include_source=True,
#         )
        
#         print(f"Successfully processed procedure: {procedure_chunk['heading']}")
#     except Exception as e:
#         print(f"Error processing procedure {procedure_chunk['heading']}: {str(e)}")
#         continue


def test_llm(llm):
    ai_msg = llm.invoke("What model are you?")
    print(ai_msg)
