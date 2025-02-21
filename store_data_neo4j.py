import os
import re
import json
from typing import List, Dict, Tuple
from pypdf import PdfReader
from neo4j import GraphDatabase
import hashlib
from rich.console import Console

console = Console()

# Neo4j Configuration (from environment variables)
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Cache file for Neo4j state
NEO4J_CACHE_FILE = "neo4j_cache.json"

from neo4j import GraphDatabase

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

def store_in_neo4j(processed_docs):
    """Store extracted entities and relationships in Neo4j."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    if not password:
        console.print("[red]Error: NEO4J_PASSWORD environment variable is not set[/red]")
        return False

    # Test connection first
    console.print("[blue]Testing Neo4j connection...[/blue]")
    success, message = test_neo4j_connection(uri, username, password)
    if not success:
        console.print(f"[red]Neo4j connection failed: {message}[/red]")
        console.print("[yellow]Please ensure:[/yellow]")
        console.print("[yellow]1. Neo4j is running[/yellow]")
        console.print("[yellow]2. Credentials in .env file are correct[/yellow]")
        console.print(f"[yellow]3. Neo4j is accepting connections on {uri}[/yellow]")
        return False

    if success:
        console.print("[green]Neo4j connection successful[/green]")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            # Clear existing data
            console.print("[blue]Clearing existing database...[/blue]")
            session.run("MATCH (n) DETACH DELETE n")
            
            console.print("[blue]Storing new entities and relationships...[/blue]")
            for doc in processed_docs:
                entities = doc["entities"]
                relationships = doc["relationships"]

                # Create nodes for each entity
                for entity, entity_type in entities:
                    try:
                        session.run(
                            "MERGE (e:Entity {name: $name}) SET e.type = $type",
                            name=entity,
                            type=entity_type
                        )
                    except Exception as e:
                        console.print(f"[red]Error creating entity '{entity}': {str(e)}[/red]")

                # Create relationships between entities
                for entity1, entity2, relationship_type, properties in relationships:
                    try:
                        # Convert relationship type to valid Neo4j format (remove spaces, uppercase)
                        neo4j_rel_type = re.sub(r'\s+', '_', relationship_type).upper()
                        cypher = f"""
                        MATCH (e1:Entity {{name: $entity1}}), (e2:Entity {{name: $entity2}})
                        MERGE (e1)-[r:{neo4j_rel_type}]->(e2)
                        SET r += $properties
                        """
                        session.run(cypher, entity1=entity1, entity2=entity2, properties=properties)
                    except Exception as e:
                        console.print(f"[red]Error creating relationship between '{entity1}' and '{entity2}': {str(e)}[/red]")

        driver.close()
        console.print("[green]Data successfully stored in Neo4j![/green]")
        return True

    except Exception as e:
        console.print(f"[red]Error storing data in Neo4j: {str(e)}[/red]")
        return False