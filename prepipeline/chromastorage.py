import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from pathlib import Path
from datetime import datetime
import json
from rich.console import Console
import re

console = Console()
BATCH_SIZE = 100  # Number of chunks processed per batch

class EmbeddingCreator:
    def __init__(self, model_name="all-mpnet-base-v2"):
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
            
            # Fix ChromaDB path to be in backend/processed_data
            chroma_path = Path(__file__).parent.parent / "processed_data" / "chromadb"
            self.chroma_client = chromadb.PersistentClient(path=str(chroma_path))
            
            console.print("[green]✓ Embedding model and ChromaDB initialized successfully.[/green]")
        except Exception as e:
            console.print(f"[red]Error initializing EmbeddingCreator: {str(e)}[/red]")
            raise

    def process_and_save_chunks(self, chunks: List[Dict], output_file: str):
        """Creates embeddings, saves chunks to ChromaDB, and writes metadata to markdown."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            collection_name = f"ts_24501_chunks_{timestamp}"
            
            # Create a ChromaDB collection
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"timestamp": timestamp}
            )

            processed_chunks = []
            for batch_num, i in enumerate(range(0, len(chunks), BATCH_SIZE)):
                batch = chunks[i:i + BATCH_SIZE]
                texts = [chunk["text"] for chunk in batch]
                section_ids = [f"chunk_{i + idx}" for idx in range(len(batch))]
                metadatas = [
                    {
                        "chunk_number": i + idx,
                        "batch": batch_num,
                        "processing_date": timestamp,
                        "model_used": "all-mpnet-base-v2",
                        "source": f"TS_24.501 Section {chunk['section']}"
                    }
                    for idx, chunk in enumerate(batch)
                ]

                # Add to ChromaDB
                collection.add(documents=texts, metadatas=metadatas, ids=section_ids)

                # Store processed chunks
                for idx, chunk in enumerate(batch):
                    processed_chunks.append({
                        "id": section_ids[idx],
                        "content": chunk["text"],
                        "metadata": metadatas[idx]
                    })

            # Save metadata and chunks to a markdown file
            output_path = Path(output_file)
            with open(output_path, "w", encoding="utf-8") as f:
                for chunk in processed_chunks:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"Chunk ID: {chunk['id']}\n")
                    f.write(f"Metadata: {json.dumps(chunk['metadata'], indent=2)}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(chunk["content"])
                    f.write("\n\n")

            console.print(f"[green]✓ Stored {len(processed_chunks)} chunks in ChromaDB[/green]")
            console.print(f"[green]✓ ChromaDB collection: {collection_name}[/green]")
            console.print(f"[green]✓ Markdown output saved: {output_file}[/green]")
        except Exception as e:
            console.print(f"[red]Error processing chunks: {str(e)}[/red]")
            raise

def read_chunks_from_file(file_path: str) -> List[Dict]:
    try:
        chunks = []
        current_chunk = []
        current_section = None
        last_seen_section = None  # Keep track of the last seen section
        in_chunk = False
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        console.print(f"[yellow]Debug: Total lines in file: {len(lines)}[/yellow]")
        
        for i, line in enumerate(lines):
            # Handle chunk separators
            if line.startswith('='*80):
                if in_chunk:  # End of chunk
                    if current_chunk:
                        chunk_text = '\n'.join(current_chunk).strip()
                        if chunk_text:
                            chunks.append({
                                'text': chunk_text,
                                'section': current_section or last_seen_section
                            })
                    current_chunk = []
                    in_chunk = False
                else:  # Start of chunk
                    in_chunk = True
                continue
            
            # Only process lines when we're inside a chunk
            if in_chunk:
                # Check for section numbers
                section_match = re.match(r'^(\d+(?:\.\d+)*)\s+', line)
                if section_match:
                    current_section = section_match.group(1)
                    last_seen_section = current_section  # Update last seen section
                
                if line.strip():
                    current_chunk.append(line.strip())
        
        console.print(f"[yellow]Debug Summary:[/yellow]")
        console.print(f"[yellow]- Chunks created: {len(chunks)}[/yellow]")
        
        return chunks
        
    except Exception as e:
        console.print(f"[red]Error reading chunks: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    try:
        base_dir = Path(__file__).parent.parent
        input_file = base_dir / "processed_data" / "chunked_TS_24.501.md"
        output_file = base_dir / "processed_data" / f"semantic_TS_24.501_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        # Check if input file exists
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        console.print(f"[yellow]✓ Input file size: {input_file.stat().st_size} bytes[/yellow]")

        # Read chunks
        chunks = read_chunks_from_file(str(input_file))
        console.print(f"[green]✓ Found {len(chunks)} chunks.[/green]")

        # Create embeddings and store in ChromaDB
        creator = EmbeddingCreator()
        creator.process_and_save_chunks(chunks, str(output_file))

    except Exception as e:
        console.print(f"[red]Failed to process embeddings: {str(e)}[/red]")
