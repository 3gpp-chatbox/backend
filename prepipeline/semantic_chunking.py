# semantic_chunking.py

from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import json
from pathlib import Path
import os
from rich.console import Console
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import torch
from datetime import datetime

console = Console()

class SemanticChunker:
    def __init__(self, model_name="all-mpnet-base-v2", threshold=0.75, max_chunk_size=2500):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold
        self.max_chunk_size = max_chunk_size
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="backend/processed_data/chromadb")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
        
    def _get_or_create_collection(self, collection_name: str):
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except:
            # Create new collection if it doesn't exist
            collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        return collection

    def _semantic_grouping(self, chunks: List[str]) -> List[str]:
        if not chunks:
            return []

        collection_name = "ts_24501_chunks"  # You can make this parameter dynamic
        collection = self._get_or_create_collection(collection_name)
        
        # Check if we already have these chunks in the database
        console.print("[yellow]Checking existing embeddings in ChromaDB...[/yellow]")
        
        # Generate IDs for chunks
        chunk_ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Add chunks to ChromaDB if they don't exist
        existing_ids = collection.get(ids=chunk_ids)["ids"]
        new_chunk_indices = [i for i, chunk_id in enumerate(chunk_ids) if chunk_id not in existing_ids]
        
        if new_chunk_indices:
            new_chunks = [chunks[i] for i in new_chunk_indices]
            new_ids = [chunk_ids[i] for i in new_chunk_indices]
            
            console.print(f"[yellow]Adding {len(new_chunks)} new chunks to ChromaDB...[/yellow]")
            collection.add(
                documents=new_chunks,
                ids=new_ids,
                metadatas=[{"source": "TS_24.501", "chunk_number": i} for i in range(len(new_chunks))]
            )
        
        # Get embeddings for all chunks
        console.print("[yellow]Retrieving embeddings...[/yellow]")
        all_embeddings = collection.get(
            ids=chunk_ids,
            include=["embeddings"]
        )["embeddings"]
        
        # Convert to tensor for similarity calculation
        sentence_embeddings = torch.tensor(all_embeddings)
        
        console.print("[yellow]Calculating similarity matrix...[/yellow]")
        similarity_matrix = util.pytorch_cos_sim(sentence_embeddings, sentence_embeddings)
        
        visited = [False] * len(chunks)
        grouped_chunks = []
        
        console.print("[yellow]Grouping similar chunks...[/yellow]")
        for i in tqdm(range(len(chunks))):
            if not visited[i]:
                similar_chunks = [chunks[i]]
                visited[i] = True
                
                # First collect all similar chunks
                for j in range(i + 1, len(chunks)):
                    if not visited[j] and similarity_matrix[i][j] > self.threshold:
                        similar_chunks.append(chunks[j])
                        visited[j] = True
                
                # Then create appropriately sized chunks
                current_chunk = []
                current_size = 0
                
                for chunk in similar_chunks:
                    if current_size + len(chunk) <= self.max_chunk_size:
                        current_chunk.append(chunk)
                        current_size += len(chunk)
                    else:
                        if current_chunk:
                            grouped_chunks.append(" ".join(current_chunk))
                        current_chunk = [chunk]
                        current_size = len(chunk)
                
                if current_chunk:
                    grouped_chunks.append(" ".join(current_chunk))
                
                if len(grouped_chunks) % 100 == 0:
                    console.print(f"[blue]Created {len(grouped_chunks)} semantic chunks so far...[/blue]")
        
        return grouped_chunks

    def process_chunks(self, chunks: List[str]) -> List[str]:
        """Process existing chunks through semantic grouping."""
        return self._semantic_grouping(chunks)

    def process_and_save_chunks(self, chunks: List[str], output_base_path: str, batch_size=500):
        """Process chunks in batches to manage memory and show better progress"""
        if not chunks:
            return []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_name = f"ts_24501_chunks_{timestamp}"
        collection = self._get_or_create_collection(collection_name)
        
        # Process in batches
        total_batches = (len(chunks) + batch_size - 1) // batch_size
        all_grouped_chunks = []
        all_chunk_groups = []
        
        console.print(f"[yellow]Processing {len(chunks)} chunks in {total_batches} batches...[/yellow]")
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, len(chunks))
            batch_chunks = chunks[start_idx:end_idx]
            
            console.print(f"[blue]Processing batch {batch_idx + 1}/{total_batches} (chunks {start_idx} to {end_idx})[/blue]")
            
            # Generate IDs and metadata for this batch
            chunk_ids = [f"chunk_{i}" for i in range(start_idx, end_idx)]
            metadatas = [{
                "source": "TS_24.501",
                "chunk_number": i,
                "processing_date": timestamp,
                "model_used": self.model_name,
                "similarity_threshold": self.threshold,
                "batch": batch_idx
            } for i in range(start_idx, end_idx)]
            
            # Generate embeddings for this batch
            console.print("[yellow]Generating embeddings for current batch...[/yellow]")
            embeddings = self.model.encode(batch_chunks, convert_to_tensor=True, show_progress_bar=True)
            
            # Save batch to ChromaDB
            console.print("[yellow]Saving batch to ChromaDB...[/yellow]")
            collection.add(
                documents=batch_chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                ids=chunk_ids
            )

            # Calculate similarity matrix for this batch
            console.print("[yellow]Calculating similarities for current batch...[/yellow]")
            similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
            
            # Group chunks within this batch
            visited = [False] * len(batch_chunks)
            batch_grouped_chunks = []
            batch_chunk_groups = []
            
            for i in tqdm(range(len(batch_chunks))):
                if not visited[i]:
                    current_group = [start_idx + i]
                    similar_chunks = [batch_chunks[i]]
                    visited[i] = True
                    
                    for j in range(i + 1, len(batch_chunks)):
                        if not visited[j] and similarity_matrix[i][j] > self.threshold:
                            similar_chunks.append(batch_chunks[j])
                            current_group.append(start_idx + j)
                            visited[j] = True
                    
                    # Create appropriately sized chunks
                    current_chunk = []
                    current_size = 0
                    
                    for chunk in similar_chunks:
                        if current_size + len(chunk) <= self.max_chunk_size:
                            current_chunk.append(chunk)
                            current_size += len(chunk)
                        else:
                            if current_chunk:
                                batch_grouped_chunks.append(" ".join(current_chunk))
                                batch_chunk_groups.append(current_group)
                            current_chunk = [chunk]
                            current_size = len(chunk)
                    
                    if current_chunk:
                        batch_grouped_chunks.append(" ".join(current_chunk))
                        batch_chunk_groups.append(current_group)
            
            all_grouped_chunks.extend(batch_grouped_chunks)
            all_chunk_groups.extend(batch_chunk_groups)
            
            console.print(f"[green]Completed batch {batch_idx + 1}/{total_batches}[/green]")
        
        return all_grouped_chunks

def load_chunks_from_markdown(file_path: str) -> List[str]:
    """Loads chunks from the markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by the long dash separator
        separator = "--------------------------------------------------"
        sections = content.split(separator)
        
        # Process each section
        chunks = []
        for section in sections:
            section = section.strip()
            # Check for any number of # characters at the start of any line
            if section and any(line.strip().startswith('#') for line in section.split('\n')):
                chunks.append(section)
        
        # Debug information
        console.print(f"[green]✓ Loaded {len(chunks)} chunks from {file_path}[/green]")
        
        # Count headers by level
        header_counts = {i: 0 for i in range(1, 13)}  # Count headers from # to ############
        for chunk in chunks:
            for line in chunk.split('\n'):
                if line.strip().startswith('#'):
                    level = len(line.strip().split()[0])  # Count number of #'s
                    if level in header_counts:
                        header_counts[level] += 1
        
        # Show header level distribution
        console.print("\n[yellow]Header level distribution:[/yellow]")
        for level, count in header_counts.items():
            if count > 0:
                console.print(f"{'#' * level}: {count} headers")
        
        if len(chunks) != 6874:
            console.print(f"\n[red]Warning: Expected 6874 chunks but found {len(chunks)}[/red]")
            console.print("\n[yellow]Sample of first few chunks:[/yellow]")
            for i, chunk in enumerate(chunks[:3]):
                first_line = next((line for line in chunk.split('\n') if line.strip()), '')
                console.print(f"Chunk {i+1} first line: {first_line}")
        
        return chunks
        
    except Exception as e:
        console.print(f"[red]Error loading chunks from {file_path}: {str(e)}[/red]")
        raise

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
        # Setup paths
        backend_dir = Path(__file__).parent.parent
        input_markdown = str(backend_dir / "processed_data" / "chunked_TS_24.501.md")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_markdown = str(backend_dir / "processed_data" / f"semantic_TS_24.501_{timestamp}.md")
        
        # Initialize chunker
        chunker = SemanticChunker()
        
        # Load and process all chunks
        input_chunks = load_chunks_from_markdown(input_markdown)
        console.print(f"[yellow]Processing all {len(input_chunks)} chunks...[/yellow]")
        
        # Process the entire dataset
        semantic_chunks = chunker.process_and_save_chunks(input_chunks, output_markdown)
        
        # Explicitly save to markdown file
        save_semantic_chunks(semantic_chunks, output_markdown)
        
        console.print(f"[green]✓ Processing complete![/green]")
        console.print(f"[green]✓ Saved to: {output_markdown}[/green]")
        console.print(f"[blue]Original chunks: {len(input_chunks)}, Semantic chunks: {len(semantic_chunks)}[/blue]")
            
    except Exception as e:
        console.print(f"[red]Error during processing: {str(e)}[/red]")
        raise