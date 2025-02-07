import os
from typing import List, Dict
from pypdf import PdfReader

def read_pdfs_from_directory(directory: str) -> List[Dict[str, str]]:
    """
    Reads all PDFs from a directory and returns a list of document dictionaries.
    """
    documents = []
    
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} not found")

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                pdf_reader = PdfReader(file_path)
                text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

                if text.strip():
                    documents.append({
                        "text": text,
                        "metadata": {
                            "source": filename,
                            "file_path": file_path
                        }
                    })
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    return documents

if __name__ == "__main__":
    data_directory = "data"
    documents = read_pdfs_from_directory(data_directory)
    print(f"✅ Processed {len(documents)} documents")
