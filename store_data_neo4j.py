import os
import re
from typing import List, Dict, Tuple
from pypdf import PdfReader
from neo4j import GraphDatabase

# Neo4j Configuration (from environment variables)
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_entity(self, entity_name: str, entity_type: str):
        """Create a node in Neo4j"""
        with self.driver.session() as session:
            session.run(
                "MERGE (n:Entity {name: $name, type: $type})",
                name=entity_name, type=entity_type
            )

    def create_relationship(self, entity1: str, entity2: str, relationship: str):
        """Create a relationship between two nodes"""
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Entity {name: $name1})
                MATCH (b:Entity {name: $name2})
                MERGE (a)-[:RELATION {type: $rel}]->(b)
                """,
                name1=entity1, name2=entity2, rel=relationship
            )

def extract_text_from_pdfs(directory: str) -> List[Dict[str, str]]:
    """Extracts text from PDFs in a given directory"""
    documents = []
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} not found")

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                pdf_reader = PdfReader(file_path)
                text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                
                if text.strip():
                    documents.append({
                        "text": text,
                        "metadata": {"source": filename, "file_path": file_path}
                    })
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    return documents

def extract_entities(text: str) -> List[Tuple[str, str]]:
    """Extracts key entities (e.g., procedures, messages) using regex"""
    entities = []
    
    # Example Regex Patterns (Modify as needed)
    procedure_pattern = re.findall(r'\b(?:Attach Request|Detach Request|Authentication Response)\b', text)
    message_pattern = re.findall(r'\b(?:NAS Message|ESM Message|EPS Bearer Context)\b', text)

    for proc in procedure_pattern:
        entities.append((proc, "Procedure"))
    
    for msg in message_pattern:
        entities.append((msg, "Message"))

    return list(set(entities))  # Remove duplicates

def extract_relationships(text: str, entities: List[Tuple[str, str]]) -> List[Tuple[str, str, str]]:
    """Finds relationships between entities"""
    relationships = []

    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            entity1, type1 = entities[i]
            entity2, type2 = entities[j]

            # Example: If both entities appear in the same sentence, create a relation
            if entity1 in text and entity2 in text:
                relationships.append((entity1, entity2, "RELATED_TO"))

    return relationships

def store_in_neo4j(documents: List[Dict]):
    """Stores extracted entities and relationships in Neo4j"""
    graph = KnowledgeGraph(URI, USERNAME, PASSWORD)

    for doc in documents:
        # Store entities in Neo4j
        for entity_text, entity_type in doc["entities"]:
            graph.create_entity(entity_text, entity_type)

        # Store relationships in Neo4j
        for entity1, entity2, relation in doc["relationships"]:
            graph.create_relationship(entity1, entity2, relation)

    graph.close()

if __name__ == "__main__":
    DATA_DIR = "data"
    
    print("📂 Extracting text from PDFs...")
    documents = extract_text_from_pdfs(DATA_DIR)

    if not documents:
        print("❌ No documents found.")
    else:
        print(f"✅ Extracted {len(documents)} documents.")

        print("🧠 Storing entities & relationships in Neo4j...")
        store_in_neo4j(documents)
        print("✅ Data successfully stored in Neo4j!")
