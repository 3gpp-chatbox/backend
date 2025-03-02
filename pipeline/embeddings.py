'''
1.  Purpose: This script is responsible for creating vector embeddings for text chunks extracted from 3GPP documents and storing these embeddings along with their metadata (including the original text chunks) in a vector database (e.g., Chroma).

2.  Input:
    *   text chunks from relational database

3.  Processing:
    *   Loads a sentence-transformer model (specified by the `model_name` parameter, default is `all-mpnet-base-v2`).
    *   Creates embeddings for the text chunks using batch processing for efficiency.
    *   Initializes (or connects to an existing) a vector database collection.
    *   Ingests the embeddings and metadata into the vector database.  Each embedding is stored with its associated metadata.
    *   Optionally persists the client if you use PersistentClient.

4.  Output:
    *   The script returns the vector database collection object for use in the extractor script.

5.  Model Selection:
    * The `model_name` parameter allows you to choose different sentence-transformer models.  Valid options include:`all-mpnet-base-v2` 
'''
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict
from db_handler import ChunkDBHandler, DBHandler

class EmbeddingHandler:
    def __init__(self, model_name: str = "all-mpnet-base-v2", persist_directory: str = "chroma_db"):
        """Initialize with chosen model and ChromaDB"""
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def create_collection(self, collection_name: str):
        """Create or get existing collection"""
        try:
            collection = self.client.get_collection(collection_name)
            print(f"Using existing collection: {collection_name}")
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {collection_name}")
        return collection

    def process_chunks(self, chunks: List[Dict], collection_name: str):
        """Process chunks and store in ChromaDB"""
        if not chunks:
            raise ValueError("No chunks provided for embedding creation")
        
        print(f"\nProcessing {len(chunks)} chunks for embeddings...")
        
        # Create or get collection
        collection = self.create_collection(collection_name)
        
        # Prepare data for batch processing
        ids = [str(chunk['index']) for chunk in chunks]
        texts = [
            f"{chunk.get('title', '')} {chunk.get('content', '')}".strip() 
            for chunk in chunks
        ]
        metadatas = [{
            'title': chunk.get('title', ''),
            'level': chunk.get('level', 0),
            'index': chunk['index']
        } for chunk in chunks]
        
        # Add documents in batches
        batch_size = 32
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(texts), batch_size):
            batch_end = min(i + batch_size, len(texts))
            current_batch = (i // batch_size) + 1
            print(f"Processing batch {current_batch}/{total_batches} ({batch_end-i} chunks)")
            
            collection.add(
                ids=ids[i:batch_end],
                documents=texts[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )
        
        print(f"✓ Successfully processed all {len(chunks)} chunks")
        return collection

def process_embeddings(db_handler: DBHandler, doc_id: str) -> chromadb.Collection:
    """Process document embeddings"""
    print("\n[3/3] Processing embeddings...")
    try:
        # Check if collection already exists
        try:
            collection = db_handler.chroma_client.get_collection(doc_id)
            print("→ Found existing embeddings collection")
            # Verify collection has content
            if collection.count() > 0:
                print(f"✓ Using existing collection with {collection.count()} embeddings")
                return collection
        except:
            pass

        # Create new embeddings if needed
        print("→ Creating new embeddings...")
        collection = db_handler.create_embeddings(doc_id)
        print(f"✓ Created new embeddings collection: {doc_id}")
        return collection

    except Exception as e:
        print(f"✗ Error processing embeddings: {e}")
        return None 