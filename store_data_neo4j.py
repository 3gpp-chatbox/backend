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

def load_neo4j_cache() -> Dict:
    """Load Neo4j cache containing file hashes of previously processed documents"""
    if os.path.exists(NEO4J_CACHE_FILE):
        try:
            with open(NEO4J_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load Neo4j cache file: {str(e)}")
    return {"processed_files": {}}

def save_neo4j_cache(cache: Dict):
    """Save Neo4j cache"""
    try:
        with open(NEO4J_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save Neo4j cache file: {str(e)}")

def get_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    file_path = os.path.normpath(file_path)
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        """Clear all nodes and relationships from the database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_entity(self, entity_name: str, entity_type: str):
        """Create a node in Neo4j"""
        with self.driver.session() as session:
            session.run(
                """
                MERGE (n:Entity {name: $name})
                SET n.type = $type
                """,
                name=entity_name, type=entity_type
            )

    def create_relationship(self, entity1: str, entity2: str, relationship: str, properties: Dict = None):
        """Create a relationship between two nodes with properties"""
        # Convert relationship type to a valid Neo4j relationship type (remove spaces, uppercase)
        rel_type = relationship.replace(" ", "_").upper()
        
        # Base query
        query = f"""
        MATCH (a:Entity {{name: $name1}})
        MATCH (b:Entity {{name: $name2}})
        MERGE (a)-[r:{rel_type}]->(b)
        """
        
        # Add properties if they exist
        if properties:
            property_sets = []
            for prop_type, values in properties.items():
                if values:
                    property_sets.append(f"r.{prop_type} = ${prop_type}")
            
            if property_sets:
                query += "SET " + ", ".join(property_sets)
        
        # Execute query with parameters
        params = {"name1": entity1, "name2": entity2}
        if properties:
            params.update(properties)
            
        with self.driver.session() as session:
            session.run(query, params)

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
    neo4j_cache = load_neo4j_cache()
    
    try:
        # Check if any files have changed
        files_changed = False
        current_files = {}
        
        for doc in documents:
            file_path = doc["metadata"]["file_path"]
            file_hash = get_file_hash(file_path)
            current_files[file_path] = file_hash
            
            if (file_path not in neo4j_cache["processed_files"] or 
                neo4j_cache["processed_files"][file_path] != file_hash):
                files_changed = True
                break
        
        # If no files have changed, skip database update
        if not files_changed and neo4j_cache["processed_files"]:
            print("💾 No changes detected in documents. Using existing Neo4j database.")
            return
        
        # If files have changed, clear and rebuild database
        print("🔄 Changes detected in documents. Updating Neo4j database...")
        print("🗑️ Clearing existing database...")
        graph.clear_database()
        
        print("📥 Storing new entities and relationships...")
        for doc in documents:
            # Store entities
            for entity_text, entity_type in doc["entities"]:
                graph.create_entity(entity_text, entity_type)

            # Store relationships with properties
            for entity1, entity2, relation, properties in doc["relationships"]:
                graph.create_relationship(entity1, entity2, relation, properties)
        
        # Update cache with current file hashes
        neo4j_cache["processed_files"] = current_files
        save_neo4j_cache(neo4j_cache)
        
        print("✅ Data successfully stored in Neo4j!")
        
    except Exception as e:
        print(f"❌ Error storing data in Neo4j: {str(e)}")
        raise e
    finally:
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
