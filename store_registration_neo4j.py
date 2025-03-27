import os
import re
import json
import time
from typing import List, Dict, Tuple, Set
from neo4j import GraphDatabase
import hashlib
from rich.console import Console
import glob
from datetime import datetime
import traceback
from dotenv import load_dotenv
from models import RegistrationData, NetworkElement, ProcedureStep
from pydantic import ValidationError

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



def validate_neo4j_data(data: dict) -> bool:
    """Validate data against Pydantic models"""
    try:
        RegistrationData(**data)
        return True
    except ValidationError as e:
        console.print(f"[red]Validation error: {e}[/red]")
        return False

def verify_neo4j_data(session) -> bool:
    """Verify data in Neo4j database"""
    try:
        # Check nodes exist
        node_count = session.run("""
            MATCH (n:NetworkElement) 
            RETURN count(n) as count
        """).single()["count"]

        # Check relationships exist
        rel_count = session.run("""
            MATCH ()-[r:SENDS_MESSAGE]->()
            WHERE r.procedure = 'Initial Registration'
            RETURN count(r) as count
        """).single()["count"]

        # Check procedure flow is complete
        flow = session.run("""
            MATCH (source)-[r:SENDS_MESSAGE]->(target)
            WHERE r.procedure = 'Initial Registration'
            RETURN source.name, r.message, target.name, r.sequence_number
            ORDER BY r.sequence_number
        """).data()

        console.print(f"[blue]Found {node_count} network elements[/blue]")
        console.print(f"[blue]Found {rel_count} procedure steps[/blue]")
        console.print("\n[blue]Procedure Flow:[/blue]")
        for step in flow:
            console.print(f"[green]{step['sequence_number']}. {step['source.name']} -> {step['target.name']}: {step['r.message']}[/green]")

        return node_count > 0 and rel_count > 0

    except Exception as e:
        console.print(f"[red]Error verifying data: {str(e)}[/red]")
        return False

def process_intermediate_file(file_path: str, driver, processed_files: Set[str]) -> bool:
    try:
        with open(file_path, 'r') as f:
            file_data = json.load(f)
        
        for result in file_data.get('results', []):
            # Check if data was previously validated
            if result.get('validated'):
                console.print(f"[blue]Found pre-validated data from {result['validation_timestamp']}[/blue]")
                
                # Still validate as safety check before Neo4j
                if validate_neo4j_data(result['data']):
                    store_to_neo4j(result['data'], driver)
                else:
                    console.print("[red]Secondary validation failed[/red]")
                    continue
            else:
                console.print("[yellow]Data not pre-validated, running full validation[/yellow]")
                if not validate_neo4j_data(result):
                    continue
                    
        return True
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
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
        
        # Initialize processing
        console.print("[blue]Starting data processing...[/blue]")
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
    try:
        # First, remove all existing constraints to start fresh
        try:
            session.run("DROP CONSTRAINT ON (n:State) ASSERT n.name IS UNIQUE")
            console.print("[green]Dropped name constraint on State nodes[/green]")
        except Exception:
            pass  # Ignore if constraint doesn't exist
            
        try:
            session.run("DROP CONSTRAINT ON (n:NetworkElement) ASSERT n.name IS UNIQUE")
            console.print("[green]Dropped name constraint on NetworkElement nodes[/green]")
        except Exception:
            pass  # Ignore if constraint doesn't exist
            
        try:
            session.run("DROP CONSTRAINT ON (n:State) ASSERT n.id IS UNIQUE")
            console.print("[green]Dropped id constraint on State nodes[/green]")
        except Exception:
            pass  # Ignore if constraint doesn't exist

        # Create new constraints
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:NetworkElement) REQUIRE n.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:State) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Event) REQUIRE n.id IS UNIQUE"
    ]
    
    for constraint in constraints:
            session.run(constraint)
            console.print(f"[green]Created constraint: {constraint}[/green]")
            
    except Exception as e:
        console.print(f"[red]Error creating constraints: {str(e)}[/red]")
        raise

def store_states(session, states: List[Dict], trigger: str):
    """Store states in Neo4j with element and state type information."""
    try:
        for state in states:
            # Create a unique ID that includes the trigger, element, and state name
            state_name = state['label'].split(':')[-1].strip()
            state_id = hashlib.md5(f"{state_name}_{state['element']}_{trigger}".encode()).hexdigest()
            
            # First ensure the network element exists
            session.run("""
                MERGE (e:NetworkElement {name: $element})
            """, {'element': state.get('element')})
            
            # Then create or update the state with its unique ID
            session.run("""
                MERGE (s:State {id: $id})
                ON CREATE SET
                    s.label = $label,
                    s.name = $name,
                    s.type = $type,
                    s.element = $element,
                    s.state_type = $state_type,
                    s.trigger = $trigger
                ON MATCH SET
                    s.label = $label,
                    s.name = $name,
                    s.type = $type,
                    s.element = $element,
                    s.state_type = $state_type,
                    s.trigger = $trigger
                WITH s
                MATCH (e:NetworkElement {name: $element})
                MERGE (e)-[r:HAS_STATE]->(s)
            """, {
                'id': state_id,
                'label': state['label'],
                'name': f"{state_name}_{state.get('element')}_{trigger}",
                'type': state['type'],
                'element': state.get('element'),
                'state_type': state.get('state_type'),
                'trigger': trigger
            })
            console.print(f"[green]✓ Stored state: {state_name} for {state.get('element')}[/green]")
            
        console.print(f"[green]✓ Stored {len(states)} states for trigger: {trigger}[/green]")
        except Exception as e:
        console.print(f"[red]Error storing states: {str(e)}[/red]")
        raise

def store_events(session, events: List[Dict], trigger: str):
    """Store events in Neo4j with state transition information."""
    try:
        for event in events:
            # Create a unique ID that includes the trigger
            event_id = f"{event['id']}_{trigger}".replace(' ', '_')
            
            session.run("""
                MERGE (e:Event {id: $id})
                SET e.label = $label,
                    e.type = $type,
                    e.from_state = $from_state,
                    e.to_state = $to_state,
                    e.trigger = $trigger
            """, {
                'id': event_id,
                'label': event['label'],
                'type': event['type'],
                'from_state': event.get('from_state'),
                'to_state': event.get('to_state'),
                'trigger': trigger
            })
        console.print(f"[green]✓ Stored {len(events)} events for trigger: {trigger}[/green]")
    except Exception as e:
        console.print(f"[red]Error storing events: {str(e)}[/red]")
        raise

def store_transitions(session, edges: List[Dict], trigger: str):
    """Store transitions between nodes with state change information."""
    try:
        for edge in edges:
            # Create unique IDs for the nodes that include the trigger
            from_id = f"{edge['from']}_{trigger}".replace(' ', '_')
            to_id = f"{edge['to']}_{trigger}".replace(' ', '_')
            
            # Create the relationship with state transition info
            session.run("""
                MATCH (from) WHERE from.id = $from_id OR from.name = $from_id
                MATCH (to) WHERE to.id = $to_id OR to.name = $to_id
                MERGE (from)-[r:TRANSITIONS {
                    trigger: $trigger,
                    label: $label
                }]->(to)
                SET r.from_state = $from_state,
                    r.to_state = $to_state,
                    r.state_change = $state_change
            """, {
                'from_id': from_id,
                'to_id': to_id,
                'trigger': trigger,
                'label': edge['label'],
                'from_state': edge.get('from_state'),
                'to_state': edge.get('to_state'),
                'state_change': edge.get('state_change', '')
            })
        console.print(f"[green]✓ Stored {len(edges)} transitions for trigger: {trigger}[/green]")
    except Exception as e:
        console.print(f"[red]Error storing transitions: {str(e)}[/red]")
        console.print(f"[yellow]Edge data: {json.dumps(edge, indent=2)}[/yellow]")
        raise

def store_network_elements(session, elements: List[Dict]):
    """Store network elements with deduplication."""
    try:
    for element in elements:
            # Get the name from either 'name' or 'label' field
            element_name = element.get('label', '').split('(')[0].strip()  # Extract name before parentheses
            if not element_name:
                console.print(f"[yellow]Warning: Skipping element with no name/label: {element}[/yellow]")
                continue

            # Create or update the network element
            cypher = """
            MERGE (n:NetworkElement {name: $name})
            SET n.type = $type,
                n.label = $label,
                n.description = $description
            """
            session.run(cypher, 
                       name=element_name,
                       type=element.get('type', 'NetworkElement'),
                       label=element.get('label', element_name),
                       description=element.get('description', ''))
            console.print(f"[green]Stored network element: {element_name}[/green]")

    except Exception as e:
        console.print(f"[red]Error storing network element: {str(e)}[/red]")
        console.print(f"[yellow]Element data: {json.dumps(element, indent=2)}[/yellow]")
        raise

def store_procedure_flow(session, trigger: str, procedure: str, flow_steps: List[Dict]):
    """Store procedure flow information in Neo4j."""
    try:
        # First create trigger node if it doesn't exist
        session.run("""
            MERGE (t:Trigger {name: $trigger})
            SET t.procedure = $procedure,
                t.type = $procedure
        """, {
            'trigger': trigger,
            'procedure': procedure
        })
        
        # Create step nodes and relationships
        for i, step in enumerate(flow_steps):
            step_id = f"{procedure}_{trigger}_STEP_{i+1}"
            
            # Create or update the step node
            session.run("""
                MERGE (step:Step {id: $step_id})
                SET step.sequence_number = $seq_num,
                    step.message = $message,
                    step.procedure = $procedure,
                    step.from_state = $from_state,
                    step.to_state = $to_state,
                    step.state_change = $state_change
            """, {
                'step_id': step_id,
                'seq_num': step['sequence_number'],
                'message': step['message'],
                'procedure': procedure,
                'from_state': step.get('from_state'),
                'to_state': step.get('to_state'),
                'state_change': step.get('state_change')
            })
            
            # Create relationships between network elements and steps
            if step['source'] and step['target']:
                session.run("""
                    MATCH (step:Step {id: $step_id})
                    MATCH (source:NetworkElement {name: $source})
                    MATCH (target:NetworkElement {name: $target})
                    MERGE (source)-[r1:PARTICIPATES_IN]->(step)
                    MERGE (target)-[r2:PARTICIPATES_IN]->(step)
                    SET r1.role = 'source',
                        r2.role = 'target'
                """, {
                    'step_id': step_id,
                    'source': step['source'],
                    'target': step['target']
                })
        
        # Create flow relationships between steps
        for i in range(len(flow_steps) - 1):
            current_step_id = f"{procedure}_{trigger}_STEP_{i+1}"
            next_step_id = f"{procedure}_{trigger}_STEP_{i+2}"
            
            session.run("""
                MATCH (current:Step {id: $current_id})
                MATCH (next:Step {id: $next_id})
                MERGE (current)-[r:NEXT]->(next)
                SET r.procedure = $procedure,
                    r.trigger = $trigger
            """, {
                'current_id': current_step_id,
                'next_id': next_step_id,
                'procedure': procedure,
                'trigger': trigger
            })
        
        # Link trigger to first step
        first_step_id = f"{procedure}_{trigger}_STEP_1"
        session.run("""
            MATCH (t:Trigger {name: $trigger})
            MATCH (start:Step {id: $first_step_id})
            MERGE (t)-[:INITIATES]->(start)
        """, {
            'trigger': trigger,
            'first_step_id': first_step_id
        })
        
        console.print(f"[green]✓ Stored procedure flow for {procedure} - {trigger}[/green]")

        except Exception as e:
        console.print(f"[red]Error storing procedure flow: {str(e)}[/red]")
        raise

def store_metadata(session, metadata: Dict):
    """Store metadata information in Neo4j.
    
    Args:
        session: Neo4j session
        metadata (Dict): Dictionary containing metadata information
    """
    try:
        # Create metadata node with timestamp
        metadata_props = {
            'type': 'Registration_Metadata',
            'timestamp': metadata.get('timestamp', ''),
            'version': metadata.get('version', '1.0'),
            'source': metadata.get('source', ''),
            'parser_version': metadata.get('parser_version', '1.0')
        }

        # Create metadata node
        session.run("""
            MERGE (m:Metadata {type: $type})
            ON CREATE SET m += $props
            ON MATCH SET m += $props
        """, {'type': metadata_props['type'], 'props': metadata_props})

        console.print("[green]✓ Stored metadata[/green]")

    except Exception as e:
        console.print(f"[red]Error storing metadata: {str(e)}[/red]")
        raise

def store_procedure(session, procedure_name: str, trigger: str, description: str = ""):
    """Store procedure information in Neo4j."""
    try:
        session.run("""
            MERGE (p:Procedure {name: $name})
            SET p.description = $description,
                p.type = 'Registration'
            WITH p
            MATCH (t:Trigger {name: $trigger})
            MERGE (t)-[:BELONGS_TO]->(p)
        """, {
            'name': procedure_name,
            'description': description,
            'trigger': trigger
        })
        console.print(f"[green]✓ Stored procedure: {procedure_name}[/green]")
    except Exception as e:
        console.print(f"[red]Error storing procedure: {str(e)}[/red]")
        raise

def process_registration_data(file_path: str = "processed_data/registration_analysis_backup.json"):
    """Process and store registration data in Neo4j."""
    try:
        # Read the JSON file
        console.print(f"[blue]Reading data from: {file_path}[/blue]")
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Connect to Neo4j
        if not all([URI, USERNAME, PASSWORD]):
            raise ValueError("Missing Neo4j credentials. Check .env file.")

        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
            
        try:
            with driver.session() as session:
                # Create constraints
                create_unique_constraints(session)
                
                # Process each result
                results = data.get('raw_results', [])
                console.print(f"[blue]Found {len(results)} results to process[/blue]")
                
                for i, result in enumerate(results, 1):
                    console.print(f"\n[blue]Processing result {i} of {len(results)}[/blue]")
                    
                    # Get raw_data, handling both error and success cases
                    raw_data = result.get('raw_data')
                    if not raw_data:
                        console.print("[yellow]Skipping result with no raw_data[/yellow]")
                        continue
                    
                    if not isinstance(raw_data, dict):
                        console.print("[yellow]Skipping result with invalid raw_data format[/yellow]")
                        continue
                    
                    # Extract procedure and trigger information
                    procedure = raw_data.get('procedure', 'Initial Registration')
                    trigger = raw_data.get('trigger', 'default')
                    description = raw_data.get('description', '')
                    console.print(f"\n[blue]Processing {procedure} data for trigger: {trigger}[/blue]")
                    
                    # Store the procedure node first
                    store_procedure(session, procedure, trigger, description)
                    
                    # Store network elements
                    network_elements = [n for n in raw_data.get('nodes', []) 
                                     if n['type'] == 'NetworkElement']
                    console.print(f"[blue]Found {len(network_elements)} network elements[/blue]")
                    store_network_elements(session, network_elements)
                    
                    # Store states with trigger information
                    states = [n for n in raw_data.get('nodes', []) 
                            if n['type'] == 'State']
                    console.print(f"[blue]Found {len(states)} states[/blue]")
                    store_states(session, states, trigger)
                    
                    # Store events with trigger information
                    events = [n for n in raw_data.get('nodes', []) 
                            if n['type'] == 'Event']
                    console.print(f"[blue]Found {len(events)} events[/blue]")
                    store_events(session, events, trigger)
                    
                    # Store transitions/edges with trigger information
                    edges = raw_data.get('edges', [])
                    console.print(f"[blue]Found {len(edges)} edges[/blue]")
                    
                    # Create procedure flow steps from edges
                    flow_steps = []
                    for idx, edge in enumerate(edges, 1):
                        step = {
                            'sequence_number': idx,
                            'source': edge.get('from'),
                            'target': edge.get('to'),
                            'message': edge.get('label', ''),
                            'from_state': edge.get('from_state'),
                            'to_state': edge.get('to_state'),
                            'state_change': edge.get('state_change'),
                            'procedure': procedure
                        }
                        flow_steps.append(step)
                    
                    # Store the procedure flow
                    store_procedure_flow(session, trigger, procedure, flow_steps)
                    
                    # Store metadata if available
                    if 'metadata' in raw_data:
                        metadata = raw_data['metadata']
                        metadata['timestamp'] = datetime.now().isoformat()
                        store_metadata(session, metadata)
                    
                    console.print(f"[green]✓ Completed processing trigger: {trigger}[/green]")
                        
                console.print("\n[green]✓ Successfully stored all registration data[/green]")
                
        finally:
            driver.close()
            
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in file: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error processing data: {str(e)}[/red]")
        console.print(traceback.format_exc())

if __name__ == "__main__":
    process_registration_data()