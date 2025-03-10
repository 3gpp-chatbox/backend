import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
 # Load from environment variable
  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to extract procedural flow from the chunk of text using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
   you are a expert in 3gpp 5g and 4g procedures,below is the thunk text about registration procedure for initial registration from 3gpp 24.501,read them carefully first:

    {text}

     now, list all procedures from the following section and then extract the the first procedure information from the list and use below mapping to extract the information(below is an example):

1. **Initial UE State**: UE is powered on and not attached to any network
2. **Attach Request**: UE sends an Attach Request message to the MME
3. **Authentication**: MME initiates authentication procedures
4. **Security Mode Command**: MME sets up security parameters
5. **Attach Accept**: MME sends an Attach Accept message to the UE
6. **Attach Complete**: UE confirms with an Attach Complete message
7. **Final UE State**: UE is attached to the network and can access services)  ,

finally, make mermaid diagram format and description for the first procedure.

    Based on the above, analyze and extract the information from the given chunk.
    """

    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to retrieve document chunks from the database
def retrieve_chunks_from_db(start_id, end_id, db_path="path_to_your_db.sqlite"):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve chunks within the given ID range
    cursor.execute('''SELECT chunk_text FROM document_chunks WHERE chunk_id BETWEEN ? AND ?''', (start_id, end_id))

    # Fetch all matching chunks
    chunks = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Join the chunks together into one large text block
    full_text = "\n".join(chunk[0] for chunk in chunks)

    return full_text


# Function to save extracted procedural info as plain text
def save_procedural_info_to_txt(procedural_info, file_path):
    with open(file_path, "w") as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

# Main function to process the document section
def process_section(start_id, end_id, db_path="path_to_your_db.sqlite"):
    # Step 1: Retrieve the chunks for the desired section (e.g., 5.5.1.2 to 5.5.1.3)
    chunk_text = retrieve_chunks_from_db(start_id, end_id, db_path)

    # Step 2: Extract procedural flow from the retrieved chunks
    procedural_info = extract_procedural_info_from_text(chunk_text)

    return procedural_info

# Example usage: Processing section 5.5.1.2 to 5.5.1.3 (IDs 625 to 765 in your database)
start_chunk_id = 625  # Start chunk ID (example)
end_chunk_id = 765    # End chunk ID (example)
db_path = "path_to_your_db.sqlite"  # Path to your SQLite database

# Process the section
procedural_info = process_section(625, 765, 'document_chunks.db')

# Print the extracted procedural info
# print("Extracted Procedural Information:\n")
# print(procedural_info)

save_procedural_info_to_txt(procedural_info, "output3.txt")  # For plain text