import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        if text:
            print("Text extracted successfully!")
        else:
            print("Warning: No text extracted from the PDF.")
        return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

def save_text_chunks(text, chunk_size=500):
    """Splits text into smaller chunks for retrieval"""
    if not text:
        print("No text available to chunk.")
        return []
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    print(f"Text split into {len(chunks)} chunks.")
    return chunks

# Test the function
pdf_file = os.path.join(os.path.dirname(__file__), ".", "data_store", "TS 24.234.pdf")
if os.path.exists(pdf_file):
    print(f"Processing file: {pdf_file}")
    raw_text = extract_text_from_pdf(pdf_file)
    if raw_text:
        chunks = save_text_chunks(raw_text)
        # Optionally print the first chunk to check
        if chunks:
            print(f"First chunk: {chunks[0][:100]}...")  # Display the first 100 characters of the first chunk
else:
    print(f"PDF file not found: {pdf_file}")
