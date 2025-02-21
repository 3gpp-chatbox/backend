import pdfplumber
import re
import logging

# Function to extract text from the PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
    return text

# Function to clean and preprocess the extracted text
def clean_text(text):
    """Cleans extracted text by removing noise and normalizing content."""
    try:
        # Handle potential encoding issues
        if not isinstance(text, str):
            text = str(text, errors='ignore')
        
        # Remove common PDF artifacts
        text = re.sub(r'\bPage\s+\d+\s+of\s+\d+\b', '', text)  # Remove "Page X of Y"
        text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with spaces
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = re.sub(r'\n\s*\n+', '\n\n', text)  # Normalize paragraph breaks
        
        # Remove very short lines (likely artifacts)
        lines = [line for line in text.split('\n') if len(line.strip()) > 5]
        text = '\n'.join(lines)
        
        return text.strip()
    except Exception as e:
        logging.warning(f"Error in clean_text: {str(e)}")
        return ""

# Function to extract and identify Mobility Management procedures
def parse_mm_procedures(text):
    mm_procedures = []

    # Example patterns to identify MM procedures
    registration_pattern = r"(Registration|REGISTERED|register)"
    handover_pattern = r"(Handover|handover)"
    update_pattern = r"(Periodic update|UPDATE)"
    deregistration_pattern = r"(Deregistration|DEREGISTERED|deregister)"

    # Checking for procedures in the text using regex
    if re.search(registration_pattern, text, re.IGNORECASE):
        mm_procedures.append("Registration Procedure")
    
    if re.search(handover_pattern, text, re.IGNORECASE):
        mm_procedures.append("Handover Procedure")
    
    if re.search(update_pattern, text, re.IGNORECASE):
        mm_procedures.append("Periodic Update Procedure")

    if re.search(deregistration_pattern, text, re.IGNORECASE):
        mm_procedures.append("Deregistration Procedure")
    
    return mm_procedures

# Function to extract relevant Mobility Management info
def extract_mm_data(pdf_path):
    # Step 1: Extract raw text from the PDF
    raw_text = extract_text_from_pdf(pdf_path)

    # Step 2: Clean the extracted text to remove unwanted noise
    cleaned_text = clean_text(raw_text)
    
    # Step 3: Parse the cleaned text to identify MM procedures
    mm_procedures = parse_mm_procedures(cleaned_text)

    # Return the cleaned text and identified procedures
    return cleaned_text, mm_procedures

# Path to your 3GPP PDF file
pdf_path = "data/TS 24.501.pdf"  # Adjust this path to your actual PDF file

# Extract MM data from the PDF
cleaned_text, mm_procedures = extract_mm_data(pdf_path)

# Output the results
print("Cleaned Text:")
print(cleaned_text[:1000])  # Print the first 1000 characters for preview
print("\nIdentified MM Procedures:")
print(mm_procedures)
