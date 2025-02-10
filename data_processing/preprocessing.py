# Convert PDFs to text (using PyMuPDF, pdfplumber, or pdfminer)
# Chunk the documents into smaller parts (e.g., per section or paragraph)
# Store document embeddings in a Vector Database for fast retrieval

import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

def save_text_chunks(text, chunk_size=500):
    """Splits text into smaller chunks for retrieval"""
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# test the function
pdf_file = os.path.join(os.path.dirname(__file__), "..", "data", "TS 24.234.pdf")
if os.path.exists(pdf_file):
    raw_text = extract_text_from_pdf(pdf_file)
else:
    print(f"PDF file not found: {pdf_file}")
