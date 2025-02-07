import os
import pickle
from dotenv import load_dotenv
from chromadb import PersistentClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document  # Import Document class
from typing import List, Dict
from preprocess_pdfs import read_pdfs_from_directory

# Load the environment variables from the .env file
load_dotenv()

# Access the Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Constants
DATA_FOLDER = "data"
CHROMA_DB_DIR = "chroma_db"

def check_if_documents_exist(collection_name: str = "pdf_documents") -> bool:
    """
    Check if documents already exist in ChromaDB
    """
    client = PersistentClient(path=CHROMA_DB_DIR)
    try:
        collection = client.get_collection(collection_name)
        count = collection.count()
        return count > 0
    except Exception as e:
        print(f"Collection not found: {str(e)}")
        return False

def store_documents_in_chroma(documents: List[Dict[str, str]], collection_name: str = "pdf_documents"):
    """
    Stores documents in ChromaDB using Google Gemini embeddings
    """
    if not documents:
        print("❌ No documents to store.")
        return None

    if not GOOGLE_API_KEY:
        print("❌ Google API key not found. Please check your .env file.")
        return None

    try:
        # Initialize Gemini embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=GOOGLE_API_KEY,
            model="models/embedding-001"  # Gemini embedding model
        )
        
        # Convert dictionaries into Document objects
        document_objects = [
            Document(page_content=doc["text"], metadata=doc["metadata"]) for doc in documents
        ]

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(document_objects)

        print(f"✅ Split into {len(chunks)} chunks")

        # Store in ChromaDB
        vector_store = Chroma.from_documents(
            chunks, 
            embeddings, 
            persist_directory=CHROMA_DB_DIR,
            collection_name=collection_name
        )
        vector_store.persist()

        print(f"✅ Stored {len(chunks)} documents in ChromaDB")
        return vector_store

    except Exception as e:
        print(f"❌ Error storing documents: {str(e)}")
        return None

def check_stored_data(collection_name: str = "pdf_documents", top_n: int = 5):
    """
    Check the first N documents stored in the ChromaDB collection
    """
    client = PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_collection(collection_name)

    # Retrieve the first N documents in the collection
    results = collection.get(include_metadata=True, limit=top_n)

    if not results:
        print("❌ No documents found in the collection.")
        return

    print(f"✅ Retrieved {len(results['documents'])} documents from ChromaDB:")
    for idx, doc in enumerate(results['documents']):
        print(f"\n{idx + 1}. Source: {results['metadatas'][idx]['source']}")
        print(f"Text snippet: {doc[:200]}...")

if __name__ == "__main__":
    # Check if documents already exist in ChromaDB
    if not check_if_documents_exist():
        data_directory = "data"
        documents = read_pdfs_from_directory(data_directory)
        store_documents_in_chroma(documents)
    else:
        print("✅ Documents already exist in ChromaDB, skipping PDF read and storage.")

    # Check stored data
    check_stored_data()  # This will retrieve and display the first 5 stored documents
