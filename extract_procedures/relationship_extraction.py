# Advanced Relationship Extraction using NLP Tools
import spacy
from transformers import pipeline
from entity_recognition import EntityRecognizer
from typing import List, Dict
import networkx as nx

class RelationshipExtractor:
    def __init__(self, spec_name: str = "TS_23_501"):
        """Initialize NLP tools"""
        # Load spaCy with custom pipeline
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load Hugging Face pipelines
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Get entities and sections
        self.entity_recognizer = EntityRecognizer(spec_name)
        self.sections = self.entity_recognizer.sections  # Get sections directly
        self.entities = self.entity_recognizer.extract_entities()
        
        # Initialize graph
        self.graph = nx.DiGraph()
        
        # Define relationship types
        self.relationship_types = [
            "authentication",  # Authentication procedure
            "session_management",  # Session establishment/management
            "handover",  # Handover procedure
            "location_management",  # Location update procedures
            "attach",  # Attach procedure
            "detach",  # Detach procedure
            "context_management",  # Context setup and release
            "security_context",  # Security context setup
            "message_exchange",  # Message exchange between entities
            "sends",
            "receives",
            "requires",
            "causes"
        ]

    def analyze_dependencies(self, text: str) -> List[Dict]:
        """Analyze syntactic dependencies in text"""
        doc = self.nlp(text)
        dependencies = []
        
        for token in doc:
            if token.dep_ in ['ROOT', 'xcomp', 'advcl']:
                # Find subject and object
                subject = [w for w in token.lefts if w.dep_ in ['nsubj', 'nsubjpass']]
                obj = [w for w in token.rights if w.dep_ in ['dobj', 'pobj']]
                
                if subject and obj:
                    dependencies.append({
                        'subject': subject[0].text,
                        'action': token.text,
                        'object': obj[0].text,
                        'type': token.dep_
                    })
        
        return dependencies

    def classify_relationship(self, text: str) -> str:
        """Classify relationship type using zero-shot classification"""
        result = self.classifier(
            text,
            candidate_labels=self.relationship_types,
            multi_label=False
        )
        return result['labels'][0]

    def extract_state_transitions(self) -> List[Dict]:
        """Extract state transitions and their triggers"""
        transitions = []
        
        for section_name, content in self.sections.items():
            doc = self.nlp(content)
            
            for sent in doc.sents:
                if any(word in sent.text.lower() for word in ['state', 'transition', 'changes']):
                    deps = self.analyze_dependencies(sent.text)
                    
                    for dep in deps:
                        transitions.append({
                            'from_state': dep['subject'],
                            'to_state': dep['object'],
                            'trigger': dep['action'],
                            'procedure': section_name
                        })
        
        return transitions

    def extract_message_flows(self) -> List[Dict]:
        """Extract message flows between components"""
        messages = []
        
        for section_name, content in self.sections.items():
            doc = self.nlp(content)
            
            for sent in doc.sents:
                if any(word in sent.text.lower() for word in ['sends', 'receives', 'message']):
                    deps = self.analyze_dependencies(sent.text)
                    
                    for dep in deps:
                        messages.append({
                            'sender': dep['subject'],
                            'receiver': dep['object'],
                            'message': dep['action'],
                            'procedure': section_name
                        })
        
        return messages

    def build_relationship_graph(self):
        """Build comprehensive relationship graph"""
        # Add state transitions
        transitions = self.extract_state_transitions()
        for trans in transitions:
            self.graph.add_edge(
                trans['from_state'],
                trans['to_state'],
                type='state_transition',
                trigger=trans['trigger'],
                procedure=trans['procedure']
            )
        
        # Add message flows
        messages = self.extract_message_flows()
        for msg in messages:
            self.graph.add_edge(
                msg['sender'],
                msg['receiver'],
                type='message_flow',
                message=msg['message'],
                procedure=msg['procedure']
            )
        
        # Add procedure dependencies
        for section_name, content in self.sections.items():
            doc = self.nlp(content)
            
            for sent in doc.sents:
                rel_type = self.classify_relationship(sent.text)
                deps = self.analyze_dependencies(sent.text)
                
                for dep in deps:
                    self.graph.add_edge(
                        dep['subject'],
                        dep['object'],
                        type=rel_type,
                        action=dep['action']
                    )

    def get_relationship_summary(self) -> Dict:
        """Get summary of all relationships"""
        self.build_relationship_graph()
        
        summary = {
            'state_transitions': [],
            'message_flows': [],
            'procedure_dependencies': []
        }
        
        for u, v, data in self.graph.edges(data=True):
            rel_type = data.get('type', '')
            
            if rel_type == 'state_transition':
                summary['state_transitions'].append({
                    'from': u,
                    'to': v,
                    'trigger': data.get('trigger', ''),
                    'procedure': data.get('procedure', '')
                })
            elif rel_type == 'message_flow':
                summary['message_flows'].append({
                    'from': u,
                    'to': v,
                    'message': data.get('message', ''),
                    'procedure': data.get('procedure', '')
                })
            else:
                summary['procedure_dependencies'].append({
                    'from': u,
                    'to': v,
                    'type': rel_type,
                    'action': data.get('action', '')
                })
        
        return summary

def main():
    extractor = RelationshipExtractor()
    summary = extractor.get_relationship_summary()
    
    print("\nState Transitions:")
    for trans in summary['state_transitions'][:3]:
        print(f"From {trans['from']} to {trans['to']} triggered by {trans['trigger']}")
    
    print("\nMessage Flows:")
    for msg in summary['message_flows'][:3]:
        print(f"From {msg['from']} to {msg['to']}: {msg['message']}")
    
    print("\nProcedure Dependencies:")
    for dep in summary['procedure_dependencies'][:3]:
        print(f"{dep['from']} {dep['type']} {dep['to']} via {dep['action']}")

if __name__ == "__main__":
    main()
