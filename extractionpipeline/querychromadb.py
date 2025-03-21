import chromadb
from rich.console import Console
from typing import List, Dict
import json
from datetime import datetime
from pathlib import Path
import os
from chromadb.utils import embedding_functions

console = Console()

class ChromaDBQuerier:
    def __init__(self):
        try:
            # Store chroma_path as class variable
            self.chroma_path = r"C:\Users\mello\3gpp\backend\prepipeline\backend\processed_data\chromadb"
            
            # Use the same embedding model as used in semantic_chunking.py
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-mpnet-base-v2"  # Same model used for creating chunks
            )
            
            if not os.path.exists(self.chroma_path):
                raise Exception(f"ChromaDB directory not found at: {self.chroma_path}")
                
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
            collections = self.chroma_client.list_collections()
            
            if not collections:
                raise Exception("No collections found in ChromaDB")
                
            # Get the collection with data (skip empty ones)
            for collection in collections:
                # Get collection with the correct embedding function
                collection_obj = self.chroma_client.get_collection(
                    name=collection,
                    embedding_function=self.embedding_function
                )
                if collection_obj.count() > 0:
                    self.collection = collection_obj
                    break
                    
            if not hasattr(self, 'collection'):
                raise Exception("No non-empty collections found")
                
            console.print(f"[green]Successfully initialized ChromaDB with collection: {self.collection.name}[/green]")
            console.print(f"[green]Number of chunks: {self.collection.count()}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error initializing ChromaDB: {str(e)}[/red]")
            raise

    def search_registration_chunks(self, min_similarity: float = 0.5) -> Dict:
        try:
            queries = [
                "Retrieve all procedures related to user registration and mobility in TS 24.501",
                "Registration procedure types and requirements",
                "Initial registration procedure",
                "Mobility registration update procedure",
                "Periodic registration update procedure",
                "Emergency registration procedure",
                "Registration accept and complete procedure",
                "Registration reject and failure handling",
                "5GMM registration states and state transitions",
                "UE and AMF registration requirements",
                "Registration area update triggers",
                "Registration procedure initiation"
            ]
            
            all_results = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Fix output directory path
            output_dir = Path(__file__).parent.parent / "processed_data" / "query_results"
            output_dir.mkdir(exist_ok=True)
            
            for query in queries:
                console.print(f"\n[yellow]Searching for: {query}[/yellow]")
                
                results = self.collection.query(
                    query_texts=[query],
                    n_results=1000,
                    include=["documents", "metadatas", "distances"]
                )
                
                matches_found = 0
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    similarity = ((1 - distance) * 100)
                    if similarity >= (min_similarity * 100):
                        matches_found += 1
                        result_key = f"{query}_result_{i}"
                        
                        all_results[result_key] = {
                            "query": query,
                            "chunk": doc,  # Full chunk content
                            "metadata": metadata,
                            "similarity": f"{similarity:.2f}%"
                        }
                        
                        # Print result preview
                        console.print(f"\n[green]Result {matches_found} (Similarity: {similarity:.2f}%)[/green]")
                        console.print(f"[blue]Preview of chunk {metadata.get('chunk_number')}:[/blue]")
                        preview = doc[:200] + "..." if len(doc) > 200 else doc
                        console.print(f"[cyan]{preview}[/cyan]")
                
                console.print(f"[blue]Found {matches_found} chunks with similarity >= {min_similarity * 100}%[/blue]")
            
            # Save results to the correct directory
            output_file = output_dir / f"registration_mobility_chunks_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)
            
            console.print(f"\n[green]✓ Saved {len(all_results)} results to {output_file}[/green]")
            
            return all_results
            
        except Exception as e:
            console.print(f"[red]Error during search: {str(e)}[/red]")
            raise

    def custom_search(self, query: str, top_k: int = 15) -> Dict:
        """Custom search method across all collections"""
        try:
            all_results = {}
            
            for collection_info in self.collections:
                collection = self.chroma_client.get_collection(name=collection_info.name)
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                all_results[collection_info.name] = {
                    "documents": results["documents"][0],
                    "metadatas": results["metadatas"][0],
                    "distances": results["distances"][0]
                }
            
            return all_results
            
        except Exception as e:
            console.print(f"[red]Error during custom search: {str(e)}[/red]")
            raise

if __name__ == "__main__":
    try:
        querier = ChromaDBQuerier()
        results = querier.search_registration_chunks()
    except Exception as e:
        console.print(f"[red]Failed to execute query: {str(e)}[/red]") 