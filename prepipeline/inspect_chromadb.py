import chromadb
from rich.console import Console
import os
from pathlib import Path
from chromadb.utils import embedding_functions

console = Console()

def inspect_chromadb():
    try:
        # Use correct path
        chroma_path = Path("backend/processed_data/chromadb")
        
        if not chroma_path.exists():
            console.print(f"[red]ChromaDB not found at: {chroma_path}[/red]")
            return
            
        console.print(f"[green]Found ChromaDB at: {chroma_path}[/green]")
        
        # Initialize client with embedding function
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-mpnet-base-v2"
        )
        client = chromadb.PersistentClient(path=str(chroma_path))
        collections = client.list_collections()
        
        console.print(f"\nFound {len(collections)} collections")
        
        # Get the non-empty collection
        collection_name = "ts_24501_chunks_20250321_131009"  # The collection with 6874 chunks
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        
        console.print(f"\n[green]Inspecting collection: {collection_name} ({collection.count()} chunks)[/green]")
        
        # Get some sample chunks
        results = collection.get(
            limit=3,  # Get 3 sample chunks
            include=["documents", "metadatas"]
        )
        
        if results["documents"]:
            for i, (doc, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
                console.print(f"\n[yellow]Sample chunk {i+1}:[/yellow]")
                console.print("[cyan]Content:[/cyan]")
                console.print(doc)
                console.print("\n[blue]Metadata:[/blue]")
                console.print(metadata)
                
            # Try to get a specific registration-related chunk
            reg_results = collection.query(
                query_texts=["Registration procedure for initial registration"],
                n_results=1,
                include=["documents", "metadatas"]
            )
            
            if reg_results["documents"][0]:
                console.print("\n[yellow]Registration procedure chunk:[/yellow]")
                console.print("[cyan]Content:[/cyan]")
                console.print(reg_results["documents"][0][0])
                console.print("\n[blue]Metadata:[/blue]")
                console.print(reg_results["metadatas"][0][0])

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    inspect_chromadb() 