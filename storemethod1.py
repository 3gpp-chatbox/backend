import os
import json
from typing import Dict, List
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

class Method1GraphStorage:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        """Create necessary constraints for the database."""
        with self.driver.session() as session:
            try:
                # Create constraints for different node types
                constraints = [
                    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:State) REQUIRE n.id IS UNIQUE",
                    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Event) REQUIRE n.id IS UNIQUE",
                    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Procedure) REQUIRE n.name IS UNIQUE"
                ]
                
                for constraint in constraints:
                    session.run(constraint)
                console.print("[green]Created database constraints successfully[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning creating constraints: {str(e)}[/yellow]")

    def store_procedure(self, procedure_name: str):
        """Store the procedure node."""
        try:
            with self.driver.session() as session:
                session.run("""
                    MERGE (p:Procedure {name: $name})
                """, {'name': procedure_name})
                console.print(f"[green]✓ Stored procedure: {procedure_name}[/green]")
        except Exception as e:
            console.print(f"[red]Error storing procedure: {str(e)}[/red]")
            raise

    def store_node(self, node: Dict, procedure_name: str):
        """Store a node with all its properties."""
        try:
            with self.driver.session() as session:
                # Extract primitive properties and convert nested objects to JSON
                properties = {}
                for key, value in node.get('properties', {}).items():
                    if isinstance(value, (str, int, float, bool)) or (isinstance(value, list) and all(isinstance(x, (str, int, float, bool)) for x in value)):
                        properties[key] = value
                    else:
                        properties[key] = json.dumps(value)

                metadata = {}
                for key, value in node.get('metadata', {}).items():
                    if isinstance(value, (str, int, float, bool)) or (isinstance(value, list) and all(isinstance(x, (str, int, float, bool)) for x in value)):
                        metadata[key] = value
                    else:
                        metadata[key] = json.dumps(value)

                # Create the node with its type label and properties
                session.run("""
                    MERGE (n:`%s` {id: $id})
                    SET n += $properties
                    SET n += $metadata
                    SET n.entity = $entity
                    WITH n
                    MATCH (p:Procedure {name: $procedure})
                    MERGE (n)-[:BELONGS_TO]->(p)
                """ % node['type'], {
                    'id': node['id'],
                    'properties': properties,
                    'metadata': metadata,
                    'entity': node['entity'],
                    'procedure': procedure_name
                })
                console.print(f"[green]✓ Stored {node['type']} node: {node['id']}[/green]")
        except Exception as e:
            console.print(f"[red]Error storing node: {str(e)}[/red]")
            raise

    def store_edge(self, edge: Dict, procedure_name: str):
        """Store an edge with all its properties."""
        try:
            with self.driver.session() as session:
                # Extract primitive properties and convert nested objects to JSON
                properties = {}
                for key, value in edge.get('properties', {}).items():
                    if isinstance(value, (str, int, float, bool)) or (isinstance(value, list) and all(isinstance(x, (str, int, float, bool)) for x in value)):
                        properties[key] = value
                    else:
                        properties[key] = json.dumps(value)

                # Create the relationship with its type and properties
                session.run("""
                    MATCH (from {id: $from_id})
                    MATCH (to {id: $to_id})
                    MERGE (from)-[r:`%s` {id: $edge_id}]->(to)
                    SET r += $properties
                    SET r.procedure = $procedure
                """ % edge['type'], {
                    'from_id': edge['from'],
                    'to_id': edge['to'],
                    'edge_id': edge['id'],
                    'properties': properties,
                    'procedure': procedure_name
                })
                console.print(f"[green]✓ Stored edge: {edge['id']}[/green]")
        except Exception as e:
            console.print(f"[red]Error storing edge: {str(e)}[/red]")
            raise

def process_method1_graph(file_path: str = "graphs/method 1/initial_registration_procedure_20250306_1642_graph.json"):
    """Process and store the method 1 graph data."""
    try:
        # Read the JSON file
        console.print(f"[blue]Reading data from: {file_path}[/blue]")
        with open(file_path, 'r') as f:
            data = json.load(f)

        storage = Method1GraphStorage()
        
        try:
            # Create constraints
            storage.create_constraints()
            
            # Store procedure
            procedure_name = data['procedureName']
            storage.store_procedure(procedure_name)
            
            # Store all nodes
            for node in data['nodes']:
                storage.store_node(node, procedure_name)
            
            # Store all edges
            for edge in data['edges']:
                storage.store_edge(edge, procedure_name)

            console.print("[green]✓ Successfully stored method 1 graph data[/green]")
            
        finally:
            storage.close()

    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
    except json.JSONDecodeError:
        console.print(f"[red]Error: Invalid JSON in file: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error processing data: {str(e)}[/red]")
        console.print(traceback.format_exc())

if __name__ == "__main__":
    process_method1_graph() 