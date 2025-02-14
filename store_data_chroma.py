import os
from dotenv import load_dotenv
from chromadb import PersistentClient, Settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict
from preprocess_pdfs import read_pdfs_from_directory
from rich.console import Console
import shutil

# Initialize console
console = Console()

# Load the environment variables from the .env file
load_dotenv()

# Access the Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Constants
DATA_FOLDER = "data"
CHROMA_DB_DIR = "chroma_db"

def reset_chroma_db():
    """Reset the ChromaDB directory"""
    if os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)
        console.print("[yellow]Removed existing ChromaDB directory[/yellow]")

def initialize_chroma_client():
    """Initialize ChromaDB client with proper settings"""
    try:
        settings = Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=True
        )
        client = PersistentClient(path=CHROMA_DB_DIR, settings=settings)
        return client
    except Exception as e:
        console.print(f"[red]Error initializing ChromaDB client: {str(e)}[/red]")
        return None

def check_if_documents_exist(collection_name: str = "pdf_documents") -> bool:
    """
    Check if documents already exist in ChromaDB
    """
    try:
        client = initialize_chroma_client()
        if not client:
            return False
            
        try:
            collection = client.get_collection(collection_name)
            count = collection.count()
            return count > 0
        except Exception as e:
            console.print(f"[yellow]Collection not found: {str(e)}[/yellow]")
            return False
    except Exception as e:
        console.print(f"[red]Error checking documents: {str(e)}[/red]")
        return False

def store_documents_in_chroma(documents: List[Dict[str, str]], collection_name: str = "pdf_documents", force_reset: bool = False):
    """
    Stores documents in ChromaDB using Google Gemini embeddings
    """
    if not documents:
        console.print("[red]❌ No documents to store.[/red]")
        return None

    if not GOOGLE_API_KEY:
        console.print("[red]❌ Google API key not found. Please check your .env file.[/red]")
        return None

    try:
        # Initialize Gemini embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=GOOGLE_API_KEY,
            model="models/embedding-001"  # Gemini embedding model
        )
        
        # Reset ChromaDB if requested
        if force_reset:
            reset_chroma_db()
        
        # Initialize ChromaDB client
        client = initialize_chroma_client()
        if not client:
            return None
        
        # Get or create collection
        try:
            collection = client.get_collection(collection_name)
            console.print(f"[blue]Using existing collection: {collection_name}[/blue]")
        except:
            collection = client.create_collection(collection_name)
            console.print(f"[blue]Created new collection: {collection_name}[/blue]")

        # Process documents in batches
        batch_size = 10  # Smaller batch size for better reliability
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Prepare batch data
            texts = [doc["text"] for doc in batch]
            metadatas = [doc["metadata"] for doc in batch]
            ids = [f"doc_{i + idx}" for idx in range(len(batch))]
            
            try:
                # Generate embeddings for the batch
                embeddings_batch = [embeddings.embed_query(text) for text in texts]
                
                # Add documents to collection
                collection.add(
                    embeddings=embeddings_batch,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                console.print(f"[green]✓ Stored batch {i//batch_size + 1} ({len(batch)} documents)[/green]")
            except Exception as e:
                console.print(f"[red]Error processing batch {i//batch_size + 1}: {str(e)}[/red]")
                continue

        total_count = collection.count()
        console.print(f"[green]✅ Total documents in collection: {total_count}[/green]")
        return collection

    except Exception as e:
        console.print(f"[red]❌ Error storing documents: {str(e)}[/red]")
        return None

def check_stored_data(collection_name: str = "pdf_documents", top_n: int = 5):
    """
    Check the first N documents stored in the ChromaDB collection
    """
    try:
        client = initialize_chroma_client()
        if not client:
            return
            
        collection = client.get_collection(collection_name)
        
        # Get all document IDs
        all_ids = collection.get()["ids"][:top_n]
        
        # Retrieve the documents
        results = collection.get(
            ids=all_ids,
            include=["documents", "metadatas"]
        )

        if not results["documents"]:
            console.print("[yellow]No documents found in the collection.[/yellow]")
            return

        console.print(f"[green]✅ Retrieved {len(results['documents'])} documents from ChromaDB:[/green]")
        for idx, doc in enumerate(results["documents"]):
            console.print(f"\n[blue]{idx + 1}. Source: {results['metadatas'][idx].get('source', 'Unknown')}[/blue]")
            console.print(f"Text snippet: {doc[:200]}...")

    except Exception as e:
        console.print(f"[red]Error checking stored data: {str(e)}[/red]")

if __name__ == "__main__":
    # Check if documents already exist in ChromaDB
    if not check_if_documents_exist():
        console.print("[blue]Reading PDFs...[/blue]")
        data_directory = "data"
        documents = read_pdfs_from_directory(data_directory)
        store_documents_in_chroma(documents, force_reset=True)  # Force reset to ensure clean state
    else:
        console.print("[green]✅ Documents already exist in ChromaDB, checking data...[/green]")

    # Check stored data
    check_stored_data()  # This will retrieve and display the first 5 stored documents
