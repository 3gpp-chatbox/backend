# semantic_chunking.py

from sentence_transformers import SentenceTransformer, util
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.cluster import KMeans
import numpy as np
from typing import List, Dict
import json
from pathlib import Path
import os
from rich.console import Console

console = Console()

class SemanticChunker:
    def __init__(self, model_name="all-mpnet-base-v2", chunk_size=1500, threshold=0.75):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = chunk_size
        self.threshold = threshold
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def process_chunks(self, chunks: List[str]) -> List[str]:
        """Process existing chunks through semantic grouping."""
        return self._semantic_grouping(chunks)
    
    def _semantic_grouping(self, chunks: List[str]) -> List[str]:
        """Group semantically similar chunks."""
        if not chunks:
            return []
            
        # Create embeddings
        sentence_embeddings = self.model.encode(chunks, convert_to_tensor=True)
        similarity_matrix = util.pytorch_cos_sim(sentence_embeddings, sentence_embeddings)
        
        # Group similar chunks
        visited = [False] * len(chunks)
        grouped_chunks = []
        
        for i in range(len(chunks)):
            if not visited[i]:
                group = [chunks[i]]
                visited[i] = True
                for j in range(i + 1, len(chunks)):
                    if similarity_matrix[i][j] > self.threshold:
                        group.append(chunks[j])
                        visited[j] = True
                grouped_chunks.append(" ".join(group))
        
        return grouped_chunks

def load_chunks_from_markdown(file_path: str) -> List[str]:
    """Loads chunks from the markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract chunks using markdown headers
        chunks = []
        chunk_sections = content.split("##")[1:]  # Split on chunk headers
        
        for section in chunk_sections:
            # Extract the chunk content (everything until the next delimiter or end)
            chunk_content = section.split("---")[0].strip()
            if chunk_content:
                chunks.append(chunk_content)
                
        console.print(f"[green]✓ Loaded {len(chunks)} chunks from {file_path}[/green]")
        return chunks
    except Exception as e:
        console.print(f"[red]Error loading chunks from {file_path}: {str(e)}[/red]")
        return []

def save_semantic_chunks(chunks: List[str], output_file: str):
    """Save semantic chunks in md format."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save as Markdown
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"## Semantic Chunk {i}\n\n")
                f.write(chunk + "\n\n")
                f.write("---\n\n")
        
        console.print(f"[green]✓ Semantic chunks saved to: {output_file}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error saving semantic chunks: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        # Get the backend directory path (two levels up from this script)
        backend_dir = Path(__file__).parent.parent
        
        # Define input and output paths relative to backend directory
        input_markdown = str(backend_dir / "processed_data" / "chunked_TS_24.501.md")
        output_markdown = str(backend_dir / "processed_data" / "semantic_TS_24.501.md")
        
        print(f"Reading chunked markdown from: {input_markdown}")
        print(f"Will save semantic chunks to: {output_markdown}")
        
        # Initialize chunker
        chunker = SemanticChunker()
        
        # Load chunks from markdown
        input_chunks = load_chunks_from_markdown(input_markdown)
        if not input_chunks:
            console.print("[red]No chunks found in input file[/red]")
            exit(1)
        
        # Process chunks
        semantic_chunks = chunker.process_chunks(input_chunks)
        
        # Save results
        if semantic_chunks:
            save_semantic_chunks(semantic_chunks, output_markdown)
            console.print(f"[green]✓ Processing complete![/green]")
            console.print(f"[blue]Original chunks: {len(input_chunks)}, Semantic chunks: {len(semantic_chunks)}[/blue]")
        else:
            console.print("[yellow]No semantic chunks were generated[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error during processing: {str(e)}[/red]")
        raise