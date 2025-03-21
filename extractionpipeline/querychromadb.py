import chromadb
from rich.console import Console
from typing import List, Dict
import json
from datetime import datetime
from pathlib import Path

console = Console()

class ChromaDBQuerier:
    def __init__(self):
        try:
            self.chroma_client = chromadb.PersistentClient(path="backend/processed_data/chromadb")
            self.collections = self.chroma_client.list_collections()
            if not self.collections:
                raise Exception("No collections found in ChromaDB")
            
            console.print(f"[green]Successfully initialized ChromaDB with {len(self.collections)} collections[/green]")
            for coll in self.collections:
                count = self.chroma_client.get_collection(name=coll.name).count()
                console.print(f"[blue]Collection: {coll.name} ({count} chunks)[/blue]")
                
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
            
            # Search across all collections
            for collection_info in self.collections:
                collection = self.chroma_client.get_collection(name=collection_info.name)
                console.print(f"\n[yellow]Searching in collection: {collection_info.name}[/yellow]")
                
                for query in queries:
                    console.print(f"\n[yellow]Searching for: {query}[/yellow]")
                    
                    results = collection.query(
                        query_texts=[query],
                        n_results=1000,  # High number to get all potential matches
                        include=["documents", "metadatas", "distances"]
                    )
                    
                    # Process results using similarity threshold
                    matches_found = 0
                    for i, (doc, metadata, distance) in enumerate(zip(
                        results["documents"][0],
                        results["metadatas"][0],
                        results["distances"][0]
                    )):
                        similarity = ((1 - distance) * 100)
                        if similarity >= (min_similarity * 100):
                            matches_found += 1
                            result_key = f"{collection_info.name}_{query}_result_{i}"
                            all_results[result_key] = {
                                "collection": collection_info.name,
                                "query": query,
                                "chunk": doc,
                                "metadata": metadata,
                                "similarity": f"{similarity:.2f}%"
                            }
                            
                            # Print result with more details
                            console.print(f"\n[green]Result {matches_found} (Similarity: {similarity:.2f}%)[/green]")
                            console.print(f"[blue]First few lines:[/blue]")
                            lines = doc.split('\n')[:3]
                            for line in lines:
                                if line.strip():
                                    console.print(f"[cyan]{line.strip()}[/cyan]")
                    
                    console.print(f"[blue]Found {matches_found} chunks with similarity >= {min_similarity * 100}%[/blue]")
            
            # Save results to file with timestamp
            output_dir = Path("backend/processed_data/query_results")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"registration_mobility_chunks_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)
            
            console.print(f"\n[green]✓ Saved {len(all_results)} results to {output_file}[/green]")
            
            # Print summary by collection
            console.print("\n[yellow]Summary of findings by collection:[/yellow]")
            for collection_info in self.collections:
                collection_results = {k: v for k, v in all_results.items() if k.startswith(collection_info.name)}
                console.print(f"[blue]Collection '{collection_info.name}': {len(collection_results)} relevant chunks found[/blue]")
            
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