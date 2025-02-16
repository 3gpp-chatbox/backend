import spacy
import re
from typing import Dict, List, Tuple
from neo4j import GraphDatabase
import json
import google.generativeai as genai

class GraphExtractor:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.max_length = 2000000
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


    def __del__(self):
        if hasattr(self, 'driver') and self.driver is not None:
            self.driver.close()


    def preprocess_doc(self, text: str) -> str:
        """Preprocess and clean text, excluding unwanted sections."""
        exclude_sections = ["Contents", "Annex", "References"]

        lines = text.split("\n")
        cleaned_lines = []
        skip_section = False

        for line in lines:
            if any(section in line for section in exclude_sections):
                skip_section = True
                continue

            if skip_section and line.strip() == "":
                skip_section = False
                continue

            if not re.match(r"^\s*(\d+\.\d+|\(C\) 3GPP|3GPP TS 24\.501|Page \d+)", line) and not skip_section:
                cleaned_lines.append(line)

        cleaned_text = "\n".join(cleaned_lines)
        cleaned_text = re.sub(r"\n{2,}", "\n\n", cleaned_text)

        return cleaned_text.strip()

    def chunk_text(self, text: str, chunk_size: int = 10000) -> List[str]:
        """Chunk text into manageable sections."""
        tokens = text.split()
        chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
        return [" ".join(chunk) for chunk in chunks]

    def identify_procedure(self, text: str) -> str:
        """
        Identify the NAS procedure type from the sentence text.
        """
        procedures = {
            'Registration': ['registration', 'attach', 'accept', 'complete', 'update', 'reject'],
            'Deregistration': ['deregistration', 'detach', 'ue-initiated', 'network-initiated'],
            'Authentication': ['authentication', 'auth', 'auth request', 'auth response', 'auth reject'],
            # 'Security': ['security', 'integrity', 'ciphering', 'security mode', 'security context'],
            # 'Service': ['service request', 'service accept', 'service reject'],
            # 'Identity': ['identity', 'identification', 'guti', '5g-s-tmsi'],
            # 'Location': ['location', 'location request', 'location update', 'location report'],
            # 'Configuration': ['configuration', 'configuration update', 'configuration request', 'configuration reject'],
            # 'PDU Session': ['pdu session', 'pdu session request', 'pdu session update', 'pdu session release'],
            # 'SM': ['sm request', 'ue initiated', 'network initiated', 'pdu session']
        }

        text_lower = text.lower()
        for proc_type, keywords in procedures.items():
            if any(keyword in text_lower for keyword in keywords):
                return proc_type
        return 'Other'
    
    def extract_nas_info_from_chunk(self, chunk_text: str) -> Tuple[Dict[str, set], List[Tuple[str, str, str]]]:
        """Extracts NAS info from a text chunk using improved regex and NLP."""
        doc = self.nlp(chunk_text)
        nodes = {"states": set(), "messages": set(), "procedures": set(), "entities": set()}
        edges = []

        for sent in doc.sents:
            procedure = self.identify_procedure(sent.text)
            if procedure != 'Other':
                nodes["procedures"].add(procedure)

                # 1. Extract Entities (Improved):
                for ent in sent.ents:
                    if ent.label_ in ["ORG", "GPE", "PERSON", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW"]: # Add more if needed
                        nodes["entities"].add(ent.text)
                        edges.append((procedure, "HAS_ENTITY", ent.text))

                # 2. Extract Messages (Improved Regex and NLP - Using Dependency Parsing):
                for token in sent:
                    if token.dep_ == "dobj" and token.head.text.lower() == "sends":  # Direct object of "sends"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "SENDS", message)) # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "receives":  # Direct object of "receives"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "RECEIVES", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "issues":  # Direct object of "issues"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "ISSUES", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "requests":  # Direct object of "requests"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "REQUESTS", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "updates":  # Direct object of "updates"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "UPDATES", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "generates":  # Direct object of "generates"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "GENERATES", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "indicates":  # Direct object of "indicates"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "INDICATES", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "forwards":  # Direct object of "forwards"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "FORWARDS", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "sends":  # Direct object of "sends"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "SENDS", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "triggers":  # Direct object of "triggers"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "TRIGGERS", message))  # More specific edge

                    elif token.dep_ == "dobj" and token.head.text.lower() == "initiates":  # Direct object of "initiates"
                        message = token.text
                        nodes["messages"].add(message)
                        edges.append((procedure, "INITIATES", message))  # More specific edge


                # 3. Extract States (Improved Regex and NLP - Using Dependency Parsing):
                for token in sent:
                    if token.dep_ == "prep" and token.head.text.lower() == "in":  # Prepositional phrase "in"
                        state = token.text
                        nodes["states"].add(state)
                        edges.append((procedure, "OCCURS_IN", state))  # More specific edge

                    elif token.dep_ == "prep" and token.head.text.lower() == "to":  # Prepositional phrase "to"
                        state = token.text
                        nodes["states"].add(state)
                        edges.append((procedure, "CHANGES_TO", state))  # More specific edge

                    elif token.dep_ == "prep" and token.head.text.lower() == "from":  # Prepositional phrase "from"
                        state = token.text
                        nodes["states"].add(state)
                        edges.append((procedure, "CHANGES_FROM", state))  # More specific edge

                    elif token.dep_ == "prep" and token.head.text.lower() == "at":  # Prepositional phrase "at"
                        state = token.text
                        nodes["states"].add(state)
                        edges.append((procedure, "IS_AT", state))  # More specific edge

                    elif token.dep_ == "prep" and token.head.text.lower() == "during":  # Prepositional phrase "during"
                        state = token.text
                        nodes["states"].add(state)
                        edges.append((procedure, "DURING", state))  # More specific edge

                # 4. Extract Keywords related to Procedures(NLP):
                keywords = [token.text for token in sent if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop] # Extract nouns and proper nouns
                for keyword in keywords:
                    edges.append((procedure, "RELATED_TO", keyword)) # Add a RELATED_TO edge

        return nodes, edges

    def create_graph_from_nas_info(self, nas_info: Dict):
            """Creates the graph in Neo4j from the NAS information."""
            with self.driver.session() as session:
                for procedure, data in nas_info.get("Procedures", {}).items():
                    session.run(f"MERGE (p:Procedure {{name: $procedure}})", procedure=procedure)

                    for message in data.get("Messages", []):
                        session.run(f"MERGE (m:Message {{name: $message}})", message=message)
                        session.run(f"MATCH (p:Procedure {{name: $procedure}}), (m:Message {{name: $message}}) CREATE (p)-[:USES]->(m)", procedure=procedure, message=message)

                    for state in data.get("States", []):
                        session.run(f"MERGE (s:State {{name: $state}})", state=state)
                        session.run(f"MATCH (p:Procedure {{name: $procedure}}), (s:State {{name: $state}}) CREATE (p)-[:RESULTS_IN]->(s)", procedure=procedure, state=state)

                    # Handle Entities (if present in your nas_info structure):
                    for entity in data.get("Entities", []):  # Assumes "Entities" key exists
                        session.run(f"MERGE (e:Entity {{name: $entity}})", entity=entity)
                        session.run(f"MATCH (p:Procedure {{name: $procedure}}), (e:Entity {{name: $entity}}) CREATE (p)-[:HAS_ENTITY]->(e)", procedure=procedure, entity=entity)

                    # Handle other relationships if needed (e.g., RELATED_TO, etc.):
                    # Example for RELATED_TO (adapt as needed):
                    for related_to in data.get("RelatedTo", []):  # Assumes "RelatedTo" key exists
                        session.run(f"MERGE (r:Keyword {{name: $related_to}})", related_to=related_to)
                        session.run(f"MATCH (p:Procedure {{name: $procedure}}), (r:Keyword {{name: $related_to}}) CREATE (p)-[:RELATED_TO]->(r)", procedure=procedure, related_to=related_to)


                    # Example for more specific message relationships (e.g., SENDS, RECEIVES):
                    for message_data in data.get("MessagesData", []): # Assumes "MessagesData" key exists and contains dictionaries with "name" and "type" keys
                        message = message_data.get("name")
                        message_type = message_data.get("type") # e.g., "SENDS", "RECEIVES"
                        if message and message_type: # Make sure both are present
                            session.run(f"MERGE (m:Message {{name: $message}})", message=message)
                            session.run(f"MATCH (p:Procedure {{name: $procedure}}), (m:Message {{name: $message}}) CREATE (p)-[:{message_type}]->(m)", procedure=procedure, message=message, message_type=message_type)



    def process_document(self, text: str):
        """Process document and extract NAS information with detailed logging."""
        print("[INFO] Starting document processing...")
        cleaned_text = self.preprocess_doc(text)
        print(f"[INFO] Text preprocessed. Length: {len(cleaned_text)} characters")

        chunks = self.chunk_text(cleaned_text)
        print(f"[INFO] Text split into {len(chunks)} chunks for processing")

        for i, chunk_text in enumerate(chunks, start=1):
            print(f"[INFO] Processing chunk {i}/{len(chunks)}. Chunk length: {len(chunk_text.split())} words")

            # Extract NAS information from each chunk
            nodes, edges = self.extract_nas_info_from_chunk(chunk_text)
            
            # Convert sets to lists for JSON serialization
            serializable_nodes = {
                k: list(v) for k, v in nodes.items()
            }
            
            print(f"[SUCCESS] NAS information extracted from chunk {i}:")
            print(json.dumps({"nodes": serializable_nodes, "edges": edges}, indent=2))

            # Create Neo4j graph
            nas_info = {
                "Procedures": {
                    proc: {
                        "Messages": list(nodes["messages"]),
                        "States": list(nodes["states"]),
                        "Entities": list(nodes["entities"])
                    } for proc in nodes["procedures"]
                }
            }
            
            self.create_graph_from_nas_info(nas_info)
            print(f"[INFO] Graph created for chunk {i}.")

        print("[INFO] Document processing completed. Graph created in Neo4j.")