import os
import json
from typing import Dict, List, Optional
from neo4j import GraphDatabase
from rich.console import Console
from dotenv import load_dotenv
import traceback
from datetime import datetime

# Initialize console and load environment variables
console = Console()
load_dotenv()

# Neo4j Configuration
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class PeriodicRegistrationNeo4j:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        """Create necessary constraints for the database."""
        with self.driver.session() as session:
            try:
                # Create constraints for NetworkElement nodes
                session.run("""
                    CREATE CONSTRAINT IF NOT EXISTS FOR (n:NetworkElement)
                    REQUIRE n.name IS UNIQUE
                """)
                
                # Create constraints for Trigger nodes
                session.run("""
                    CREATE CONSTRAINT IF NOT EXISTS FOR (t:Trigger)
                    REQUIRE t.name IS UNIQUE
                """)
                
                # Create constraints for State nodes
                session.run("""
                    CREATE CONSTRAINT IF NOT EXISTS FOR (s:State)
                    REQUIRE s.name IS UNIQUE
                """)
                
                # Add constraint for Procedure nodes
                session.run("""
                    CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure)
                    REQUIRE p.name IS UNIQUE
                """)
                
                console.print("[green]Created database constraints successfully[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning creating constraints: {str(e)}[/yellow]")

    def store_network_elements(self, elements: List[Dict]):
        """Store network elements in Neo4j."""
        with self.driver.session() as session:
            for element in elements:
                try:
                    session.run("""
                        MERGE (n:NetworkElement {name: $name})
                        ON CREATE SET n.type = $type,
                                    n.description = $description
                        ON MATCH SET n.type = CASE 
                            WHEN n.type IS NULL THEN $type 
                            ELSE n.type END,
                            n.description = CASE 
                            WHEN n.description IS NULL THEN $description 
                            ELSE n.description END
                    """, {
                        "name": element["name"],
                        "type": element.get("type", "NetworkElement"),
                        "description": element.get("description", "")
                    })
                except Exception as e:
                    console.print(f"[red]Error storing network element {element.get('name')}: {str(e)}[/red]")

    def store_state(self, state_type: str):
        """Store state type in Neo4j."""
        try:
            with self.driver.session() as session:
                session.run("""
                    MERGE (s:State {name: $state_type})
                    ON CREATE SET s.type = 'State',
                                s.description = 'NAS State'
                """, {"state_type": state_type})
                console.print(f"[green]✓ Stored state: {state_type}[/green]")
        except Exception as e:
            console.print(f"[red]Error storing state {state_type}: {str(e)}[/red]")

    def store_trigger(self, trigger_data: dict):
        """Store trigger information in Neo4j."""
        try:
            with self.driver.session() as session:
                trigger_name = trigger_data.get('name')
                if not trigger_name:
                    raise ValueError("Trigger data must contain a 'name' field")

                trigger_props = {
                    'name': trigger_name,
                    'type': 'Periodic_Registration',
                    'description': trigger_data.get('description', ''),
                    'specification': trigger_data.get('specification', ''),
                    'section': trigger_data.get('section', '')
                }

                session.run("""
                    MERGE (t:Trigger {name: $name})
                    ON CREATE SET t += $props
                    ON MATCH SET t += $props
                """, {'name': trigger_name, 'props': trigger_props})

                console.print(f"[green]✓ Stored trigger: {trigger_name}[/green]")

        except Exception as e:
            console.print(f"[red]Error storing trigger data: {str(e)}[/red]")
            raise

    def store_procedure_flow(self, trigger: str, flow_steps: List[Dict]):
        """Store procedure flow information in Neo4j."""
        try:
            with self.driver.session() as session:
                # First create all step nodes
                for i, step in enumerate(flow_steps):
                    state_type = step.get('state_type', '5GMM-REGISTERED')
                    step_id = f"STEP_{i+1}"
                    
                    # Ensure the state exists
                    self.store_state(state_type)
                    
                    # Create step node with all properties
                    session.run("""
                        MERGE (step:Step {id: $step_id})
                        SET step.name = $name,
                            step.description = $description,
                            step.step_number = $step_number,
                            step.procedure = $procedure,
                            step.trigger = $trigger,
                            step.message_type = $message_type,
                            step.source = $source,
                            step.target = $target,
                            step.state_type = $state_type
                    """, {
                        'step_id': step_id,
                        'name': step.get('message', ''),
                        'description': step.get('description', ''),
                        'step_number': i + 1,
                        'procedure': 'Periodic_Registration',
                        'trigger': trigger,
                        'message_type': step.get('message_type', ''),
                        'source': step.get('source', ''),
                        'target': step.get('target', ''),
                        'state_type': state_type
                    })

                    # Create relationships to network elements
                    session.run("""
                        MATCH (step:Step {id: $step_id})
                        MATCH (source:NetworkElement {name: $source})
                        MATCH (target:NetworkElement {name: $target})
                        MATCH (state:State {name: $state_type})
                        MERGE (source)-[:PARTICIPATES_IN]->(step)
                        MERGE (target)-[:PARTICIPATES_IN]->(step)
                        MERGE (step)-[:HAS_STATE]->(state)
                    """, {
                        'step_id': step_id,
                        'source': step.get('source', ''),
                        'target': step.get('target', ''),
                        'state_type': state_type
                    })

                # Create flow relationships between steps
                for i in range(len(flow_steps) - 1):
                    current_step_id = f"STEP_{i+1}"
                    next_step_id = f"STEP_{i+2}"
                    
                    # Create NEXT relationship between steps
                    session.run("""
                        MATCH (current:Step {id: $current_id})
                        MATCH (next:Step {id: $next_id})
                        MERGE (current)-[r:NEXT]->(next)
                        SET r.procedure = $procedure,
                            r.trigger = $trigger
                    """, {
                        'current_id': current_step_id,
                        'next_id': next_step_id,
                        'procedure': 'Periodic_Registration',
                        'trigger': trigger
                    })

                # Link to trigger node
                session.run("""
                    MATCH (t:Trigger {name: $trigger})
                    MATCH (start:Step {id: 'STEP_1'})
                    MERGE (t)-[:INITIATES]->(start)
                """, {
                    'trigger': trigger
                })

                console.print(f"[green]✓ Stored procedure flow for trigger: {trigger}[/green]")

        except Exception as e:
            console.print(f"[red]Error storing procedure flow: {str(e)}[/red]")
            raise

    def store_metadata(self, metadata: Dict):
        """Store metadata information in Neo4j.
        
        Args:
            metadata (Dict): Dictionary containing metadata information
        """
        try:
            with self.driver.session() as session:
                # Create metadata node
                metadata_props = {
                    'type': 'Periodic_Registration_Metadata',
                    'timestamp': metadata.get('timestamp', ''),
                    'version': metadata.get('version', ''),
                    'source': metadata.get('source', ''),
                    'parser_version': metadata.get('parser_version', '')
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

    def store_procedure(self, procedure_name: str, trigger: str, description: str = ""):
        """Store procedure information in Neo4j."""
        try:
            with self.driver.session() as session:
                session.run("""
                    MERGE (p:Procedure {name: $name})
                    SET p.description = $description,
                        p.type = 'Periodic_Registration'
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

def process_periodic_registration_data(file_path: str = "processed_data/periodic_registration_analysis.json"):
    """Process and store periodic registration data."""
    try:
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        neo4j_handler = PeriodicRegistrationNeo4j()
        
        try:
            # Create constraints
            neo4j_handler.create_constraints()
            
            # Process results array
            results = data.get('results', [])
            if not results:
                console.print("[yellow]No results found in the data[/yellow]")
                return

            for result in results:
                # Store procedure first
                procedure_name = "Periodic Registration"
                trigger = result.get('trigger', '')
                description = result.get('description', '')
                neo4j_handler.store_procedure(procedure_name, trigger, description)

                # Store network elements
                if 'network_elements' in result:
                    neo4j_handler.store_network_elements(result['network_elements'])

                # Store trigger
                trigger_data = {
                    'name': result.get('trigger', ''),
                    'description': result.get('description', ''),
                    'specification': result.get('metadata', {}).get('specReference', ''),
                    'section': ''  # Add section if available in your data
                }
                neo4j_handler.store_trigger(trigger_data)

                # Store procedure flow with state types
                if 'procedure_flow' in result:
                    flow_steps = []
                    for step in result['procedure_flow']:
                        flow_step = {
                            'source': step['source'],
                            'target': step['target'],
                            'message': step['message'],
                            'description': step['description'],
                            'message_type': step.get('message_type', ''),
                            'parameters': step.get('parameters', []),
                            'conditions': step.get('conditions', []),
                            'outcome': step.get('outcome', ''),
                            'state_type': step.get('state_type', '5GMM-REGISTERED')  # Include state type
                        }
                        flow_steps.append(flow_step)
                    neo4j_handler.store_procedure_flow(trigger_data['name'], flow_steps)

                # Store metadata
                if 'metadata' in result:
                    metadata = {
                        'timestamp': datetime.now().isoformat(),
                        'version': '1.0',
                        'source': result['metadata'].get('specReference', ''),
                        'parser_version': '1.0',
                        'timer': result['metadata'].get('timer', '')
                    }
                    neo4j_handler.store_metadata(metadata)

            console.print("[green]✓ Successfully stored periodic registration data[/green]")
            
        finally:
            neo4j_handler.close()

    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in file: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error processing data: {str(e)}[/red]")
        console.print(traceback.format_exc())

if __name__ == "__main__":
    process_periodic_registration_data() 