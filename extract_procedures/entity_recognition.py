import spacy
from preprocess import TextPreprocessor
from typing import List, Dict
import re

class EntityRecognizer:
    def __init__(self, spec_name: str = "TS_23_501"):
        """Initialize entity recognizer for NAS related procedures to NR"""
        self.nlp = spacy.load("en_core_web_sm")
        self.preprocessor = TextPreprocessor(spec_name)
        self.sections = self.extract_sections()  # Get sections directly

    def extract_sections(self) -> Dict[str, str]:
        """Extract main sections from the document"""
        sections = {}
        current_section = ""
        current_text = []
        
        for line in self.preprocessor.raw_text.split('\n'):
            # Look for section headers with NR/5G related terms
            section_match = re.search(r'(nr|5g|session|ran|amf|smf|registration|authentication)', line, re.IGNORECASE)

            if section_match:
                # Save previous section if exists
                if current_section and current_text:
                    sections[current_section] = ' '.join(current_text)
                current_section = section_match.group(0).upper()
                current_text = []
            elif current_section:  # Only add text if we're in a section
                if line.strip():  # Only add non-empty lines
                    current_text.append(line.strip())

        # Add the last section
        if current_section and current_text:
            sections[current_section] = ' '.join(current_text)
            
        return sections

    def extract_entities(self) -> Dict[str, List[str]]:
        """Extract entities from sections"""
        entities = {
            'STATES': [],
            'MESSAGES': [],
            'COMPONENTS': []
        }

        for section_name, content in self.sections.items():
            doc = self.nlp(content)
            
            # Extract components (network entities)
            for ent in doc.ents:
                if ent.label_ == 'ORG' or any(term in ent.text.lower() for term in ['amf', 'smf', 'upf', 'ran']):
                    entities['COMPONENTS'].append(ent.text)
            
            # Extract states and messages
            for sent in doc.sents:
                # States
                if 'state' in sent.text.lower():
                    entities['STATES'].append(sent.text.strip())
                
                # Messages
                if any(term in sent.text.lower() for term in [
                    'attach accept', 'attach request', 
                    'authentication request', 'authentication response',
                    'session establishment request', 'session establishment response'
                ]):
                    entities['MESSAGES'].append(sent.text.strip())

        # Remove duplicates and sort
        for key in entities:
            entities[key] = sorted(set(entities[key]))
        
        return entities

def main():
    recognizer = EntityRecognizer()
    
    # Print sections
    print("\nExtracted Sections:")
    for name, content in recognizer.sections.items():
        print(f"\nSection: {name}")
        print(f"Length: {len(content)} characters")
    
    # Print entities
    entities = recognizer.extract_entities()
    print("\nExtracted Entities:")
    for entity_type, items in entities.items():
        print(f"\n{entity_type}:")
        for item in items[:3]:  # Show first 3 of each type
            print(f"- {item}")

if __name__ == "__main__":
    main()
