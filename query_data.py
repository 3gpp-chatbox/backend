import os
from dotenv import load_dotenv
import google.generativeai as genai
from chromadb import PersistentClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict
from rich.console import Console
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Initialize console
console = Console()

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_DIR = "chroma_db"

# Ensure that the GOOGLE_API_KEY is available
if not GOOGLE_API_KEY:
    raise ValueError("❌ Google API key not found. Please check your .env file.")

# Set the API key for the Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def query_documents(query: str, n_results: int = 5, collection_name: str = "pdf_documents") -> List[Dict]:
    """
    Queries documents from ChromaDB using Google Gemini API to generate summaries.
    Includes retry logic for resilience.
    """
    try:
        console.print(f"[blue]Initializing embeddings for query: {query}[/blue]")
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        console.print("[blue]Loading ChromaDB client...[/blue]")
        # Initialize ChromaDB client with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                client = PersistentClient(path=CHROMA_DB_DIR)
                collection = client.get_collection(collection_name)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                console.print(f"[yellow]Retry {attempt + 1}/{max_retries} connecting to ChromaDB[/yellow]")
                time.sleep(2 ** attempt)  # Exponential backoff

        console.print("[blue]Generating query embedding...[/blue]")
        # Generate embedding for the query
        query_embedding = embeddings.embed_query(query)

        console.print("[blue]Performing similarity search...[/blue]")
        # Query the collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        if not results['documents']:
            console.print("[yellow]No results found in ChromaDB[/yellow]")
            return []

        # Format results
        formatted_results = []
        for i in range(len(results['documents'])):
            formatted_results.append({
                "text": results['documents'][i],
                "metadata": results['metadatas'][i] if isinstance(results['metadatas'][i], dict) else {"source": str(results['metadatas'][i])},
                "distance": results['distances'][i]
            })

        console.print(f"[green]✓ Found {len(formatted_results)} results[/green]")
        return formatted_results

    except Exception as e:
        console.print(f"[red]Error querying documents: {str(e)}[/red]")
        return []

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def query_with_gemini(query_text: str) -> str:
    """Query with Gemini for generating relevant responses with retry logic"""
    try:
        console.print("[blue]Sending query to Gemini API...[/blue]")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query_text)
        
        if response.text:
            console.print("[green]✓ Received response from Gemini[/green]")
            return response.text
        else:
            console.print("[yellow]Warning: Empty response from Gemini[/yellow]")
            return None
            
    except Exception as e:
        console.print(f"[red]Error querying Gemini: {str(e)}[/red]")
        return None

# Test code
if __name__ == "__main__":
    test_query = "What is the main topic?"
    results = query_documents(test_query)

    print(f"\nQuery: {test_query}")
    print("\nResults:")
    for i, result in enumerate(results, 1):
        metadata = result['metadata'] if isinstance(result['metadata'], dict) else {"source": str(result['metadata'])}
        print(f"\n{i}. Source: {metadata.get('source', 'Unknown')}")
        print(f"Distance: {result['distance']}")
        print(f"Text: {result['text'][:300]}...")  # Show snippet of the text

def generate_embeddings(texts):
    """Generate embeddings using Gemini"""
    try:
        response = genai.embed_text(model="models/embedding-001", text=texts)
        return [embedding['embedding'] for embedding in response['embeddings']]
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return []