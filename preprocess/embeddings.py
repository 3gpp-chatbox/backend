'''
1. create embedings for : 
    1.data chunks
    2.queries 
2. use the following models both for data chunks and queries: 
    i. Sentence Embeddings: 
    modelst to use: sentence-transformers- all-mpnet-base-v2, all-MiniLM-L6-v2, or all-distilroberta-v1, universal-sentence encoder (USE)- google/universal-sentence-encoder-large
    ii. Domain-Specific Embeddings: Fine-tuning Sentence-Transformers, Training from Scratch (Advanced): If you have a very large corpus of 3GPP data, you could train a language model (like BERT or RoBERTa)

3. Embedding Optimization: Dimensionality Reduction, Clustering, and Indexing
4. Embedding Storage: Vector Database (e.g., FAISS)
5. Embedding Retrieval: Querying the Vector Database
'''
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
from typing import List, Dict, Tuple
from db_handler import ChunkDBHandler

class EmbeddingHandler:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):  # Using a more powerful model
        """Initialize with chosen model"""
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunk_ids = []  # Store chunk IDs to map back to database
        
    def create_chunk_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """Create embeddings for data chunks"""
        # Store chunk IDs for later retrieval
        self.chunk_ids = [chunk['index'] for chunk in chunks]
        
        # Combine title and content for better context
        texts = [f"{chunk['title']} {chunk['content']}" for chunk in chunks]
        embeddings = self.model.encode(
            texts, 
            show_progress_bar=True,
            normalize_embeddings=True  # Normalize for better similarity search
        )
        return embeddings

    def create_query_embedding(self, query: str) -> np.ndarray:
        """Create embedding for a search query"""
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return query_embedding

    def build_faiss_index(self, embeddings: np.ndarray):
        """Build FAISS index with optimizations"""
        # Using IndexIVFFlat for better search performance
        quantizer = faiss.IndexFlatL2(self.dimension)
        nlist = min(int(len(embeddings) / 10), 100)  # number of clusters
        self.index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
        
        # Train the index
        if not self.index.is_trained:
            self.index.train(embeddings.astype('float32'))
        
        # Add vectors to the index
        self.index.add(embeddings.astype('float32'))
        
        # Set search parameters
        self.index.nprobe = min(nlist, 10)  # Number of clusters to search
        return self.index

    def search(self, query: str, k: int = 5) -> List[Tuple[int, float]]:
        """Search for similar chunks using a query"""
        if not self.index:
            raise ValueError("Index not built or loaded")
            
        # Create query embedding
        query_vector = self.create_query_embedding(query)
        
        # Search the index
        distances, indices = self.index.search(
            query_vector.reshape(1, -1).astype('float32'), 
            k
        )
        
        # Map results back to chunk IDs
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  # FAISS returns -1 for no match
                chunk_id = self.chunk_ids[idx]
                results.append((chunk_id, float(dist)))
                
        return results

    def save_index(self, index_path: str):
        """Save FAISS index and chunk mappings"""
        if self.index is not None:
            # Save the FAISS index
            faiss.write_index(self.index, index_path)
            
            # Save chunk ID mappings
            mapping_path = index_path + '.mapping'
            np.save(mapping_path, np.array(self.chunk_ids))

    def load_index(self, index_path: str):
        """Load FAISS index and chunk mappings"""
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            
            # Load chunk ID mappings
            mapping_path = index_path + '.mapping'
            if os.path.exists(mapping_path):
                self.chunk_ids = np.load(mapping_path).tolist()

def process_embeddings(db_path: str, doc_id: str, index_path: str):
    """Main function to process embeddings"""
    print("\n[3/3] Creating embeddings...")
    try:
        # Initialize handlers
        db_handler = ChunkDBHandler(db_path)
        embedding_handler = EmbeddingHandler()

        # Check if embeddings already exist
        if os.path.exists(index_path) and os.path.exists(index_path + '.mapping'):
            print("→ Found existing embeddings, loading index...")
            embedding_handler.load_index(index_path)
            print("✓ Loaded existing embeddings index")
            return True

        # Get chunks from database
        chunks = db_handler.get_chunks(doc_id)
        if not chunks:
            print("No chunks found in database")
            return False

        # Create embeddings
        print("→ Generating new embeddings...")
        embeddings = embedding_handler.create_chunk_embeddings(chunks)

        # Build and save index
        print("→ Building optimized FAISS index...")
        embedding_handler.build_faiss_index(embeddings)
        embedding_handler.save_index(index_path)

        # Store embedding metadata in database
        db_handler.store_embedding_metadata(doc_id, {
            'dimension': embedding_handler.dimension,
            'index_path': index_path
        })

        print(f"✓ Created embeddings for {len(chunks)} chunks")
        print(f"✓ Saved optimized FAISS index to {index_path}")
        return True

    except Exception as e:
        print(f"✗ Error during embedding creation: {e}")
        return False 