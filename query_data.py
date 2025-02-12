import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_DIR = "chroma_db"

# Ensure that the GOOGLE_API_KEY is available
if not GOOGLE_API_KEY:
    raise ValueError("❌ Google API key not found. Please check your .env file.")

# Set the API key for the Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def query_documents(query: str, n_results: int = 5, collection_name: str = "pdf_documents") -> List[Dict]:
    """
    Queries documents from ChromaDB using Google Gemini API to generate summaries.
    """
    try:
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        # Load the existing vector store with embeddings
        vector_store = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embeddings,
            collection_name=collection_name
        )

        # Query the vector store
        results = vector_store.similarity_search_with_relevance_scores(query, k=n_results)
        
        if not results:
            print("❌ No results found.")
            return []

        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "text": doc.page_content,
                "metadata": doc.metadata,
                "distance": score
            })

        return formatted_results

    except Exception as e:
        print(f"❌ Error querying documents: {str(e)}")
        return []

if __name__ == "__main__":
    test_query = "What is the main topic?"
    results = query_documents(test_query)

    print(f"\nQuery: {test_query}")
    print("\nResults:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']}")
        print(f"Processed text: {result['text'][:300]}...")  # Show snippet of the processed summary

def generate_embeddings(texts):
    """Generate embeddings using Gemini"""
    try:
        response = genai.embed_text(model="models/embedding-001", text=texts)
        return [embedding['embedding'] for embedding in response['embeddings']]
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return []

def query_with_gemini(query_text):
    """Query with Gemini for generating relevant responses"""
    try:
        response = genai.generate_text(model="models/generative-001", text=query_text)
        return response['text']
    except Exception as e:
        print(f"Error querying with Gemini: {str(e)}")
        return None