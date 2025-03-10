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

# Retrieve the existing collection
try:
    collection = client.get_collection(collection_name)
    print(f"Using existing ChromaDB collection: {collection_name}")
except chromadb.errors.CollectionNotFound:
    print(f"Error: Collection '{collection_name}' not found.")
    sys.exit(1)  # Exit if collection is not found



def generate_keywords(procedure_name):
    try:
        prompt = f"""
        Generate keywords related to the 3GPP procedure: {procedure_name}.
        Return keywords as a comma-separated list.
        """
        # Assuming `model.generate_content()` is returning a response with a `.text` attribute
        response = model.generate_content(prompt)
        
        # Ensure response has text and split into keywords
        return response.text.strip().split(", ") if response.text.strip() else []
    except Exception as e:
        print(f"Error generating keywords: {e}")
        return []


def find_relevant_sections(query, collection, top_n=3):
    try:
        # Encode the query (combining the procedure name and keywords)
        query_embedding = model_embedding.encode(query).tolist()

        # Perform the query to get the top N relevant sections
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_n,
            include=["embeddings", "documents"]  # Include embeddings and documents in the query result
        )

        # Check if results are found
        if not results.get("documents"):
            print("No relevant sections found.")
            return []

        # Return the documents (sections)
        return results["documents"]
    
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []


# Example: Generate keywords for the procedure name
keywords = generate_keywords("initial registration initiation")
print(f"Generated keywords: {keywords}")

# Combine the procedure name and keywords for the query
query = "initial registration initiation " + " ".join(keywords)

# Find relevant sections based on the query
relevant_sections = find_relevant_sections(query, collection)

# Print the relevant sections found
print(f"Relevant sections found: {len(relevant_sections)}")
if relevant_sections:
    for idx, section in enumerate(relevant_sections):
        print(f"Section {idx + 1}: {section[:200]}...")  # Print the first 200 chars of each section for preview


