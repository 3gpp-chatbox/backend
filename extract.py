import sqlite3
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
from typing import List, Dict, Optional, Any 
import sys
import re
import chromadb
from sentence_transformers import SentenceTransformer

# Configure API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')
# ✅ Initialize the embedding model for query encoding
model_embedding = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ Initialize ChromaDB client and connect to the collection
client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "3gpp_sections"

PROCEDURE_NAME = "Initial Registration Initiation"

# Retrieve the existing collection
try:
    collection = client.get_collection(collection_name)
    print(f"Using existing ChromaDB collection: {collection_name}")
except chromadb.errors.CollectionNotFound:
    print(f"Error: Collection '{collection_name}' not found.")
    sys.exit(1)  # Exit if collection is not found



def generate_keywords(procedure_name):
    prompt = f"""
    you are 3gpp expert  expert, you know 3gpp specification procedure very well.
    Generate keywords related to the 3GPP procedure: {procedure_name}.
    Return keywords as a comma-separated list.
    """
    response = model.generate_content(prompt)
    return response.text.strip().split(", ")

keywords = generate_keywords(PROCEDURE_NAME)
print(f"Generated keywords: {keywords}")

def find_relevant_sections(query, collection, top_n=3):
    query_embedding = model_embedding.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_n)
    return results["documents"][0], results["ids"][0] #return documents and ids

relevant_sentences, relevant_ids = find_relevant_sections(PROCEDURE_NAME + " " + " ".join(keywords), collection)

#Recreate the top section.
top_section_sentences = []
for id, sentence in zip(relevant_ids, relevant_sentences):
    section_id = id.split("_sentence_")[0]
    if section_id == relevant_ids[0].split("_sentence_")[0]:
        top_section_sentences.append(sentence)

top_section = ". ".join(top_section_sentences)

other_sections = relevant_sentences[1:]



def extract_specific_parts(section, procedure_name, collection):
    query_embedding = model_embedding.encode(procedure_name).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3, where={"$contains": section})
    return ". ".join(results["documents"][0])

extracted_parts = [extract_specific_parts(section, PROCEDURE_NAME, collection) for section in other_sections]



INPUT_FOLDER = "llm_inputs"  # Name of the folder
if not os.path.exists(INPUT_FOLDER):
    os.makedirs(INPUT_FOLDER)
def extract_procedure_info(top_section, other_sections, procedure_name):
    combined_content = f"This is the top relevant section name and content: {top_section}\n\n"
    combined_content += "This is the second and third relevant section name and its content: "

    for section in other_sections:
        combined_content += section + "\n\n"


     # Save the input content to a file
    file_path = os.path.join(INPUT_FOLDER, "llm_input.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(combined_content)

    prompt = f"""
    Extract procedure information from the following text related to the procedure "{procedure_name}":
    {combined_content}
    Return the information in JSON format.
    """
    response = model.generate_content(prompt)
    extracted_json = response.text.strip()

    combine_prompt = f"""
    Create a summary of the following procedure information:
    {extracted_json}
    """
    combined_response = model.generate_content(combine_prompt)

    return extracted_json, combined_response.text.strip()

all_sections_content = [top_section] + extracted_parts
extracted_json, summary = extract_procedure_info(top_section, extracted_parts, PROCEDURE_NAME)
print("Extracted JSON:", extracted_json)
print("Summary:", summary)