import fitz  # PyMuPDF
import re
import os

def remove_toc(pdf_path, output_path):
    """Remove TOC pages automatically by detecting common TOC patterns."""
    document = fitz.open(pdf_path)
    pages_to_remove = []

    # Scan for pages that might be TOC pages
    for page_num in range(document.page_count):
        page_text = document[page_num].get_text("text")
        
        # Check for keywords or patterns commonly found in TOC
        if re.search(r'\bTable of Contents\b', page_text, re.IGNORECASE) or \
           re.search(r'\.{5,}', page_text) or \
           len(page_text.split("\n")) < 10:  # Heuristic: TOC pages tend to have fewer lines
            pages_to_remove.append(page_num)

    # Create a new PDF without the TOC pages
    new_document = fitz.open()
    
    for page_num in range(document.page_count):
        if page_num not in pages_to_remove:
            new_document.insert_pdf(document, from_page=page_num, to_page=page_num)
    
    # Save the cleaned PDF (without TOC pages)
    new_document.save(output_path)
    new_document.close()
    document.close()

def extract_and_clean_text(pdf_path):
    """Extract and clean text from a PDF file, removing headers, footers, page numbers, and unwanted section headers."""
    doc = fitz.open(pdf_path)
    text = ""

    for page_num, page in enumerate(doc):
        page_text = page.get_text("text")
        
        # Remove headers and footers (assuming they are consistent)
        lines = page_text.split("\n")
        if len(lines) > 2:
            lines = lines[1:-1]  # Remove first and last line (header/footer)
        page_text = " ".join(lines)

        # Remove page numbers (assuming they are standalone numbers)
        page_text = re.sub(r'\b\d+\b', '', page_text)

        # Remove headings followed by dots and any content after them
        page_text = re.sub(r'^[A-Za-z\s]+[\.\.\.]+', '', page_text)  # Match headings with dots
        page_text = re.sub(r'\s*\n{2,}', '\n', page_text)  # Clean extra blank lines

        text += page_text + "\n"
    
    # Cleaning text
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    
    return text

# Define the path to the "data" folder and the PDF file
data_folder = "data"
pdf_filename = "TS 24.501.pdf"  # Replace with your actual PDF file name
pdf_path = os.path.join(data_folder, pdf_filename)

# Define the path to save the cleaned PDF without TOC
output_pdf_path = os.path.join(data_folder, "output_cleaned.pdf")

# Remove TOC pages from the PDF
remove_toc(pdf_path, output_pdf_path)

# Now, extract and clean the text from the cleaned PDF (without TOC pages)
if os.path.exists(output_pdf_path):
    # Extract and clean text from the cleaned PDF
    cleaned_text = extract_and_clean_text(output_pdf_path)

    # Display the cleaned text in the console (you can adjust how much text you want to show)
    print("Preprocessed Content (Cleaned Text):")
    print(cleaned_text[:1000])  # Display the first 1000 characters of the cleaned text to avoid overload

    # Optionally save to a text file
    with open("cleaned_text.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("\nText extraction and cleaning complete.")
else:
    print(f"Error: The file '{pdf_filename}' was not found in the 'data' folder.")
