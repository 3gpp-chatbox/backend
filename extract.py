import sqlite3
import google.generativeai as genai

# Initialize Google Generative AI (Gemini)
genai.configure(api_key="AIzaSyCXPLahgYeLeOICLr87Zv7AJnjBBuMOCJo")  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to extract procedural flow from the chunk of text using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
    Extract procedural flow information from the following section:

    {text}

    Your task is to extract the following elements:
    1. Steps: The different states of the procedure (e.g., UE state, network state).
    2. Actions: What actions are taken during each step.
    3. Events: What triggers each action or step.
    4. Parameters: What parameters are exchanged between the entities.
    5. Metadata: Any additional contextual information like message types or timestamps.
    
    Provide the information in the following structured format:

    Example:
    {{
        "steps": [
            {{
                "step": "Step 1",
                "description": "Attach Request: UE sends an Attach Request message to the MME.",
                "actions": [
                    {{"action": "Send Attach Request", "parameters": ["IMSI", "TAI"]}}
                ],
                "events": ["Attach Request Received"]
            }},
            {{
                "step": "Step 2",
                "description": "Authentication: MME initiates authentication procedures.",
                "actions": [
                    {{"action": "Initiate Authentication", "parameters": ["IMSI", "TAI"]}}
                ],
                "events": ["Authentication Challenge"]
            }}
        ]
    }}

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
print("Extracted Procedural Information:\n")
print(procedural_info)