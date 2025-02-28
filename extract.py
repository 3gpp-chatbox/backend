import os
import re
import json
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv
from rich.console import Console
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback
from pathlib import Path
import sys
import threading
import subprocess
from semantic_chunking import SemanticChunker, save_semantic_chunks
# Initialize console for better output
console = Console()

# Load environment variables
load_dotenv(override=True)

# Configuration
INPUT_MD_FILE = os.path.join("processed_data", "semantic_chunks.md")  # Use semantic_chunks.md instead of .txt
PROCESSED_DATA_FOLDER = os.path.join("processed_data")
CHUNK_SIZE = 4000
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.json")
OUTPUT_MD_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.md")
INTERMEDIATE_BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3

EXTRACTION_PROMPT = """Analyze the following text and extract information about the 5G network initial registration procedure.
Return the information in a valid JSON format exactly as shown in the template below. Focus on capturing the sequential flow
of the registration procedure, where each step is clearly linked to the next step. Network elements and states will be the nodes,
and the transitions and events will be the relationships(edges) with clear sequence numbers. Network elements and states will be the nodes
and the transitions and events will be the relationships(edges).Edges are labeled with the type of relationship (e.g. SENDS_MESSAGES_TO, TRANSITIONS_TO, etc.).
Do not include any other text or explanations outside the JSON structure. DO NOT INCLUDE ANY OTHER PROCEDURES OR SUBPROCEDURES EXCEPT FOR THE INITIAL REGISTRATION PROCEDURE.

Extract the following information:

1. Network Elements:
    - Identify network elements (UE, AMF, SMF, UPF, PCF, NRF)
    - Include their roles and descriptions

2. States:
    - Identify states in the registration procedure (5GMM-NULL, 5GMM-REGISTERED, etc.)
    - Classify as INITIAL, INTERMEDIATE, or FINAL
    - Include descriptions

3. Registration Flow:
    - Identify each step in the registration procedure
    - Include sequence numbers for each step
    - Identify the source and destination elements for each message
    - Include the state changes at each step
    - Include the message being sent
    - Include the trigger for the message
    - Include the conditions for the message
    - Include the timing for the message
    - Include the type of relationship (e.g. SENDS_MESSAGES_TO, TRANSITIONS_TO, etc.)
    -


Return the response in this EXACT JSON structure:
{
    "network_elements": [
        {
            "name": "element name",
            "type": "Network Element",
            "description": "description"
        }
    ],
    "states": [
        {
            "name": "state name",
            "type": "INITIAL/INTERMEDIATE/FINAL",
            "description": "description"
        }
    ],
    "registration_flow": [
        {
            "sequence_number": 1,
            "step_name": "Initial Registration Request",
            "source_element": "UE",
            "destination_element": "AMF",
            "message": "Registration Request",
            "source_state": "5GMM-NULL",
            "destination_state": "5GMM-REGISTERING",
            "description": "UE initiates registration procedure",
            "trigger": "UE powers on",
            "conditions": ["UE in coverage area", "Valid USIM"],
            "timing": "T3510 starts"
        },
        {
            "sequence_number": 2,
            "step_name": "AMF Authentication",
            "source_element": "AMF",
            "destination_element": "UE",
            "message": "Authentication Request",
            "source_state": "5GMM-REGISTERING",
            "destination_state": "5GMM-REGISTERING-AUTHENTICATING",
            "description": "AMF initiates authentication procedure",
            "trigger": "Valid Registration Request received",
            "conditions": ["UE identity verified"],
            "timing": "T3560 starts"
        }
    ],
    "metadata": {
        "procedure_name": "Initial Registration",
        "total_steps": 2,
        "source": "document reference"
    }
}

The registration_flow array should contain ALL steps in the registration procedure in sequential order.
Each step must include:
- A unique sequence number
- Clear source and destination elements
- The message being sent
- State changes (if any)
- Triggers, conditions, and timing information


Text to analyze:
"""
RELEVANT_KEYWORDS = [
    "registration procedure",
    "5GMM",
    "initial registration",
    "UE registration",
    "AMF",
    "SMF",
    "registration accept",
    "registration request"
]

def initialize_llm():
    """Initialize LLM with error handling."""
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("Missing Google API key. Please check your .env file.")

        console.print(f"[blue]Using Google Gemini: {LLM_MODEL}[/blue]")
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=0,
            max_output_tokens=2048
        )
        return llm

    except Exception as e:
        console.print(f"[red]Error initializing LLM: {str(e)}[/red]")
        raise

def ensure_folders_exist():
    """Create necessary folders if they don't exist."""
    folders = [
        PROCESSED_DATA_FOLDER
    ]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        console.print(f"[blue]Ensuring folder exists: {folder}[/blue]")

def save_completion_marker():
    """Save a marker file to indicate completion of processing."""
    try:
        marker_file = os.path.join(PROCESSED_DATA_FOLDER, "extraction_complete.json")
        completion_data = {
            "timestamp": datetime.now().isoformat(),
            "status": "complete"
        }
        with open(marker_file, 'w') as f:
            json.dump(completion_data, f, indent=2)
        console.print(f"[green]✓ Saved completion marker to {marker_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving completion marker: {str(e)}[/red]")

def process_md_chunks(md_file_path: str, llm) -> List[Dict]:
    """Process semantic chunks from markdown file."""
    try:
        console.print(f"[blue]Processing {md_file_path}...[/blue]")
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Split on "## Semantic Chunk" headers
        chunks = md_content.split("## Semantic Chunk")[1:]  # Skip the first empty part
        chunks = [chunk.split("---")[0].strip() for chunk in chunks]  # Get content before "---"
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]  # Remove empty chunks

        console.print(f"[blue]Found {len(chunks)} chunks to process[/blue]")
        if not chunks:
            console.print("[yellow]No chunks found. Check if the file format is correct.[/yellow]")
            console.print(f"[yellow]File contents preview: {md_content[:200]}...[/yellow]")

        results = []
        for chunk_index, chunk in enumerate(chunks):
            doc = Document(page_content=chunk, metadata={"source": md_file_path, "chunk_index": chunk_index, "total_chunks": len(chunks)})
            chunk_result = process_chunk(doc, llm)
            if chunk_result:
                results.append(chunk_result)

            # Save intermediate results every INTERMEDIATE_BATCH_SIZE chunks
            if (chunk_index + 1) % INTERMEDIATE_BATCH_SIZE == 0:
                intermediate_file = os.path.join(PROCESSED_DATA_FOLDER, f"intermediate_results_{chunk_index + 1}.json")
                save_results(results, intermediate_file)
                console.print(f"[blue]Intermediate results saved to {intermediate_file}[/blue]")

        return results

    except Exception as e:
        console.print(f"[red]Error processing markdown file {md_file_path}: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return []

def process_chunk(doc: Document, llm: Any) -> Dict:
    """Process a document chunk and return extracted information."""
    try:
        chunk_info = f"chunk {doc.metadata['chunk_index'] + 1}/{doc.metadata['total_chunks']}"

        # Skip chunks that don't contain relevant information
        if not is_relevant_chunk(doc.page_content):
            console.print(f"[yellow]Skipping irrelevant chunk: {chunk_info}[/yellow]")
            return None

        console.print(f"[blue]Analyzing registration flows in: {doc.metadata['source']} ({chunk_info})[/blue]")

        # Create the full prompt
        full_prompt = EXTRACTION_PROMPT + doc.page_content

        try:
            extracted_data = call_llm_with_retry(llm, full_prompt)

            # Validate the structure of extracted data
            required_fields = ['network_elements', 'states', 'transitions',
                               'network_element_relationships', 'triggers',
                               'conditions', 'timing']

            # Ensure all required fields exist
            for field in required_fields:
                if field not in extracted_data:
                    extracted_data[field] = []

            # Only keep the chunk if it found meaningful information
            if not any(extracted_data.get(field) for field in ['network_elements', 'states', 'transitions']):
                console.print(f"[yellow]No relevant information found in chunk {chunk_info}[/yellow]")
                return None

            extracted_data['metadata'] ={
                'source': doc.metadata['source'],
                'chunk_index': doc.metadata['chunk_index'],
                'total_chunks': doc.metadata['total_chunks'],
                'extraction_time': datetime.now().isoformat()
            }

            console.print(f"[green]✓ Found and processed state flows in chunk {chunk_info}[/green]")
            return extracted_data

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                console.print(f"[red]API quota exceeded after retries. Skipping chunk.[/red]")
                return None
            console.print(f"[yellow]Failed to process chunk: {str(e)}[/yellow]")
            return None

    except Exception as e:
        console.print(f"[red]Error processing chunk: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return None

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    reraise=True
)
def call_llm_with_retry(llm: Any, prompt: str) -> Dict:
    """Call LLM with retry logic and rate limiting."""
    try:
        time.sleep(RATE_LIMIT_DELAY)
        response = llm.invoke(prompt)

        if not response.content:
            raise ValueError("Empty response from LLM")

        # Clean up the response text
        response_text = response.content.strip()
        
        # Try to find and extract the JSON part
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end != 0:
            try:
                json_str = response_text[start:end]
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                console.print(f"[yellow]Failed to parse JSON: {str(e)}[/yellow]")
        
        # Return empty structure if parsing fails
        return {
            "network_elements": [],
            "states": [],
            "transitions": [],
            "network_element_relationships": [],
            "triggers": [],
            "conditions": [],
            "timing": []
        }

    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            console.print(f"[yellow]API quota exceeded. Waiting before retry...[/yellow]")
            time.sleep(RATE_LIMIT_DELAY * 5)
            raise
        console.print(f"[red]Error calling LLM: {str(e)}[/red]")
        raise

def is_relevant_chunk(text: str) -> bool:
    """Check if chunk contains relevant information about registration procedure."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in RELEVANT_KEYWORDS)

def save_results(results: List[Dict], output_file: str):
    """Save results to JSON file."""
    try:
        output_data = {
            'metadata': {
                'extraction_time': datetime.now().isoformat(),
                'total_documents': len(results)
            },
            'results': results
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        console.print(f"[green]✓ Results saved to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving results: {str(e)}[/red]")

def save_results_to_md(results: List[Dict], output_file: str):
    """Save results to markdown file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                if result:
                    f.write(f"# Extracted Data from {result['metadata']['source']} (Chunk {result['metadata']['chunk_index'] + 1})\n\n")
                    for section, items in result.items():
                        if section == 'metadata':
                            continue
                        f.write(f"## {section.replace('_', ' ').title()}\n\n")
                        if isinstance(items, list):
                            for item in items:
                                f.write(json.dumps(item, indent=2, ensure_ascii=False) + "\n\n")
                        else:
                            f.write(json.dumps(items, indent=2, ensure_ascii=False) + "\n\n")
        console.print(f"[green]✓ Results saved to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving results to markdown: {str(e)}[/red]")

def main():
    try:
        # Ensure folders exist
        ensure_folders_exist()

        # Initialize LLM
        llm = initialize_llm()

        # Process the markdown file
        all_results = process_md_chunks(INPUT_MD_FILE, llm)

        # Save final results to JSON and MD file
        save_results(all_results, OUTPUT_FILE)
        save_results_to_md(all_results, OUTPUT_MD_FILE)
        console.print("[green]✓ Processing completed successfully[/green]")

    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")
        console.print(traceback.format_exc())

    finally:
        # Ensure completion marker is saved even if there's an error
        save_completion_marker()

if __name__ == "__main__":
    main()
