# Text Preprocessing and Cleaning
from raw_extracting import extract_text_from_docx
import re
from typing import List, Dict

class TextPreprocessor:
    def __init__(self, spec_name: str = "TS_23_501"):
        """Initialize preprocessor with raw text from document"""
        self.raw_text = extract_text_from_docx(spec_name)
        
    def clean_text(self) -> str:
        """Clean and normalize the raw text"""
        text = re.sub(r'\s+', ' ', self.raw_text)  # Remove extra whitespace
        text = re.sub(r'[^\w\s.,;:()"-]', '', text)  # Remove unwanted characters
        return text.strip()
    
    

def main():
    preprocessor = TextPreprocessor()
    
    # Clean text
    clean_text = preprocessor.clean_text()
    print("\nCleaned Text Sample:")
    print(clean_text[:200])
    

if __name__ == "__main__":
    main()
