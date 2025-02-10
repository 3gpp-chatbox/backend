import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Add parent directory to path
from config import Gemini_API_KEY  # Direct import
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize models and database
genai.configure(api_key=Gemini_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="db_3gpp")  # Persistent DB
collection = client.get_or_create_collection("3gpp_specs")  # Avoid errors


def search_3gpp_docs(query):
    """Retrieve relevant document chunks based on user query"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    
    # Flatten the results and extract the text from the nested structure
    metadata_list = results["metadatas"]
    texts = [r["text"] for sublist in metadata_list for r in sublist]  # Flatten and extract 'text' from each dictionary
    
    return texts  # Return the list of texts


def generate_summary(query):
    """Summarize retrieved 3GPP content using Gemini"""
    context = search_3gpp_docs(query)
    
    prompt = f"""
    Based on the following 3GPP specifications, answer the query:
    {context}
    ---
    User Query: {query}
    Provide a brief and accurate summary.
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text.strip()

# Example usage
if __name__ == "__main__":
    user_query = " Capability of a WLAN UE?"
    summary = generate_summary(user_query)
    print("Summary:", summary)
