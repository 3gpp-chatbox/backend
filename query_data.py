import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from typing import List, Dict

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_DIR = "chroma_db"

def query_documents(query: str, n_results: int = 5, collection_name: str = "pdf_documents") -> List[Dict]:
    """
    Queries documents from ChromaDB using Google Gemini
    """
    if not GOOGLE_API_KEY:
        print("❌ Google API key not found. Please check your .env file.")
        return []

    try:
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=GOOGLE_API_KEY,
            model="models/embedding-001"
        )
        
        # Load the existing vector store
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
        print(f"Text snippet: {result['text'][:200]}...")
