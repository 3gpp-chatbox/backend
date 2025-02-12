import os
import logging
from typing import List, Dict
from pypdf import PdfReader
import re

# Set up logging
logging.basicConfig(filename="preprocessing.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_text(text: str) -> str:
    """Cleans extracted text by normalizing spaces and formatting."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()

def read_pdfs_from_directory(directory: str) -> List[Dict[str, str]]:
    """Reads all PDFs from a directory and returns a list of document dictionaries."""
    documents = []

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} not found")

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                pdf_reader = PdfReader(file_path)
                text = []
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(clean_text(page_text))

                text = "\n\n".join(text)  # Ensure proper paragraph breaks
                
                if text.strip():
                    documents.append({
                        "text": text,
                        "metadata": {
                            "source": filename,
                            "file_path": file_path
                        }
                    })
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")

    return documents

if __name__ == "__main__":
    data_directory = "data"
    documents = read_pdfs_from_directory(data_directory)
    print(f"✅ Processed {len(documents)} documents")
