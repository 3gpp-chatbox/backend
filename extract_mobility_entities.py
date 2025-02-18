import os
from neo4j import GraphDatabase
import re

# Neo4j Configuration (from environment variables)
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Define key entities and relationships
entities = [
    {"name": "User Equipment", "type": "UE", "properties": {"ID": "", "Status": "", "Registration_Time": ""}},
    {"name": "Access and Mobility Management Function", "type": "AMF", "properties": {"AMF_ID": "", "Location": ""}},
    {"name": "Registration", "type": "Registration", "properties": {"Type": "", "Status": "", "Timestamp": ""}},
    {"name": "Deregistration", "type": "Deregistration", "properties": {"Type": "", "Status": "", "Timestamp": ""}},
    {"name": "Connection", "type": "Connection", "properties": {"Connection_Status": "", "Connection_Type": ""}},
    {"name": "Network Area", "type": "Network_Area", "properties": {"Area_Code": "", "PLMN_ID": ""}},
    {"name": "Mobility Event", "type": "Mobility_Event", "properties": {"Event_Type": ""}},
    {"name": "Procedure Type", "type": "Procedure_Type", "properties": {"Type": ""}},
]

relationships = [
    {"from": "User Equipment", "to": "Access and Mobility Management Function", "type": "REGISTERS_WITH"},
    {"from": "User Equipment", "to": "Access and Mobility Management Function", "type": "DEREGISTERS_FROM"},
    {"from": "User Equipment", "to": "Network Area", "type": "MOVES_TO"},
    {"from": "Access and Mobility Management Function", "to": "Mobility Event", "type": "HANDLES"},
]

def store_in_neo4j(extracted_entities, extracted_relationships):
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    with driver.session() as session:
        # Create nodes for each extracted entity
        for entity in extracted_entities:
            session.run(
                "MERGE (e:Entity {name: $name, type: $type}) "
                "SET e += $properties",
                name=entity["name"],
                type=entity["type"],
                properties=entity["properties"]
            )

        # Create relationships between extracted entities
        for relationship in extracted_relationships:
            session.run(
                f"""
                MATCH (e1:Entity {{name: $from}}), (e2:Entity {{name: $to}})
                MERGE (e1)-[r:{relationship['type']}]->(e2)
                """,
                from=relationship["from"],
                to=relationship["to"]
            )

    driver.close()

def extract_entities_and_relationships(documents):
    """Extract entities and relationships from the documents using regex patterns."""
    extracted_entities = []
    extracted_relationships = []

    # Define regex patterns for entities and relationships
    entity_patterns = {
        "UE": r'\b(?:User Equipment|UE)\b',
        "AMF": r'\b(?:Access and Mobility Management Function|AMF)\b',
        "Registration": r'\b(?:Registration)\b',
        "Deregistration": r'\b(?:Deregistration)\b',
        "Connection": r'\b(?:Connection)\b',
        "Network Area": r'\b(?:Network Area)\b',
        "Mobility Event": r'\b(?:Mobility Event)\b',
        "Procedure Type": r'\b(?:Procedure Type)\b',
    }

    relationship_patterns = {
        "REGISTERS_WITH": r'\b(?:UE|User Equipment)\s+(?:registers|attaches)\s+(?:with|to)\s+(?:AMF)\b',
        "DEREGISTERS_FROM": r'\b(?:UE|User Equipment)\s+(?:deregisters|detaches)\s+(?:from)\s+(?:AMF)\b',
        "MOVES_TO": r'\b(?:UE|User Equipment)\s+(?:moves|enters|leaves)\s+(?:Network Area)\b',
        "HANDLES": r'\b(?:AMF)\s+(?:handles|manages)\s+(?:Mobility Event)\b',
    }

    for doc in documents:
        text = doc["text"]

        # Extract entities
        for entity_type, pattern in entity_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                extracted_entities.append({
                    "name": match,
                    "type": entity_type,
                    "properties": {}  # Add any relevant properties if needed
                })

        # Extract relationships
        for rel_type, pattern in relationship_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                # Assuming the relationship involves UE and AMF
                extracted_relationships.append({
                    "from": "User Equipment",  # Adjust based on actual extraction
                    "to": "Access and Mobility Management Function",  # Adjust based on actual extraction
                    "type": rel_type
                })

    return extracted_entities, extracted_relationships

if __name__ == "__main__":
    from preprocess_pdfs import read_pdfs_from_directory

    data_dir = "data"  # Specify your data directory
    documents = read_pdfs_from_directory(data_dir)
    extracted_entities, extracted_relationships = extract_entities_and_relationships(documents)
    store_in_neo4j(extracted_entities, extracted_relationships) 