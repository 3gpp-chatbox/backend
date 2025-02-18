import os
import re
import json
from typing import List, Dict, Tuple
from pypdf import PdfReader
from neo4j import GraphDatabase
import hashlib

# Neo4j Configuration (from environment variables)
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Cache file for Neo4j state
NEO4J_CACHE_FILE = "neo4j_cache.json"

from neo4j import GraphDatabase

def store_in_neo4j(processed_docs):
    """Store extracted entities and relationships in Neo4j."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        for doc in processed_docs:
            entities = doc["entities"]
            relationships = doc["relationships"]

            # Create nodes for each entity
            for entity, entity_type in entities:
                try:
                    session.run(
                        "MERGE (e:Entity {name: $name, type: $type})",
                        name=entity,
                        type=entity_type
                    )
                except Exception as e:
                    print(f"Error creating entity '{entity}': {str(e)}")

            # Create relationships between entities
            for entity1, entity2, relationship_type, properties in relationships:
                try:
                    session.run(
                        """
                        MATCH (e1:Entity {name: $entity1}), (e2:Entity {name: $entity2})
                        MERGE (e1)-[r:RELATIONSHIP_TYPE {type: $relationship_type}]->(e2)
                        """,
                        entity1=entity1,
                        entity2=entity2,
                        relationship_type=relationship_type
                    )
                except Exception as e:
                    print(f"Error creating relationship between '{entity1}' and '{entity2}': {str(e)}")

    driver.close()