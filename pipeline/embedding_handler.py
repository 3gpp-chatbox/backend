from typing import List, Dict
import json
import chromadb
import re

class DBHandler:
    def __init__(self, model_name: str = "all-mpnet-base-v2", persist_directory: str = "DB/chroma_db"):
        """Initialize ChromaDB connection and embedding model"""
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.model_name = model_name
        self.batch_size = 32

    def _create_or_get_collection(self, collection_name: str, metadata: Dict = None):
        """Create or get existing collection"""
        try:
            collection = self.chroma_client.get_collection(collection_name)
            print(f"Using existing collection: {collection_name}")
        except:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata=metadata or {"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {collection_name}")
        return collection

    def store_chunks(self, chunks: List[Dict], doc_id: str) -> int:
        """Store chunks with embeddings in ChromaDB"""
        try:
            print(f"\nProcessing {len(chunks)} chunks for storage...")
            
            # Delete existing collection if it exists and create a new one
            try:
                # Check and delete if exists
                self.chroma_client.get_collection(doc_id)
                self.chroma_client.delete_collection(doc_id)
                print(f"Deleted existing collection: {doc_id}")
            except:
                pass
            
            # Create new collection
            collection = self.chroma_client.create_collection(
                name=doc_id,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {doc_id}")
            
            # Prepare data for embedding
            ids = [str(i) for i in range(len(chunks))]
            texts = [f"{chunk['title']} {chunk['content']}".strip() for chunk in chunks]
            metadatas = [{
                'title': chunk['title'],
                'level': chunk['level'],
                'index': i
            } for i, chunk in enumerate(chunks)]

            # Add documents in batches
            total_batches = (len(texts) + self.batch_size - 1) // self.batch_size
            for i in range(0, len(texts), self.batch_size):
                batch_end = min(i + self.batch_size, len(texts))
                current_batch = (i // self.batch_size) + 1
                print(f"Processing batch {current_batch}/{total_batches} ({batch_end-i} chunks)")
                
                collection.add(
                    ids=ids[i:batch_end],
                    documents=texts[i:batch_end],
                    metadatas=metadatas[i:batch_end]
                )

            print(f"✓ Successfully processed all {len(chunks)} chunks")
            return len(chunks)
        except Exception as e:
            print(f"Error storing chunks: {e}")
            return 0

    def get_chunks(self, doc_id: str, query: str = None, n_results: int = 10) -> List[Dict]:
        """Retrieve chunks from ChromaDB with optional semantic search"""
        try:
            collection = self.chroma_client.get_collection(doc_id)
            
            if query:
                results = collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    include=["documents", "metadatas", "distances"]
                )
                chunks = []
                for doc, metadata, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity = 1 - (distance / 2)  # Convert cosine distance to similarity
                    chunks.append({
                        'title': metadata['title'],
                        'content': doc.replace(metadata['title'], '').strip(),
                        'level': metadata['level'],
                        'index': metadata['index'],
                        'collection': doc_id,
                        'similarity': similarity
                    })
                return chunks
            else:
                results = collection.get()
                return [{
                    'title': metadata['title'],
                    'content': doc.replace(metadata['title'], '').strip(),
                    'level': metadata['level'],
                    'index': metadata['index'],
                    'collection': doc_id
                } for doc, metadata in zip(results['documents'], results['metadatas'])]
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return []

    def store_procedure_metadata(self, metadata: Dict):
        """Store procedure metadata in ChromaDB"""
        try:
            collection_name = f"{metadata['doc_id']}_procedures"
            collection = self._create_or_get_collection(
                collection_name, 
                metadata={"type": "procedure_metadata"}
            )

            document_text = f"{metadata['procedure_name']}\n{metadata['description']}"
            collection.add(
                ids=[metadata['procedure_name']],
                documents=[document_text],
                metadatas=[{
                    'procedure_name': metadata['procedure_name'],
                    'description': metadata['description'],
                    'steps_file': metadata['steps_file'],
                    'related_3gpp_spec_sections': json.dumps(metadata['related_3gpp_spec_sections']),
                    'source_document_title': metadata['source_document_title'],
                    'source_chunk_ids': json.dumps(metadata['source_chunk_ids']),
                    'doc_id': metadata['doc_id'],
                    'similarity_score': metadata['similarity_score']
                }]
            )
            print(f"→ Stored metadata for procedure: {metadata['procedure_name']}")
            
        except Exception as e:
            print(f"Error storing procedure metadata: {e}")

    def get_procedure_metadata(self, doc_id: str, procedure_name: str = None) -> List[Dict]:
        """Retrieve procedure metadata from ChromaDB"""
        try:
            collection_name = f"{doc_id}_procedures"
            collection = self.chroma_client.get_collection(collection_name)
            
            if procedure_name:
                results = collection.get(ids=[procedure_name])
            else:
                results = collection.get()
            
            if not results['metadatas']:
                return []
                
            return [{
                'procedure_name': metadata['procedure_name'],
                'description': metadata['description'],
                'steps_file': metadata['steps_file'],
                'related_3gpp_spec_sections': json.loads(metadata['related_3gpp_spec_sections']),
                'source_document_title': metadata['source_document_title'],
                'source_chunk_ids': json.loads(metadata['source_chunk_ids']),
                'doc_id': metadata['doc_id'],
                'similarity_score': metadata['similarity_score']
            } for metadata in results['metadatas']]
            
        except Exception as e:
            print(f"Error retrieving procedure metadata: {e}")
            return []

    def hybrid_search(self, doc_id: str, query: str, n_results: int = 10, min_similarity: float = 0.5) -> List[Dict]:
        """
        Combines keyword matching and semantic search for better results.
        
        Args:
            doc_id: Document ID to search in
            query: Search query
            n_results: Maximum number of results to return
            min_similarity: Minimum similarity score threshold
        """
        try:
            # 1. Get semantic search results
            semantic_results = self.get_chunks(doc_id, query, n_results=n_results * 2)  # Get more results for filtering
            if not semantic_results:
                print("No semantic search results found")
                return []
            
            # 2. Prepare keyword patterns
            keywords = [k.lower() for k in query.split() if len(k) > 2]  # Skip very short words
            if not keywords:
                print("No valid keywords found in query")
                return semantic_results[:n_results]  # Return just semantic results if no keywords
            
            # 3. Score results using both semantic and keyword matching
            scored_results = []
            for chunk in semantic_results:
                # Get semantic similarity score
                semantic_score = chunk['similarity']  # Now properly included from get_chunks
                
                # Calculate keyword match score
                content = (chunk['title'] + ' ' + chunk['content']).lower()
                keyword_matches = sum(1 for k in keywords if k in content)
                keyword_score = keyword_matches / len(keywords)
                
                # Combine scores (weighted average - adjust weights as needed)
                combined_score = (semantic_score * 0.7) + (keyword_score * 0.3)
                
                if combined_score >= min_similarity:
                    scored_results.append({
                        **chunk,
                        'semantic_score': semantic_score,
                        'keyword_score': keyword_score,
                        'combined_score': combined_score
                    })
            
            # Sort by combined score and return top n_results
            scored_results.sort(key=lambda x: x['combined_score'], reverse=True)
            print(f"Found {len(scored_results)} results after hybrid scoring")
            return scored_results[:n_results]
            
        except Exception as e:
            print(f"Error in hybrid search: {e}")
            return []

# Keep old class for backward compatibility
class ChunkDBHandler(DBHandler):
    def __init__(self, db_path=None, persist_directory="DB/chroma_db"):
        super().__init__(persist_directory=persist_directory) 