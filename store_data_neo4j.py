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

    def create_entity(self, entity_name: str, entity_type: str, properties: Dict = None):
        """Create a node in Neo4j with properties"""
        with self.driver.session() as session:
            # Base query
            query = """
            MERGE (n:Entity {name: $name})
            SET n.type = $type
            """
            
            # Add properties if they exist
            if properties:
                for key, value in properties.items():
                    query += f"\nSET n.{key} = ${key}"
            
            # Execute query with parameters
            params = {"name": entity_name, "type": entity_type}
            if properties:
                params.update(properties)
            
            session.run(query, params)

    def create_relationship(self, entity1: str, entity2: str, relationship: str, properties: Dict = None):
        """Create a relationship between two nodes with properties"""
        # Convert relationship type to a valid Neo4j relationship type (remove spaces, uppercase)
        rel_type = relationship.replace(" ", "_").upper()
        
        # Base query with label-specific matching
        query = """
        MATCH (a)
        WHERE a.name = $name1
        MATCH (b)
        WHERE b.name = $name2
        MERGE (a)-[r:%s]->(b)
        """ % rel_type
        
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

    def create_implicit_relationships(self):
        """Create implicit relationships between entities based on 3GPP domain knowledge"""
        with self.driver.session() as session:
            # Add step-specific relationships
            relationships = [
                # Network Elements and Messages (only if they interact)
                """
                MATCH (n:Entity {type: 'NETWORK_ELEMENT'})
                MATCH (m:Entity {type: 'MESSAGE'})
                WHERE EXISTS((n)-[:SENDS|:RECEIVES]->(m))
                MERGE (n)-[:USES]->(m)
                """,
                
                # Messages and Procedures (only if explicitly related)
                """
                MATCH (m:Entity {type: 'MESSAGE'})
                MATCH (p:Entity {type: 'PROCEDURE'})
                WHERE EXISTS((m)-[:PART_OF|:USED_IN]->(p))
                MERGE (m)-[:PART_OF]->(p)
                """,
                
                # Procedures and States (only if there's a transition)
                """
                MATCH (p:Entity {type: 'PROCEDURE'})
                MATCH (s:Entity {type: 'STATE'})
                WHERE EXISTS((p)-[:TRANSITIONS_TO|:RESULTS_IN]->(s))
                MERGE (p)-[:TRANSITIONS_TO]->(s)
                """,
                
                # Protocol and Messages/Procedures (only if defined)
                """
                MATCH (p:Entity {type: 'PROTOCOL'})
                MATCH (m:Entity {type: 'MESSAGE'})
                WHERE EXISTS((p)-[:DEFINES]->(m))
                MERGE (p)-[:DEFINES]->(m)
                """,
                
                # Message sequence (only if there's a clear sequence)
                """
                MATCH (m1:Entity {type: 'MESSAGE'})
                MATCH (m2:Entity {type: 'MESSAGE'})
                WHERE EXISTS((m1)-[:PRECEDES|:TRIGGERS]->(m2))
                MERGE (m1)-[:FOLLOWED_BY]->(m2)
                """,
                
                # Procedure hierarchy (only for explicit sub-procedures)
                """
                MATCH (p1:Entity {type: 'PROCEDURE'})
                MATCH (p2:Entity {type: 'PROCEDURE'})
                WHERE EXISTS((p1)-[:INCLUDES|:CONTAINS]->(p2))
                MERGE (p1)-[:HAS_SUB_PROCEDURE]->(p2)
                """,
                
                # Connect steps to their procedures
                """
                MATCH (s:Entity {type: 'STEP'})
                MATCH (p:Entity {type: 'PROCEDURE'})
                WHERE EXISTS((s)-[:PART_OF]->(p))
                MERGE (p)-[:HAS_STEP]->(s)
                """,
                
                # Connect sequential steps
                """
                MATCH (s1:Entity {type: 'STEP'})
                MATCH (s2:Entity {type: 'STEP'})
                WHERE s1.sequence_number < s2.sequence_number
                AND s1.procedure_id = s2.procedure_id
                MERGE (s1)-[:FOLLOWED_BY]->(s2)
                """,
                
                # Connect steps to their sub-procedures
                """
                MATCH (s:Entity {type: 'STEP'})
                MATCH (sp:Entity {type: 'PROCEDURE'})
                WHERE EXISTS((s)-[:INITIATES]->(sp))
                MERGE (s)-[:TRIGGERS_SUB_PROCEDURE]->(sp)
                """,
                
                # Connect steps to their parameters
                """
                MATCH (s:Entity {type: 'STEP'})
                MATCH (p:Entity {type: 'PARAMETER'})
                WHERE EXISTS((s)-[:USES|:SETS|:REQUIRES]->(p))
                MERGE (s)-[:HAS_PARAMETER]->(p)
                """,
                
                # Connect steps to their conditions
                """
                MATCH (s:Entity {type: 'STEP'})
                MATCH (c:Entity {type: 'CONDITIONAL'})
                WHERE EXISTS((s)-[:DEPENDS_ON]->(c))
                MERGE (s)-[:HAS_CONDITION]->(c)
                """
            ]
            
            # Execute each relationship creation query
            for query in relationships:
                session.run(query)

    def store_procedure_flow(self, flow: Dict):
        """Store complete procedure flow in Neo4j"""
        procedure_name = flow['name']
        
        # Create procedure node
        self.create_entity(
            procedure_name,
            'PROCEDURE',
            {
                'specification': flow['metadata'].get('specification'),
                'section': flow['metadata'].get('section'),
                'release': flow['metadata'].get('release')
            }
        )
        
        # Store initial state
        if flow['initial_state']:
            self.create_entity(
                f"{procedure_name}_Initial_State",
                'STATE',
                {
                    'state': flow['initial_state']['state'],
                    'description': flow['initial_state']['description']
                }
            )
            self.create_relationship(
                procedure_name,
                f"{procedure_name}_Initial_State",
                'STARTS_FROM',
                {'type': 'initial_state'}
            )
        
        # Store final state
        if flow['final_state']:
            self.create_entity(
                f"{procedure_name}_Final_State",
                'STATE',
                {
                    'state': flow['final_state']['state'],
                    'description': flow['final_state']['description']
                }
            )
            self.create_relationship(
                procedure_name,
                f"{procedure_name}_Final_State",
                'ENDS_IN',
                {'type': 'final_state'}
            )
        
        # Store state transitions
        for transition in flow['state_transitions']:
            from_state = transition['from_state']
            to_state = transition['to_state']
            
            # Create state nodes
            self.create_entity(from_state, 'STATE', {'description': transition['description']})
            self.create_entity(to_state, 'STATE', {'description': transition['description']})
            
            # Create transition relationship
            self.create_relationship(
                from_state,
                to_state,
                'TRANSITIONS_TO',
                {'description': transition['description']}
            )
        
        # Store procedure steps
        prev_step = None
        for step in flow['steps']:
            step_name = f"{procedure_name}_Step_{step['step_number']}"
            
            # Create step node
            self.create_entity(
                step_name,
                'STEP',
                {
                    'message': step['message'],
                    'description': step['description'],
                    'sequence_number': step['step_number'],
                    'message_type': step['message_type'],
                    'context': step['context']
                }
            )
            
            # Link step to procedure
            self.create_relationship(
                procedure_name,
                step_name,
                'HAS_STEP',
                {'sequence': step['step_number']}
            )
            
            # Link to previous step
            if prev_step:
                self.create_relationship(
                    prev_step,
                    step_name,
                    'FOLLOWED_BY',
                    {'sequence_order': step['step_number']}
                )
            
            # Store parameters for this step
            for param in step['parameters']:
                param_name = f"{step_name}_Param_{param['name']}"
                self.create_entity(
                    param_name,
                    'PARAMETER',
                    {
                        'name': param['name'],
                        'description': param['description'],
                        'mandatory': param['mandatory']
                    }
                )
                self.create_relationship(
                    step_name,
                    param_name,
                    'HAS_PARAMETER'
                )
            
            # Store conditions for this step
            for condition in step['conditions']:
                cond_name = f"{step_name}_Condition_{hash(condition['condition'])}"
                self.create_entity(
                    cond_name,
                    'CONDITIONAL',
                    {
                        'condition': condition['condition'],
                        'context': condition['context']
                    }
                )
                self.create_relationship(
                    step_name,
                    cond_name,
                    'HAS_CONDITION'
                )
            
            prev_step = step_name

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

def extract_entities(text: str) -> List[Tuple[str, str, Dict]]:
    """Extracts all core NAS procedure components"""
    entities = []
    
    # Core component patterns
    patterns = {
        'STATE': [
            r'\b(?:5GMM|EMM|MM|CM|RRC)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
            r'\b(?:REGISTERED|DEREGISTERED|IDLE|CONNECTED)\s+(?:state|mode)\b',
            r'(?:enters?|transitions? to|remains? in)\s+(?:the\s+)?([A-Z-]+(?:\s+state|\s+mode)?)',
        ],
        'ACTION': [
            r'\b(?:sends?|transmits?|forwards?|initiates?|performs?|executes?)\s+(?:the\s+)?([A-Za-z\s]+)',
            r'\b(?:starts?|triggers?|launches?)\s+(?:the\s+)?([A-Za-z\s]+(?:procedure|process))',
            r'(?:shall|must|will)\s+([A-Za-z\s]+(?:the message|the procedure|the process))',
        ],
        'EVENT': [
            r'(?:upon|when|after|if)\s+(?:receiving|detecting|observing)\s+([A-Za-z\s]+)',
            r'(?:in case of|during|while)\s+([A-Za-z\s]+)',
            r'(?:timer\s+)?T\d+\s+(?:expiry|expires?|timeout)',
        ],
        'PARAMETER': [
            r'(?:parameter|value|field)\s+([A-Za-z0-9_]+)\s+(?:is|shall be|must be)',
            r'(?:sets?|configures?)\s+(?:the\s+)?([A-Za-z0-9_]+)\s+(?:to|as|with)',
            r'(?:mandatory|optional)\s+parameter\s+([A-Za-z0-9_]+)',
            r'IE\s+(?:type|value)\s+([A-Za-z0-9_]+)',
        ],
        'FLOW': [
            r'(?:step\s+\d+|next|then|subsequently)\s+([A-Za-z\s]+)',
            r'(?:follows|is followed by)\s+([A-Za-z\s]+)',
            r'(?:before|after)\s+([A-Za-z\s]+)',
        ],
        'CONDITIONAL': [
            r'(?:if|when|unless|provided that)\s+([^,\.]+)',
            r'(?:in case|in the event)\s+(?:that|of|when|if)\s+([^,\.]+)',
            r'(?:depending on|based on)\s+([^,\.]+)',
        ],
        'METADATA': [
            r'(?:specified in|defined in|according to)\s+(?:3GPP\s+)?TS\s+(\d+\.\d+)',
            r'(?:clause|section|chapter)\s+(\d+\.\d+\.\d+(?:\.\d+)?)',
            r'(?:Release|Rel\.|R)\s*(\d+)',
        ],
        'PROCEDURE': [
            r'\b(?:Initial|Mobility|Periodic|Emergency)\s+Registration\s+Procedure\b',
            r'\b(?:UE|Network)-initiated\s+De-registration\s+Procedure\b',
            r'\b(?:Service\s+Request|PDU\s+Session\s+Establishment)\s+Procedure\b',
            r'\b(?:Authentication|Security Mode Control|Identity)\s+Procedure\b',
        ],
        'MESSAGE': [
            r'\b(?:Authentication|Identity|Security Mode)\s+(?:Request|Response|Command|Result|Complete)\b',
            r'\b(?:Registration|Deregistration)\s+(?:Request|Accept|Reject|Complete)\b',
            r'\b(?:Service|Configuration|Status)\s+(?:Request|Accept|Reject|Notification)\b',
        ],
        'STEP': [
            # Numbered steps
            r'(?:Step|step)\s+(\d+)[:.]\s*([^.!?\n]+)',
            r'(?:^|\n)\s*(\d+)[).]\s*([^.!?\n]+)',
            # Sequential steps
            r'(?:First|Second|Third|Fourth|Fifth)\s*[,.]\s*([^.!?\n]+)',
            # Action steps
            r'(?:shall|must|will)\s+(?:then|subsequently|afterwards)\s+([^.!?\n]+)',
            # Sub-procedure steps
            r'(?:consists of|includes|contains)\s+(?:the following|these)\s+steps?:\s*([^.!?\n]+)',
            r'(?:sub-procedure|sub procedure)\s+steps?:\s*([^.!?\n]+)'
        ],
        'STEP_SEQUENCE': [
            r'(?:in sequence|in order|sequentially|one after another)',
            r'(?:following steps?|sequence of steps|step-by-step)',
            r'(?:step\s+\d+\s+(?:is followed by|precedes)\s+step\s+\d+)',
        ],
    }
    
    # Extract entities with their context
    for entity_type, type_patterns in patterns.items():
        for pattern in type_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Get the full match and any captured groups
                full_match = match.group(0)
                captured = match.groups()[0] if match.groups() else full_match
                
                # Get surrounding context (sentence)
                start_pos = max(0, match.start() - 100)
                end_pos = min(len(text), match.end() + 100)
                context = text[start_pos:end_pos].strip()
                
                # Create metadata
                metadata = {
                    'context': context,
                    'position': match.start(),
                    'raw_match': full_match
                }
                
                # Add to entities list
                entities.append((captured.strip(), entity_type, metadata))
    
    return list(set((e[0], e[1]) for e in entities))  # Remove duplicates

def extract_relationships(text: str, entities: List[Tuple[str, str]]) -> List[Tuple[str, str, str, Dict]]:
    """Finds relationships between core NAS components"""
    relationships = []
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    # Define relationship patterns
    patterns = {
        # State transitions
        'TRANSITIONS_TO': r'(?P<subject>\w+)\s+(?:transitions?|changes?|moves?)\s+to\s+(?P<object>\w+)',
        'TRIGGERS_STATE': r'(?P<subject>\w+)\s+(?:causes?|triggers?)\s+(?:transition|change)\s+to\s+(?P<object>\w+)',
        
        # Action relationships
        'PERFORMS': r'(?P<subject>\w+)\s+performs?\s+(?P<object>\w+)',
        'INITIATES': r'(?P<subject>\w+)\s+initiates?\s+(?P<object>\w+)',
        'EXECUTES': r'(?P<subject>\w+)\s+executes?\s+(?P<object>\w+)',
        
        # Event triggers
        'TRIGGERS': r'(?P<subject>\w+)\s+triggers?\s+(?P<object>\w+)',
        'CAUSES': r'(?P<subject>\w+)\s+causes?\s+(?P<object>\w+)',
        'LEADS_TO': r'(?P<subject>\w+)\s+leads?\s+to\s+(?P<object>\w+)',
        
        # Parameter usage
        'HAS_PARAMETER': r'(?P<subject>\w+)\s+(?:has|contains|includes)\s+parameter\s+(?P<object>\w+)',
        'SETS_PARAMETER': r'(?P<subject>\w+)\s+sets?\s+(?P<object>\w+)',
        'REQUIRES_PARAMETER': r'(?P<subject>\w+)\s+requires?\s+(?P<object>\w+)',
        
        # Flow relationships
        'FOLLOWED_BY': r'(?P<subject>\w+)\s+(?:is followed by|follows)\s+(?P<object>\w+)',
        'PRECEDES': r'(?P<subject>\w+)\s+precedes?\s+(?P<object>\w+)',
        'INCLUDES_STEP': r'(?P<subject>\w+)\s+includes?\s+step\s+(?P<object>\w+)',
        
        # Conditional relationships
        'DEPENDS_ON': r'(?P<subject>\w+)\s+depends?\s+on\s+(?P<object>\w+)',
        'CONDITIONAL_ON': r'(?P<subject>\w+)\s+(?:if|when)\s+(?P<object>\w+)',
        'REQUIRES': r'(?P<subject>\w+)\s+requires?\s+(?P<object>\w+)',
        
        # Metadata relationships
        'DEFINED_IN': r'(?P<subject>\w+)\s+(?:is defined in|is specified in)\s+(?P<object>\w+)',
        'REFERS_TO': r'(?P<subject>\w+)\s+refers?\s+to\s+(?P<object>\w+)',
        'SPECIFIED_IN': r'(?P<subject>\w+)\s+(?:is specified in|according to)\s+(?P<object>\w+)'
    }

    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check each entity pair in the sentence
        for i, (entity1, type1) in enumerate(entities):
            for entity2, type2 in entities[i+1:]:
                if entity1.lower() in sentence_lower and entity2.lower() in sentence_lower:
                    # Try to find specific relationships based on entity types
                    relationship_found = False
                    
                    # Type-specific relationships
                    if type1 == 'STATE' and type2 == 'STATE':
                        if re.search(rf'{entity1}\s+(?:transitions?|changes?)\s+to\s+{entity2}', sentence, re.IGNORECASE):
                            relationships.append((entity1, entity2, 'TRANSITIONS_TO', {'context': sentence}))
                            relationship_found = True
                    
                    elif type1 == 'ACTION' and type2 == 'EVENT':
                        if re.search(rf'{entity1}\s+(?:triggers?|causes?)\s+{entity2}', sentence, re.IGNORECASE):
                            relationships.append((entity1, entity2, 'TRIGGERS', {'context': sentence}))
                            relationship_found = True
                    
                    elif type1 == 'PROCEDURE' and type2 == 'PARAMETER':
                        if re.search(rf'{entity1}\s+(?:has|requires?)\s+parameter\s+{entity2}', sentence, re.IGNORECASE):
                            relationships.append((entity1, entity2, 'HAS_PARAMETER', {'context': sentence}))
                            relationship_found = True
                    
                    # Check generic patterns if no specific relationship found
                    if not relationship_found:
                        for rel_type, pattern in patterns.items():
                            match = re.search(pattern, sentence_lower)
                            if match:
                                subject = match.group('subject')
                                obj = match.group('object')
                                if (subject in entity1.lower() and obj in entity2.lower()) or \
                                   (subject in entity2.lower() and obj in entity1.lower()):
                                    relationships.append((entity1, entity2, rel_type, {'context': sentence}))
                                    break

    return relationships

def extract_procedure_steps(text: str, procedure_name: str) -> List[Dict]:
    """Extract steps from procedure text with their sequence and context"""
    steps = []
    step_number = 0
    
    # Patterns for step extraction
    step_patterns = [
        # Numbered steps
        r'(?:Step|step)\s+(\d+)[:.]\s*([^.!?\n]+)',
        r'(?:^|\n)\s*(\d+)[).]\s*([^.!?\n]+)',
        # Sequential steps
        r'(?:First|Second|Third|Fourth|Fifth)\s*[,.]\s*([^.!?\n]+)',
        # Action steps
        r'(?:shall|must|will)\s+(?:then|subsequently|afterwards)\s+([^.!?\n]+)',
        # Sub-procedure steps
        r'(?:consists of|includes|contains)\s+(?:the following|these)\s+steps?:\s*([^.!?\n]+)'
    ]
    
    for pattern in step_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            step_number += 1
            
            # Extract step content based on pattern type
            if len(match.groups()) > 1:  # Numbered step
                step_num = int(match.group(1))
                step_content = match.group(2)
            else:  # Other step types
                step_num = step_number
                step_content = match.group(1)
            
            # Get context around the step
            start_pos = max(0, match.start() - 100)
            end_pos = min(len(text), match.end() + 100)
            context = text[start_pos:end_pos].strip()
            
            # Create step entity
            step = {
                'name': f"{procedure_name}_Step_{step_num}",
                'content': step_content.strip(),
                'sequence_number': step_num,
                'procedure_id': procedure_name,
                'type': 'STEP',
                'context': context,
                'position': match.start()
            }
            
            steps.append(step)
    
    # Sort steps by sequence number
    return sorted(steps, key=lambda x: x['sequence_number'])

def store_procedure_steps(graph: KnowledgeGraph, steps: List[Dict], procedure_name: str):
    """Store procedure steps in Neo4j"""
    for step in steps:
        # Create step entity
        graph.create_entity(
            step['name'],
            'STEP',
            {
                'content': step['content'],
                'sequence_number': step['sequence_number'],
                'procedure_id': step['procedure_id'],
                'context': step['context']
            }
        )
        
        # Connect step to procedure
        graph.create_relationship(
            step['name'],
            procedure_name,
            'PART_OF',
            {'sequence': step['sequence_number']}
        )
        
        # If not the last step, connect to next step
        if step['sequence_number'] < len(steps):
            next_step = next(s for s in steps if s['sequence_number'] == step['sequence_number'] + 1)
            if next_step:
                graph.create_relationship(
                    step['name'],
                    next_step['name'],
                    'FOLLOWED_BY',
                    {'sequence_order': step['sequence_number']}
                )

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
        extractor = ProcedureExtractor()
        
        for doc in documents:
            text = doc["text"]
            
            # Extract and store LTE Attach procedure
            lte_flow = extractor.extract_procedure(text, "LTE_ATTACH")
            if lte_flow:
                graph.store_procedure_flow(lte_flow)
            
            # Extract and store 5G Registration procedure
            reg_flow = extractor.extract_procedure(text, "REGISTRATION")
            if reg_flow:
                graph.store_procedure_flow(reg_flow)
            
            # Store other entities and relationships
            for entity_text, entity_type, metadata in doc["entities"]:
                graph.create_entity(entity_text, entity_type)

            for entity1, entity2, relation, properties in doc["relationships"]:
                graph.create_relationship(entity1, entity2, relation, properties)
        
        # Create implicit relationships
        print("🔄 Creating implicit relationships...")
        graph.create_implicit_relationships()
        
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

        print(" Storing entities & relationships in Neo4j...")
        store_in_neo4j(documents)
        print("✅ Data successfully stored in Neo4j!")
