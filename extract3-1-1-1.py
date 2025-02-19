import sqlite3
import google.generativeai as genai

# Initialize Google Generative AI (Gemini)
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Load from environment variable

model = genai.GenerativeModel('gemini-1.5-flash')

# Function to extract procedural flow from the chunk of text using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
    below is the thunk text of a section, read them carefully first:

    {text}

 remember, all you analysis and extract should be based on the thunk text, and you should not make any assumptions. now, list all procedures from the  section and then focus one first procedure ,extract the the first procedure information  and use below pattern to mapping it (below is an example) finally,also Return description  a Mermaid flowchart for the first procedure using graph TD syntax (for a vertical layout). Ensure that All node labels are enclosed in double quotes ("").There are no extra spaces inside {{}} brackets. below is that example: 

Extracting the Model from 3GPP Specification

Core Components to Identify

□ States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or IDs.

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

save_procedural_info_to_txt(procedural_info, "output3-1-1-1.txt")  # For plain text