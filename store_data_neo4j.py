import os
import re
import json
import time
from typing import List, Dict, Tuple, Set
from pypdf import PdfReader
from neo4j import GraphDatabase
import hashlib
from rich.console import Console
import glob
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Initialize console and load environment variables
console = Console()
load_dotenv()

# Neo4j Configuration
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Cache file for Neo4j state
NEO4J_CACHE_FILE = "neo4j_cache.json"

# Input files configuration
INTERMEDIATE_PATTERN = "intermediate_results_*.json"
PROCESSED_FILES_CACHE = "processed_neo4j_files.json"
BATCH_SIZE = 100  # Number of operations to batch together

def load_processed_files() -> Set[str]:
    """Load the set of already processed intermediate files."""
    try:
        if os.path.exists(PROCESSED_FILES_CACHE):
            with open(PROCESSED_FILES_CACHE, 'r') as f:
                return set(json.load(f))
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load processed files cache: {e}[/yellow]")
    return set()

def save_processed_files(processed: Set[str]):
    """Save the set of processed files."""
    try:
        with open(PROCESSED_FILES_CACHE, 'w') as f:
            json.dump(list(processed), f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not save processed files cache: {e}[/yellow]")

def test_neo4j_connection(uri, username, password):
    """Test Neo4j connection and credentials"""
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            # Simple query to test connection
            result = session.run("RETURN 1 as test")
            result.single()
        driver.close()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

def convert_to_relationship_type(description: str) -> str:
    """Convert a relationship description to a valid Neo4j relationship type."""
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

def batch_neo4j_operations(session, operations: List[Dict]):
    """Execute Neo4j operations in batches for better performance."""
    try:
        # Create an unwind statement for batch processing
        if not operations:
            return
            
        operation_type = operations[0]['type']
        
        if operation_type == 'network_element':
            cypher = """
            UNWIND $operations as op
            MERGE (n:NetworkElement {name: op.name})
            SET n.type = op.element_type,
                n.description = op.description
            """
        elif operation_type == 'state':
            cypher = """
            UNWIND $operations as op
            MERGE (s:State {name: op.name})
            SET s.type = op.state_type,
                s.description = op.description
            """
        elif operation_type == 'relationship':
            # Use dynamic relationship type based on the verb
            cypher = """
            UNWIND $operations as op
            MATCH (e1:NetworkElement {name: op.element1})
            MATCH (e2:NetworkElement {name: op.element2})
            WITH e1, e2, op
            CALL apoc.merge.relationship(e1, op.rel_type, {}, {description: op.description}, e2)
            YIELD rel
            RETURN count(*)
            """
        elif operation_type == 'transition':
            cypher = """
            UNWIND $operations as op
            MATCH (s1:State {name: op.from_state})
            MATCH (s2:State {name: op.to_state})
            MERGE (s1)-[r:TRANSITIONS_TO]->(s2)
            SET r.trigger = op.trigger,
                r.condition = op.condition,
                r.probability = op.probability
            """
            
        session.run(cypher, operations=operations)
        
    except Exception as e:
        console.print(f"[red]Error in batch operation: {str(e)}[/red]")

def process_intermediate_file(file_path: str, driver, processed_files: Set[str]) -> bool:
    """Process a single intermediate results file and store in Neo4j."""
    try:
        if file_path in processed_files:
            return True
            
        console.print(f"[blue]Processing {file_path}...[/blue]")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        with driver.session() as session:
            # First, ensure APOC is available
            try:
                session.run("CALL apoc.help('merge')")
            except Exception as e:
                console.print("[red]Error: APOC procedures not available. Please install APOC in your Neo4j instance.[/red]")
                return False

            for result in data.get('results', []):
                # Batch network elements
                network_elements = []
                for element in result.get('network_elements', []):
                    network_elements.append({
                        'type': 'network_element',
                        'name': element['name'],
                        'element_type': element['type'],
                        'description': element.get('description', '')
                    })
                    if len(network_elements) >= BATCH_SIZE:
                        batch_neo4j_operations(session, network_elements)
                        network_elements = []
                if network_elements:
                    batch_neo4j_operations(session, network_elements)

                # Batch states
                states = []
                for state in result.get('states', []):
                    states.append({
                        'type': 'state',
                        'name': state['name'],
                        'state_type': state['type'],
                        'description': state.get('description', '')
                    })
                    if len(states) >= BATCH_SIZE:
                        batch_neo4j_operations(session, states)
                        states = []
                if states:
                    batch_neo4j_operations(session, states)

                # Process relationships with explicit verb labels
                relationships = []
                for rel in result.get('network_element_relationships', []):
                    rel_type = convert_to_relationship_type(rel['relationship'])
                    relationships.append({
                        'type': 'relationship',
                        'element1': rel['element1'],
                        'element2': rel['element2'],
                        'rel_type': rel_type,
                        'description': rel['relationship']
                    })
                    if len(relationships) >= BATCH_SIZE:
                        batch_neo4j_operations(session, relationships)
                if relationships:
                    batch_neo4j_operations(session, relationships)

                # Process transitions
                transitions = []
                for transition in result.get('transitions', []):
                    transitions.append({
                        'type': 'transition',
                        'from_state': transition['from_state'],
                        'to_state': transition['to_state'],
                        'trigger': transition.get('trigger', ''),
                        'condition': transition.get('condition', ''),
                        'probability': transition.get('probability', '')
                    })
                    if len(transitions) >= BATCH_SIZE:
                        batch_neo4j_operations(session, transitions)
                        transitions = []
                if transitions:
                    batch_neo4j_operations(session, transitions)

        processed_files.add(file_path)
        save_processed_files(processed_files)
        console.print(f"[green]✓ Processed {file_path}[/green]")
        return True

    except Exception as e:
        console.print(f"[red]Error processing {file_path}: {str(e)}[/red]")
        return False

def monitor_and_process():
    """Monitor for new intermediate files and process them as they appear."""
    if not PASSWORD:
        console.print("[red]Error: NEO4J_PASSWORD environment variable is not set[/red]")
        return False

    # Test connection first
    console.print("[blue]Testing Neo4j connection...[/blue]")
    success, message = test_neo4j_connection(URI, USERNAME, PASSWORD)
    if not success:
        console.print(f"[red]Neo4j connection failed: {message}[/red]")
        console.print("[yellow]Please ensure:[/yellow]")
        console.print("[yellow]1. Neo4j is running[/yellow]")
        console.print("[yellow]2. Credentials in .env file are correct[/yellow]")
        console.print(f"[yellow]3. Neo4j is accepting connections on {URI}[/yellow]")
        return False

    console.print("[green]Neo4j connection successful[/green]")
    
    try:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        
        # Test APOC availability
        with driver.session() as session:
            try:
                session.run("CALL apoc.help('merge')")
                console.print("[green]APOC procedures available[/green]")
            except Exception as e:
                console.print("[red]Error: APOC procedures not available. Please install APOC in your Neo4j instance.[/red]")
                console.print(f"[red]Error details: {str(e)}[/red]")
                return False
        
        # Clear existing data before starting
        console.print("[blue]Clearing existing database...[/blue]")
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        console.print("[green]Database cleared successfully[/green]")
        
        processed_files = load_processed_files()
        
        console.print("[blue]Monitoring for new intermediate results...[/blue]")
        
        # Get the directory where the script is running
        current_dir = os.getcwd()
        console.print(f"[blue]Looking for files in: {current_dir}[/blue]")
        
        while True:
            # Get all intermediate files with full path
            intermediate_files = glob.glob(os.path.join(current_dir, "processed_data", "intermediate_results_*.json"))
            
            if not intermediate_files:
                console.print("[yellow]No intermediate files found yet...[/yellow]")
            else:
                console.print(f"[blue]Found {len(intermediate_files)} intermediate files[/blue]")
                
            # Process any new files
            for file_path in intermediate_files:
                if file_path not in processed_files:
                    console.print(f"[blue]Processing new file: {file_path}[/blue]")
                    success = process_intermediate_file(file_path, driver, processed_files)
                    if not success:
                        console.print(f"[red]Failed to process {file_path}[/red]")
            
            # Check if extraction is complete
            completion_file = os.path.join(current_dir, "processed_data", "extraction_complete.json")
            if os.path.exists(completion_file):
                console.print("[green]Found completion marker, finishing up...[/green]")
                break
                
            time.sleep(5)  # Wait before checking for new files

        driver.close()
        console.print("[green]✓ All intermediate results have been processed![/green]")
        
        # Verify data was saved
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        with driver.session() as session:
            # Check for nodes
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            console.print(f"[blue]Verification: Found {node_count} nodes and {rel_count} relationships in Neo4j[/blue]")
        driver.close()
        
        return True

    except Exception as e:
        console.print(f"[red]Error in monitoring process: {str(e)}[/red]")
        console.print(traceback.format_exc())  # Add full traceback
        return False

def main():
    """Main function to monitor and process intermediate results."""
    try:
        if monitor_and_process():
            console.print("[green]✓ All data has been successfully processed and stored in Neo4j![/green]")
        else:
            console.print("[red]Failed to process and store data in Neo4j.[/red]")
            
    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")

def read_registration_data(file_path: str) -> Dict:
    """Read data from either JSON or Markdown file."""
    try:
        console.print(f"[blue]Opening file: {file_path}[/blue]")
        
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                console.print("[green]Successfully loaded JSON file[/green]")
                return data
        elif file_path.endswith('.md'):
            data = {'results': []}
            current_section = None
            current_chunk = {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            console.print(f"[blue]Processing {len(lines)} lines from markdown file[/blue]")
            
            for i, line in enumerate(lines):
                if line.startswith('# Extracted Data'):
                    if current_chunk:
                        console.print(f"[blue]Adding chunk with sections: {list(current_chunk.keys())}[/blue]")
                        data['results'].append(current_chunk)
                    current_chunk = {}
                elif line.startswith('## '):
                    current_section = line.strip('## \n').lower().replace(' ', '_')
                    current_chunk[current_section] = []
                    console.print(f"[blue]Found section: {current_section}[/blue]")
                elif line.strip() and current_section and line.strip().startswith('{'):
                    try:
                        item = json.loads(line.strip())
                        current_chunk[current_section].append(item)
                    except json.JSONDecodeError as e:
                        console.print(f"[yellow]Warning: Could not parse JSON at line {i+1}: {e}[/yellow]")
                        continue
            
            if current_chunk:
                console.print(f"[blue]Adding final chunk with sections: {list(current_chunk.keys())}[/blue]")
                data['results'].append(current_chunk)
            
            console.print(f"[green]Successfully processed markdown file with {len(data['results'])} chunks[/green]")
            return data
            
        raise ValueError(f"Unsupported file format: {file_path}")
        
    except Exception as e:
        console.print(f"[red]Error reading file {file_path}: {str(e)}[/red]")
        console.print(traceback.format_exc())  # Print full traceback
        raise

def create_unique_constraints(session):
    """Create unique constraints for nodes."""
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:NetworkElement) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:State) REQUIRE n.name IS UNIQUE"
    ]
    
    for constraint in constraints:
        try:
            session.run(constraint)
        except Exception as e:
            console.print(f"[yellow]Warning creating constraint: {str(e)}[/yellow]")

def generate_content_hash(content: Dict) -> str:
    """Generate a hash for content to track duplicates."""
    content_str = json.dumps(content, sort_keys=True)
    return hashlib.md5(content_str.encode()).hexdigest()

def store_network_elements(session, elements: List[Dict]):
    """Store network elements with their properties."""
    for element in elements:
        cypher = """
        MERGE (n:NetworkElement {name: $name})
        SET n.type = $type,
            n.description = $description
        """
        session.run(cypher, 
                   name=element['name'],
                   type=element.get('type', ''),
                   description=element.get('description', ''))

def store_states(session, states: List[Dict]):
    """Store states with their properties."""
    for state in states:
        cypher = """
        MERGE (s:State {name: $name})
        SET s.type = $type,
            s.description = $description
        """
        session.run(cypher, 
                   name=state['name'],
                   type=state.get('type', ''),
                   description=state.get('description', ''))

def store_events(session, events: List[Dict]):
    """Store events as nodes."""
    for event in events:
        cypher = """
        MERGE (e:Event {name: $name})
        SET e.description = $description
        """
        session.run(cypher, 
                   name=event['name'],
                   description=event.get('description', ''))

def store_transitions(session, transitions: List[Dict]):
    """Store transitions as relationships with deduplication."""
    processed_hashes = set()
    for transition in transitions:
        content_hash = generate_content_hash(transition)
        if content_hash in processed_hashes:
            continue
            
        # Create relationship between network elements for the message
        cypher_message = """
        MATCH (from:NetworkElement {name: $from_element})
        MATCH (to:NetworkElement {name: $to_element})
        MERGE (from)-[r:SENDS_MESSAGE {
            step: $step,
            message: $message
        }]->(to)
        SET r.trigger = $trigger,
            r.condition = $condition,
            r.timing = $timing,
            r.content_hash = $content_hash
        """
        session.run(cypher_message,
                   from_element=transition['from_element'],
                   to_element=transition['to_element'],
                   step=transition.get('step', 0),
                   message=transition['message'],
                   trigger=transition.get('trigger', ''),
                   condition=transition.get('condition', ''),
                   timing=transition.get('timing', ''),
                   content_hash=content_hash)
        
        # Create relationship between states for the transition
        cypher_state = """
        MATCH (from:State {name: $from_state})
        MATCH (to:State {name: $to_state})
        MERGE (from)-[r:TRANSITIONS_TO {
            step: $step,
            message: $message
        }]->(to)
        SET r.trigger = $trigger,
            r.condition = $condition,
            r.timing = $timing,
            r.content_hash = $content_hash
        """
        session.run(cypher_state,
                   from_state=transition['from_state'],
                   to_state=transition['to_state'],
                   step=transition.get('step', 0),
                   message=transition['message'],
                   trigger=transition.get('trigger', ''),
                   condition=transition.get('condition', ''),
                   timing=transition.get('timing', ''),
                   content_hash=content_hash)
        processed_hashes.add(content_hash)

def store_element_relationships(session, relationships: List[Dict]):
    """Store relationships between network elements with deduplication."""
    processed_hashes = set()
    for rel in relationships:
        content_hash = generate_content_hash(rel)
        if content_hash in processed_hashes:
            continue
            
        rel_type = convert_to_relationship_type(rel['relationship'])
        cypher = """
        MATCH (e1:NetworkElement {name: $element1})
        MATCH (e2:NetworkElement {name: $element2})
        MERGE (e1)-[r:RELATES_TO {
            element1: $element1,
            element2: $element2,
            type: $rel_type
        }]->(e2)
        SET r.description = $description,
            r.content_hash = $content_hash
        """
        session.run(cypher,
                   element1=rel['element1'],
                   element2=rel['element2'],
                   rel_type=rel_type,
                   description=rel['relationship'],
                   content_hash=content_hash)
        processed_hashes.add(content_hash)

def store_triggers(session, triggers: List[Dict]):
    """Store triggers."""
    for trigger in triggers:
        cypher = """
        MATCH (s:State {name: $state})
        MERGE (t:Trigger {name: $trigger})
        MERGE (s)-[r:HAS_TRIGGER]->(t)
        """
        session.run(cypher,
                   state=trigger['state'],
                   trigger=trigger['trigger'])

def store_conditions(session, conditions: List[Dict]):
    """Store conditions."""
    for condition in conditions:
        cypher = """
        MATCH (s:State {name: $state})
        MERGE (c:Condition {description: $condition})
        MERGE (s)-[r:HAS_CONDITION]->(c)
        """
        session.run(cypher,
                   state=condition['state'],
                   condition=condition['condition'])

def store_timing(session, timings: List[Dict]):
    """Store timing information."""
    for timing in timings:
        cypher = """
        MATCH (s:State {name: $state})
        MERGE (t:Timing {description: $timing})
        MERGE (s)-[r:HAS_TIMING]->(t)
        """
        session.run(cypher,
                   state=timing['state'],
                   timing=timing['timing'])

def store_registration_flow(session, flow_items: List[Dict]):
    """Store registration flow items with all their properties."""
    for item in flow_items:
        try:
            # Create or merge source and destination elements if they exist
            if item.get('source_element') and item.get('destination_element'):
                cypher_elements = """
                MERGE (source:NetworkElement {name: $source_name})
                MERGE (dest:NetworkElement {name: $dest_name})
                """
                session.run(cypher_elements, 
                        source_name=item['source_element'],
                        dest_name=item['destination_element'])

            # Create or merge source and destination states if they exist
            if item.get('source_state') and item.get('destination_state'):
                cypher_states = """
                MERGE (source_state:State {name: $source_state})
                MERGE (dest_state:State {name: $dest_state})
                """
                session.run(cypher_states,
                        source_state=item['source_state'],
                        dest_state=item['destination_state'])

            # Create the message relationship between elements if they exist
            if item.get('source_element') and item.get('destination_element'):
                cypher_message = """
                MATCH (source:NetworkElement {name: $source_name})
                MATCH (dest:NetworkElement {name: $dest_name})
                MERGE (source)-[r:SENDS_MESSAGE]->(dest)
                SET r.step = $sequence_number,
                    r.message = $message,
                    r.step_name = $step_name,
                    r.description = $description,
                    r.trigger = $trigger,
                    r.conditions = $conditions,
                    r.timing = $timing
                """
                session.run(cypher_message,
                        source_name=item['source_element'],
                        dest_name=item['destination_element'],
                        sequence_number=item['sequence_number'],
                        message=item.get('message', ''),
                        step_name=item.get('step_name', ''),
                        description=item.get('description', ''),
                        trigger=item.get('trigger', ''),
                        conditions=item.get('conditions', []),
                        timing=item.get('timing', ''))

            # Create the state transition relationship if states exist
            if item.get('source_state') and item.get('destination_state'):
                cypher_transition = """
                MATCH (source_state:State {name: $source_state})
                MATCH (dest_state:State {name: $dest_state})
                MERGE (source_state)-[t:TRANSITIONS_TO]->(dest_state)
                SET t.step = $sequence_number,
                    t.message = $message,
                    t.trigger = $trigger,
                    t.conditions = $conditions,
                    t.timing = $timing
                """
                session.run(cypher_transition,
                        source_state=item['source_state'],
                        dest_state=item['destination_state'],
                        sequence_number=item['sequence_number'],
                        message=item.get('message', ''),
                        trigger=item.get('trigger', ''),
                        conditions=item.get('conditions', []),
                        timing=item.get('timing', ''))
        except Exception as e:
            console.print(f"[yellow]Warning: Error processing flow item {item.get('sequence_number', 'unknown')}: {str(e)}[/yellow]")
            continue

def process_registration_data(file_path: str = "processed_data/registration_analysis.json"):
    """Process and store registration analysis data."""
    try:
        # Test Neo4j connection first
        console.print("[blue]Testing Neo4j connection...[/blue]")
        success, message = test_neo4j_connection(URI, USERNAME, PASSWORD)
        if not success:
            console.print(f"[red]Neo4j connection failed: {message}[/red]")
            return

        console.print(f"[blue]Reading data from {file_path}...[/blue]")
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Clear existing data
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        with driver.session() as session:
            clear_database(session)
            
        # Process each result in the results array
        for result in data.get('results', []):
            with driver.session() as session:
                # Create constraints
                create_unique_constraints(session)
                
                # Store network elements
                if 'network_elements' in result:
                    console.print(f"[blue]Storing {len(result['network_elements'])} network elements...[/blue]")
                    store_network_elements(session, result['network_elements'])

                # Store states
                if 'states' in result:
                    console.print(f"[blue]Storing {len(result['states'])} states...[/blue]")
                    store_states(session, result['states'])

                # Store registration flow
                if 'registration_flow' in result:
                    console.print(f"[blue]Storing registration flow with {len(result['registration_flow'])} steps...[/blue]")
                    store_registration_flow(session, result['registration_flow'])

                # Store metadata
                if 'metadata' in result:
                    console.print("[blue]Storing metadata...[/blue]")
                    cypher_metadata = """
                    CREATE (m:Metadata)
                    SET m += $metadata
                    """
                    session.run(cypher_metadata, metadata=result['metadata'])

        # Verify final data counts
        with driver.session() as session:
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            
            console.print(f"[green]✓ Data stored successfully in Neo4j[/green]")
            console.print(f"[blue]Total nodes: {node_count}[/blue]")
            console.print(f"[blue]Total relationships: {rel_count}[/blue]")
            
    except Exception as e:
        console.print(f"[red]Error storing data in Neo4j: {str(e)}[/red]")
        console.print(traceback.format_exc())
        raise
    finally:
        if 'driver' in locals():
            driver.close()

def clear_database(session):
    """Clear all nodes and relationships from the database."""
    try:
        session.run("MATCH (n) DETACH DELETE n")
        console.print("[green]✓ Database cleared successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error clearing database: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    process_registration_data()
