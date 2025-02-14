import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text from 3GPP documents."""
        # Remove special characters and normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract sections from 3GPP document text."""
        sections = {}
        
        # Pattern for 3GPP section headers
        section_pattern = r'(\d+\.[\d\.]*)\s+([^\n]+?)(?=\n|\d+\.[\d\.]*|$)'
        
        matches = re.finditer(section_pattern, text)
        for match in matches:
            section_num = match.group(1)
            section_title = match.group(2).strip()
            
            # Find the content until the next section
            start_pos = match.end()
            next_match = re.search(section_pattern, text[start_pos:])
            if next_match:
                content = text[start_pos:start_pos + next_match.start()]
            else:
                content = text[start_pos:]
                
            sections[section_num] = {
                'title': section_title,
                'content': content.strip()
            }
            
        logger.info(f"Extracted {len(sections)} sections from document")
        return sections

    @staticmethod
    def validate_entities(entities: List[Dict]) -> List[Dict]:
        """Validate extracted entities before storing in Neo4j."""
        valid_entities = []
        for entity in entities:
            if all(key in entity for key in ['id', 'type', 'name']):
                valid_entities.append(entity)
            else:
                logger.warning(f"Invalid entity structure: {entity}")
        return valid_entities 