import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.documents import Document
from pypdf import PdfReader
from rich.console import Console
from typing import List, Dict, Any, Set
import traceback
import json
from datetime import datetime
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import re
import hashlib
from neo4j import GraphDatabase
import subprocess
import threading
import sys
from pathlib import Path

# Initialize console for better output
console = Console()

# Load environment variables
load_dotenv(override=True)

# Configuration
PDF_FOLDER = os.path.join("data")
PROCESSED_DATA_FOLDER = os.path.join("processed_data")  # New folder for processed data
CHUNK_SIZE = 3000
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.json")
INTERMEDIATE_BATCH_SIZE = 10  # Save intermediate results every 10 chunks
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

EXTRACTION_PROMPT = """Analyze the following text and extract information about the 5G network initial registration procedure.
Return the information in a valid JSON format exactly as shown in the template below. Network elements and states will be the nodes
and the transitions and events will be the relationships(edges).Edges are labeled with the type of relationship (e.g. SENDS_MESSAGES_TO, TRANSITIONS_TO, etc.).
Do not include any other text or explanations outside the JSON structure.

Extract the following information:

1. Network Elements:
   - Identify network elements (UE, AMF, SMF, UPF, PCF, NRF)
   - Include their roles and descriptions

2. States:
   - Identify states in the registration procedure (5GMM-NULL, 5GMM-REGISTERED, etc.)
   - Classify as INITIAL, INTERMEDIATE, or FINAL
   - Include descriptions

3. Transitions:
   - Identify state transitions
   - Include triggers, conditions, and timing
   - Note any prerequisites

4. Network Element Relationships:
   - Identify dependencies between network elements
   - Include descriptions of how elements interact
   - Include descriptions of the relationships


5. Triggers:
   - Identify triggers for state transitions
   - Include descriptions of what triggers the transition

6. Conditions:
   - Identify conditions that must be met for state transitions
   - Include descriptions of the conditions

7. Timing:
   - Identify timing of state transitions
   - Include descriptions of the timing

Return the response in this exact JSON structure:
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
    "transitions": [
        {
            "from_state": "source state",
            "to_state": "target state",
            "trigger": "what triggers the transition",
            "condition": "conditions that must be met",
            "probability": "likelihood if specified"
        }
    ],
    "network_element_relationships": [
        {
            "element1": "element name",
            "element2": "element name",
            "relationship": "description of the relationship"
        }
    ],
    "triggers": [
        {
            "state": "state name",
            "trigger": "what triggers the transition"
        }
    ],
    "conditions": [
        {
            "state": "state name",
            "condition": "conditions that must be met"
        }
    ],
    "timing": [
        {
            "state": "state name",
            "timing": "timing of the transition"
        }
    ]
}

Text to analyze:
"""

# Keywords to identify relevant sections
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

def is_relevant_chunk(text: str) -> bool:
    """Check if chunk contains relevant information about registration procedure."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in RELEVANT_KEYWORDS)

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:?!-]', '', text)
    return text.strip()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF with better error handling and memory management."""
    text = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            
            console.print(f"[blue]Processing {total_pages} pages from {pdf_path}[/blue]")
            for i, page in enumerate(reader.pages, 1):
                try:
                    page_text = page.extract_text() or ""
                    # Only append if page contains relevant content
                    if is_relevant_chunk(page_text):
                        text.append(clean_text(page_text))
                    if i % 10 == 0:
                        console.print(f"[blue]Processed {i}/{total_pages} pages[/blue]")
                except Exception as page_error:
                    console.print(f"[yellow]Warning: Error extracting text from page {i}: {str(page_error)}[/yellow]")
                    
        return "\n".join(text)
    
    except Exception as e:
        console.print(f"[red]Error processing {pdf_path}: {str(e)}[/red]")
        return ""

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
        
        try:
            # First try to parse as is
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON
            try:
                # Find the first { and last }
                start = response_text.find('{')
                end = response_text.rfind('}')
                
                if start == -1 or end == -1:
                    raise ValueError("No JSON object found in response")
                
                json_str = response_text[start:end + 1]
                return json.loads(json_str)
            except (json.JSONDecodeError, ValueError) as e:
                console.print(f"[yellow]Failed to parse response as JSON. Error: {str(e)}[/yellow]")
                console.print("[yellow]Raw response:[/yellow]")
                console.print(response_text)
                
                # Create a minimal valid response
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
        full_prompt = EXTRACTION_PROMPT + clean_text(doc.page_content)

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
                
            extracted_data['metadata'] = {
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

def get_content_hash(content: str) -> str:
    """Generate a hash of the content for deduplication."""
    return hashlib.md5(content.encode()).hexdigest()

def is_similar_content(content1: str, content2: str, similarity_threshold: float = 0.8) -> bool:
    """Check if two content chunks are similar using basic similarity metric."""
    words1 = set(content1.lower().split())
    words2 = set(content2.lower().split())
    
    if not words1 or not words2:
        return False
        
    intersection = words1.intersection(words2)
    smaller_set = min(len(words1), len(words2))
    
    return len(intersection) / smaller_set > similarity_threshold

class ContentDeduplicator:
    def __init__(self):
        self.content_hashes: Set[str] = set()
        self.processed_contents: List[str] = []
        
    def is_duplicate(self, content: str) -> bool:
        """Check if content is duplicate or too similar to previously processed content."""
        content_hash = get_content_hash(content)
        
        # Check exact duplicates first
        if content_hash in self.content_hashes:
            return True
            
        # Check similarity with previously processed content
        for processed_content in self.processed_contents[-5:]:  # Only check last 5 chunks for efficiency
            if is_similar_content(content, processed_content):
                return True
                
        # Not a duplicate, store for future checks
        self.content_hashes.add(content_hash)
        self.processed_contents.append(content)
        return False

def process_pdf_file(pdf_path: str, llm: Any) -> List[Dict]:
    """Process a PDF file and return extracted information."""
    try:
        console.print(f"\n[blue]Processing PDF: {pdf_path}[/blue]")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            console.print(f"[yellow]No relevant text extracted from {pdf_path}. Skipping.[/yellow]")
            return []

        # Create chunks with smaller overlap
        overlap = 100
        chunks = []
        start = 0
        deduplicator = ContentDeduplicator()
        
        while start < len(text):
            end = min(start + CHUNK_SIZE, len(text))
            if end < len(text):
                last_period = text.rfind('.', end - overlap, end)
                if last_period != -1:
                    end = last_period + 1
            
            chunk = text[start:end]
            
            # Only add chunks that:
            # 1. Contain relevant information
            # 2. Are not duplicates or too similar to previous chunks
            if is_relevant_chunk(chunk) and not deduplicator.is_duplicate(chunk):
                chunks.append(chunk)
            elif deduplicator.is_duplicate(chunk):
                console.print(f"[yellow]Skipping duplicate/similar chunk at position {start}[/yellow]")
            
            start = end - overlap if end < len(text) else end

        console.print(f"[blue]Created {len(chunks)} unique relevant chunks[/blue]")

        # Process chunks and collect results
        results = []
        seen_states = set()
        seen_transitions = set()
        
        for chunk_index, chunk in enumerate(chunks):
            chunk_doc = Document(
                page_content=chunk,
                metadata={
                    "source": pdf_path,
                    "chunk_index": chunk_index,
                    "total_chunks": len(chunks)
                }
            )
            chunk_result = process_chunk(chunk_doc, llm)
            
            if chunk_result:
                # Deduplicate states and transitions
                if 'states' in chunk_result:
                    unique_states = []
                    for state in chunk_result['states']:
                        state_key = f"{state['name']}_{state['type']}"
                        if state_key not in seen_states:
                            seen_states.add(state_key)
                            unique_states.append(state)
                    chunk_result['states'] = unique_states
                
                if 'transitions' in chunk_result:
                    unique_transitions = []
                    for transition in chunk_result['transitions']:
                        transition_key = f"{transition['from_state']}_{transition['to_state']}_{transition['trigger']}"
                        if transition_key not in seen_transitions:
                            seen_transitions.add(transition_key)
                            unique_transitions.append(transition)
                    chunk_result['transitions'] = unique_transitions
                
                results.append(chunk_result)
                save_intermediate_results(results, chunk_index, len(chunks))

        return results

    except Exception as e:
        console.print(f"[red]Error processing PDF {pdf_path}: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return []

def ensure_folders_exist():
    """Ensure all required folders exist and clean up old processed files."""
    try:
        os.makedirs(PDF_FOLDER, exist_ok=True)
        os.makedirs(PROCESSED_DATA_FOLDER, exist_ok=True)
        
        # Clean up old files in processed_data folder
        console.print("[blue]Checking for old processed files...[/blue]")
        old_files = [
            f for f in os.listdir(PROCESSED_DATA_FOLDER)
            if f.startswith(("intermediate_results_", "extraction_complete"))
        ]
        
        if old_files:
            console.print("[yellow]Found old processed files. Cleaning up...[/yellow]")
            for file in old_files:
                try:
                    os.remove(os.path.join(PROCESSED_DATA_FOLDER, file))
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not remove {file}: {str(e)}[/yellow]")
            console.print("[green]✓ Cleaned up old processed files[/green]")
        else:
            console.print("[blue]No old processed files found[/blue]")
            
    except Exception as e:
        console.print(f"[red]Error setting up folders: {str(e)}[/red]")
        raise

def save_intermediate_results(results: List[Dict], chunk_index: int, total_chunks: int):
    """Save intermediate results every INTERMEDIATE_BATCH_SIZE chunks."""
    try:
        # Only save if we have collected INTERMEDIATE_BATCH_SIZE chunks or it's the last batch
        if chunk_index % INTERMEDIATE_BATCH_SIZE != 0 and chunk_index != total_chunks:
            return

        batch_number = (chunk_index - 1) // INTERMEDIATE_BATCH_SIZE + 1
        total_batches = (total_chunks - 1) // INTERMEDIATE_BATCH_SIZE + 1
        
        intermediate_file = os.path.join(
            PROCESSED_DATA_FOLDER,
            f"intermediate_results_batch_{batch_number}_of_{total_batches}.json"
        )
        
        output_data = {
            'metadata': {
                'extraction_time': datetime.now().isoformat(),
                'total_documents': len(results),
                'batch_number': batch_number,
                'total_batches': total_batches,
                'chunks_in_batch': min(INTERMEDIATE_BATCH_SIZE, chunk_index % INTERMEDIATE_BATCH_SIZE or INTERMEDIATE_BATCH_SIZE)
            },
            'results': results
        }
        
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓ Saved intermediate results batch {batch_number} of {total_batches}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error saving intermediate results: {str(e)}[/red]")

def save_completion_marker():
    """Save a completion marker file to indicate extraction is done."""
    try:
        completion_file = os.path.join(PROCESSED_DATA_FOLDER, "extraction_complete.json")
        with open(completion_file, 'w', encoding='utf-8') as f:
            json.dump({
                'completion_time': datetime.now().isoformat(),
                'status': 'complete'
            }, f)
        console.print(f"[green]✓ Saved completion marker[/green]")
    except Exception as e:
        console.print(f"[red]Error saving completion marker: {str(e)}[/red]")

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

def test_neo4j_connection():
    """Test Neo4j connection and credentials."""
    try:
        if not NEO4J_PASSWORD:
            console.print("[red]Error: NEO4J_PASSWORD environment variable is not set[/red]")
            return False

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
        driver.close()
        return True
    except Exception as e:
        console.print(f"[red]Neo4j connection error: {str(e)}[/red]")
        return False

def convert_to_relationship_type(description: str) -> str:
    """Convert a relationship description to a valid Neo4j relationship type.
    
    Examples:
    - "sends messages to" -> SENDS_MESSAGES_TO
    - "authenticates with" -> AUTHENTICATES_WITH
    - "requests service from" -> REQUESTS_SERVICE_FROM
    """
    # Clean and normalize the text
    text = description.strip().lower()
    
    # Common relationship patterns to extract verbs
    common_patterns = [
        r'^(sends|receives|authenticates|requests|provides|manages|controls|forwards|processes|initiates|terminates|connects|disconnects|registers|deregisters|allocates|deallocates|establishes|releases|monitors|updates|verifies|validates|configures|coordinates|handles|routes|transmits|stores|retrieves|generates|maintains|synchronizes|notifies|informs|checks|authorizes|rejects|accepts|acknowledges|triggers|implements|supports|enables|facilitates|performs|executes|delivers|serves|hosts|contains|includes|requires|depends|links|associates|relates|maps|binds|attaches|detaches|joins|splits|merges|divides|combines|integrates|separates|isolates|groups|classifies|categorizes|organizes|arranges|orders|sequences|prioritizes|ranks|rates|scores|evaluates|assesses|measures|calculates|computes|determines|decides|selects|chooses|picks|identifies|recognizes|detects|finds|locates|tracks|follows|precedes|succeeds|leads|guides|directs|steers|drives|pushes|pulls|moves|shifts|changes|modifies|alters|adjusts|tunes|optimizes|enhances|improves|upgrades|downgrades|maintains|preserves|protects|secures|encrypts|decrypts|signs|verifies)\s.*'
    ]
    
    for pattern in common_patterns:
        match = re.match(pattern, text)
        if match:
            verb = match.group(1)
            # Convert to uppercase and replace spaces with underscores
            return re.sub(r'\s+', '_', verb.upper())
    
    # If no verb pattern is found, create a relationship type from the first few words
    words = re.sub(r'[^\w\s]', '', text).split()[:3]  # Take first 3 words max
    return '_'.join(words).upper()

def store_registration_data_in_neo4j(results: List[Dict]):
    """Store registration procedure data in Neo4j."""
    try:
        if not test_neo4j_connection():
            return False

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        with driver.session() as session:
            # Clear existing data
            console.print("[blue]Clearing existing database...[/blue]")
            session.run("MATCH (n) DETACH DELETE n")
            
            for result in results:
                # Create NetworkElement nodes
                for element in result.get('network_elements', []):
                    session.run("""
                        MERGE (n:NetworkElement {name: $name})
                        SET n.type = $type,
                            n.description = $description
                    """, name=element['name'], type=element['type'], 
                         description=element.get('description', ''))

                # Create State nodes
                for state in result.get('states', []):
                    session.run("""
                        MERGE (s:State {name: $name})
                        SET s.type = $type,
                            s.description = $description
                    """, name=state['name'], type=state['type'],
                         description=state.get('description', ''))

                # Create NetworkElement relationships with explicit verb labels
                for rel in result.get('network_element_relationships', []):
                    rel_type = convert_to_relationship_type(rel['relationship'])
                    cypher = f"""
                        MATCH (e1:NetworkElement {{name: $element1}})
                        MATCH (e2:NetworkElement {{name: $element2}})
                        MERGE (e1)-[r:{rel_type}]->(e2)
                        SET r.description = $relationship
                    """
                    session.run(cypher, 
                              element1=rel['element1'], 
                              element2=rel['element2'],
                              relationship=rel['relationship'])

                # Create State transitions with explicit verb labels
                for transition in result.get('transitions', []):
                    # Extract verb from trigger if available, otherwise use TRANSITIONS_TO
                    rel_type = convert_to_relationship_type(transition.get('trigger', '')) if transition.get('trigger') else 'TRANSITIONS_TO'
                    cypher = f"""
                        MATCH (s1:State {{name: $from_state}})
                        MATCH (s2:State {{name: $to_state}})
                        MERGE (s1)-[r:{rel_type}]->(s2)
                        SET r.trigger = $trigger,
                            r.condition = $condition,
                            r.probability = $probability
                    """
                    session.run(cypher,
                              from_state=transition['from_state'],
                              to_state=transition['to_state'],
                              trigger=transition.get('trigger', ''),
                              condition=transition.get('condition', ''),
                              probability=transition.get('probability', ''))

                # Create Triggers with explicit verb relationships
                for trigger in result.get('triggers', []):
                    rel_type = convert_to_relationship_type(trigger['trigger'])
                    cypher = f"""
                        MERGE (t:Trigger {{name: $trigger}})
                        MATCH (s:State {{name: $state}})
                        MERGE (t)-[r:{rel_type}]->(s)
                    """
                    session.run(cypher, 
                              trigger=trigger['trigger'], 
                              state=trigger['state'])

                # Create Conditions with explicit verb relationships
                for condition in result.get('conditions', []):
                    rel_type = convert_to_relationship_type(condition['condition'])
                    cypher = f"""
                        MERGE (c:Condition {{name: $condition}})
                        MATCH (s:State {{name: $state}})
                        MERGE (c)-[r:{rel_type}]->(s)
                    """
                    session.run(cypher, 
                              condition=condition['condition'], 
                              state=condition['state'])

                # Create Timing with explicit verb relationships
                for timing in result.get('timing', []):
                    rel_type = convert_to_relationship_type(timing['timing'])
                    cypher = f"""
                        MERGE (t:Timing {{description: $timing}})
                        MATCH (s:State {{name: $state}})
                        MERGE (t)-[r:{rel_type}]->(s)
                    """
                    session.run(cypher, 
                              timing=timing['timing'], 
                              state=timing['state'])

        driver.close()
        console.print("[green]✓ Registration data successfully stored in Neo4j with explicit relationship labels![/green]")
        return True

    except Exception as e:
        console.print(f"[red]Error storing data in Neo4j: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return False

def start_neo4j_process():
    """Start the Neo4j storage process in a separate thread."""
    try:
        # Get the path to store_data_neo4j.py
        current_dir = Path(__file__).parent
        neo4j_script = current_dir / "store_data_neo4j.py"
        
        if not neo4j_script.exists():
            console.print("[red]Error: store_data_neo4j.py not found in the same directory[/red]")
            return None
            
        # Start the Neo4j storage process with the processed_data folder path
        process = subprocess.Popen(
            [sys.executable, str(neo4j_script), "--data-dir", PROCESSED_DATA_FOLDER],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
                                
        # Create a thread to monitor and print the process output
        def monitor_output():
            while True:
                output = process.stdout.readline()
                if output:
                    console.print("[blue][Neo4j Storage][/blue] " + output.strip())
                error = process.stderr.readline()
                if error:
                    console.print("[red][Neo4j Storage Error][/red] " + error.strip())
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
        thread = threading.Thread(target=monitor_output, daemon=True)
        thread.start()
        
        return process
        
    except Exception as e:
        console.print(f"[red]Error starting Neo4j storage process: {str(e)}[/red]")
        return None

def main():
    try:
        # Ensure folders exist
        ensure_folders_exist()
        
        # Start Neo4j storage process in parallel
        console.print("[blue]Starting Neo4j storage process...[/blue]")
        neo4j_process = start_neo4j_process()
        
        # Initialize LLM
        llm = initialize_llm()
        
        # Check for PDF files
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        if not pdf_files:
            console.print(f"[yellow]No PDF files found in {PDF_FOLDER}[/yellow]")
            console.print("[yellow]Please place your PDF files in this directory and run the script again.[/yellow]")
            return
        
        console.print(f"[blue]Found {len(pdf_files)} PDF files to process[/blue]")
        
        # Process each PDF and collect results
        all_results = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
            results = process_pdf_file(pdf_path, llm)
            all_results.extend(results)
        
        # Save final results to JSON file
        save_results(all_results, OUTPUT_FILE)
        console.print("[green]✓ Processing completed successfully[/green]")
        
        # Save completion marker for Neo4j process
        save_completion_marker()
        
        # Wait for Neo4j process to finish
        if neo4j_process:
            console.print("[blue]Waiting for Neo4j storage to complete...[/blue]")
            neo4j_process.wait()
            
        console.print("[green]✓ All operations completed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")
        console.print(traceback.format_exc())
        
    finally:
        # Ensure completion marker is saved even if there's an error
        save_completion_marker()

if __name__ == "__main__":
    main()