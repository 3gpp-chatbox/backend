import sqlite3
import re
import os

from dotenv import load_dotenv
import google.generativeai as genai
import time
from google.api_core.exceptions import ResourceExhausted


# Configure API key
load_dotenv()
# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')
DB_NAME = 'section_content_0303.db'

# Step 1: Extract sections containing procedures or related content
def extract_sections_for_procedures():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT section_id, section_name FROM sections
        WHERE section_name LIKE '%procedure%' OR section_name LIKE '%method%' OR section_name LIKE '%registration%'
    ''')
    
    return cursor.fetchall()

# Step 2: Extract content for those sections
def extract_content_for_sections(sections_with_procedures):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    extracted_content = []

    for section_id, section_name in sections_with_procedures:
        cursor.execute('''
            SELECT content_chunk FROM content WHERE section_id = ?
        ''', (section_id,))
        
        content_chunks = cursor.fetchall()

        for chunk in content_chunks:
            content = chunk[0]
            extracted_content.append((section_id, section_name, content))

    conn.close()
    return extracted_content

# Step 3: Use regex and LLM to process and extract procedures
def extract_procedures(content_chunks):
    procedures = []
    retries = 5  # Number of retries in case of quota exhaustion
    backoff_time = 5  # Initial backoff time in seconds
    
    # Regex pattern for matching procedural steps
    procedure_pattern = re.compile(r'(Procedure|Step|Action|Method|Flow)[^:]*:(.*)', re.IGNORECASE)

    for section_id, section_name, content in content_chunks:
        matches = procedure_pattern.findall(content)

        for match in matches:
            procedure_title = match[0].strip()
            procedure_description = match[1].strip()

            # Use LLM for further verification or summarization if needed
            prompt = f"Is this a procedure or action step? \n\nTitle: {procedure_title} \nDescription: {procedure_description}"

            # Retry mechanism for the request
            for attempt in range(retries):
                try:
                    # Use 'generate_content' method to get the model's response
                    response = model.generate_content(prompt)

                    is_procedure = "yes" in response.text.lower()

                    if is_procedure:
                        procedures.append({
                            'section_id': section_id,
                            'section_name': section_name,
                            'procedure_title': procedure_title,
                            'procedure_description': procedure_description
                        })
                    break  # Exit the retry loop if successful
                
                except ResourceExhausted as e:
                    print(f"Quota exhausted: {e}. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff
                except Exception as e:
                    print(f"An error occurred: {e}.")
                    break  # Exit the retry loop on other errors

    return procedures

# Main flow: Extract and process procedures
if __name__ == '__main__':
    # Step 1: Extract sections related to procedures
    sections_for_procedures = extract_sections_for_procedures()

    # Step 2: Extract content for these sections
    content_chunks = extract_content_for_sections(sections_for_procedures)

    # Step 3: Extract and verify procedures using regex and LLM
    procedures = extract_procedures(content_chunks)

    # Print or save the extracted procedures
    with open('extracted_procedures.txt', 'w', encoding='utf-8') as f:
        for procedure in procedures:
            f.write(f"Section: {procedure['section_name']} (ID: {procedure['section_id']})\n")
            f.write(f"Procedure Title: {procedure['procedure_title']}\n")
            f.write(f"Description: {procedure['procedure_description']}\n\n")

    print("✅ Procedure extraction completed and saved to extracted_procedures.txt.")
