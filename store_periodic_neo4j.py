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
                for i, step in enumerate(flow_steps):
                    source = step.get('source')
                    target = step.get('target')
                    if not source or not target:
                        continue

                    message_props = {
                        'name': step.get('message', ''),
                        'step_number': i + 1,
                        'procedure': 'Periodic_Registration',
                        'trigger': trigger,
                        'description': step.get('description', ''),
                        'specification': step.get('specification', ''),
                        'section': step.get('section', '')
                    }

                    # Use MERGE to avoid duplicates
                    session.run("""
                        MATCH (source:NetworkElement {name: $source})
                        MATCH (target:NetworkElement {name: $target})
                        MERGE (source)-[r:SENDS_MESSAGE {
                            procedure: $procedure,
                            trigger: $trigger,
                            step_number: $step_number
                        }]->(target)
                        ON CREATE SET r += $props
                        ON MATCH SET r += $props
                    """, {
                        'source': source,
                        'target': target,
                        'procedure': 'Periodic_Registration',
                        'trigger': trigger,
                        'step_number': i + 1,
                        'props': message_props
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
                    CREATE (m:Metadata)
                    SET m += $props
                """, {'props': metadata_props})

                console.print("[green]✓ Stored metadata[/green]")

        except Exception as e:
            console.print(f"[red]Error storing metadata: {str(e)}[/red]")
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
            
            # Store network elements (these are shared across triggers)
            if 'network_elements' in data:
                neo4j_handler.store_network_elements(data['network_elements'])

            # Process each trigger's data separately
            for trigger_data in data.get('triggers', []):
                trigger_name = trigger_data.get('name')
                if trigger_name:
                    # Store trigger data
                    neo4j_handler.store_trigger(trigger_data)
                    
                    # Store procedure flow for this trigger
                    if 'procedure_flow' in trigger_data:
                        neo4j_handler.store_procedure_flow(trigger_name, trigger_data['procedure_flow'])
                    
                    # Store metadata if present
                    if 'metadata' in trigger_data:
                        neo4j_handler.store_metadata(trigger_data['metadata'])

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