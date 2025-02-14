import spacy
import re
import sqlite3
import json
from typing import Dict, List, Tuple

class GraphExtractor:
    def __init__(self, db_path: str = "chunk_results.db"):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.max_length = 2000000  # Increase limit as needed
        
        # Global containers for aggregated results
        self.nas_nodes = {"states": set(), "messages": set(), "procedures": set(), "entities": set()}
        self.nas_edges = []
        
        # Option to store intermediate chunk results in a SQLite database
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database and create table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS chunk_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_text TEXT,
                nodes TEXT,  -- Stored as JSON
                edges TEXT   -- Stored as JSON
            )
        ''')
        conn.commit()
        conn.close()

    def _store_chunk_result(self, chunk_text: str, nodes: Dict[str, set], edges: List[Dict]):
        """Store the result of a single chunk in the database."""
        # Convert nodes (sets) to lists and then to JSON
        nodes_json = json.dumps({k: list(v) for k, v in nodes.items()})
        edges_json = json.dumps(edges)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO chunk_results (chunk_text, nodes, edges)
            VALUES (?, ?, ?)
        ''', (chunk_text, nodes_json, edges_json))
        conn.commit()
        conn.close()

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess and clean the text.
        This method is applied on smaller text chunks.
        """
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\s.,;:"()-]', '', text)
        return text

    def identify_procedure(self, text: str) -> str:
        """
        Identify the NAS procedure type from the sentence text.
        """
        procedures = {
            'Registration': ['registration', 'attach', 'accept', 'complete', 'update', 'reject'],
            'Deregistration': ['deregistration', 'detach', 'ue-initiated', 'network-initiated'],
            'Authentication': ['authentication', 'auth', 'auth request', 'auth response', 'auth reject'],
            'Security': ['security', 'integrity', 'ciphering', 'security mode', 'security context'],
            'Service': ['service request', 'service accept', 'service reject'],
            'Identity': ['identity', 'identification', 'guti', '5g-s-tmsi'],
            'Location': ['location', 'location request', 'location update', 'location report'],
            'Configuration': ['configuration', 'configuration update', 'configuration request', 'configuration reject'],
            'PDU Session': ['pdu session', 'pdu session request', 'pdu session update', 'pdu session release'],
            'SM': ['sm request', 'ue initiated', 'network initiated', 'pdu session']
        }

        text_lower = text.lower()
        for proc_type, keywords in procedures.items():
            if any(keyword in text_lower for keyword in keywords):
                return proc_type
        return 'Other'

    def process_text_in_chunks(self, text: str) -> Tuple[Dict[str, set], List[Dict]]:
        """
        Process the text in smaller chunks (e.g., paragraphs) to extract NAS nodes and edges.
        Instead of storing intermediate results in-memory, store each chunk in a database.
        """
        # Global containers for the final results
        global_nodes = {"states": set(), "messages": set(), "procedures": set(), "entities": set()}
        global_edges = []
        
        # Split the document into chunks (using paragraphs in this example)
        paragraphs = text.split('\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Preprocess and parse the chunk
            preprocessed = self.preprocess_text(para)
            if not preprocessed:
                continue
            doc = self.nlp(preprocessed)
            
            # Containers for this chunk's results
            chunk_nodes = {"states": set(), "messages": set(), "procedures": set(), "entities": set()}
            chunk_edges = []
            
            # Define NAS patterns and procedure keywords
            nas_patterns = {
                'states': r'(REGISTERED|DEREGISTERED|IDLE|CONNECTED|AUTHENTICATION|SERVICE_REQUEST)',
                'messages': r'(Registration Request|Registration Accept|Authentication Request|Security Mode Command|Identity Request)',
                'procedures': r'(Registration|Deregistration|Authentication|Security|Service Request|Identity|Location|Configuration|PDU Session|SM)',
                'entities': r'(AMF|UE|AUSF|SEAF|SMF|UPF|MME)'
            }

            procedure_keywords = [
                'REGISTRATION', 'DEREGISTRATION', 'AUTHENTICATION', 'SECURITY',
                'SERVICE REQUEST', 'IDENTITY', 'LOCATION', 'CONFIGURATION',
                'PDU SESSION', 'SM'
            ]
            
            # Process each sentence in the chunk
            for sent in doc.sents:
                # Regex-based extraction
                for node_type, pattern in nas_patterns.items():
                    for match in re.finditer(pattern, sent.text, re.IGNORECASE):
                        chunk_nodes[node_type].add(match.group(0))
                
                # NER-based extraction
                for ent in doc.ents:
                    if ent.label_ in {"ORG", "PERSON", "GPE"}:
                        chunk_nodes["entities"].add(ent.text)
                
                # Edge extraction for sentences mentioning a procedure
                if any(proc in sent.text.upper() for proc in procedure_keywords):
                    for token in sent:
                        if token.dep_ == "ROOT":
                            subj = next((w.text for w in token.lefts if w.dep_ in ['nsubj', 'nsubjpass']), None)
                            obj = next((w.text for w in token.rights if w.dep_ in ['dobj', 'pobj']), None)
                            if subj and obj:
                                chunk_edges.append({
                                    'source': subj,
                                    'target': obj,
                                    'relationship': token.text,
                                    'procedure': self.identify_procedure(sent.text)
                                })
            
            # Store this chunk's results in the database
            self._store_chunk_result(para, chunk_nodes, chunk_edges)
            
            # Merge chunk results into global results
            for key in global_nodes:
                global_nodes[key].update(chunk_nodes[key])
            global_edges.extend(chunk_edges)
        
        # Update global instance variables
        self.nas_nodes = global_nodes
        self.nas_edges = global_edges
        return global_nodes, global_edges

    def print_graph_summary(self):
        """Print summary of aggregated NAS graph elements."""
        print("\nNAS Graph Elements Summary:")
        for node_type, nodes in self.nas_nodes.items():
            print(f"\n{node_type.capitalize()} ({len(nodes)}):")
            print('\n'.join(f"- {node}" for node in nodes))
        
        print("\nEdges:")
        for edge in self.nas_edges:
            print(f"{edge['source']} --[{edge['relationship']}]--> {edge['target']} (Procedure: {edge['procedure']})")

# Example usage:
if __name__ == "__main__":
    extractor = GraphExtractor()
    sample_text = """
    The AMF sent a Registration Request to the UE. Upon receiving it, the UE replied with a Registration Accept.
    During the Authentication procedure, the Authentication Request was sent, followed by the Security Mode Command.
    """
    nodes, edges = extractor.process_text_in_chunks(sample_text)
    extractor.print_graph_summary()
