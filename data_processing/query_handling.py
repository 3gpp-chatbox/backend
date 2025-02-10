import google.generativeai as genai
from config import Gemini_API_KEY
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize models and database
genai.configure(api_key=Gemini_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("3gpp_docs")  # or get_collection if it exists

def search_3gpp_docs(query):
    """Retrieve relevant document chunks based on user query"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    
    return [r["text"] for r in results["metadatas"][0]]

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
user_query = "What is the NAS message structure in 5G?"
summary = generate_summary(user_query)
print("Summary:", summary)
