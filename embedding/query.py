import chromadb
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configure API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize the Persistent Chroma client
client = chromadb.PersistentClient(path="./chroma_db")  # Chroma uses persistent storage
collection = client.get_collection("sections")  # Access the existing collection

# Step 1: Extract Table of Contents (ToC) and prepare for LLM
toc_entries = []

# Query the Chroma collection
# Ensure that you explicitly ask for documents and metadata (or other fields you need)
result = collection.query(documents=True)  # Specify what you want to query, e.g., 'documents'

# Iterate over the results and extract the metadata (section_id, section_name)
for item in result['documents']:
    metadata = item['metadata']
    section_id = metadata['section_id']
    section_name = metadata['section_name']
    toc_entries.append(f"{section_id}: {section_name}")

# Join ToC entries into a string for LLM processing
toc_text = "\n".join(toc_entries)

# Function to find sections containing procedure info
def find_section_with_procedure_info(procedure_query):
    # Prepare the prompt for LLM
    prompt = f"Here is the Table of Contents (ToC) from a 3GPP NAS document. Please list the sections containing procedures:\n{toc_text}"
    
    # Interact with Google Gemini (or other LLM) to process the ToC
    response = model.generate_content(prompt).text.strip()
    
    # Output the response from Gemini
    print(response)

# Example usage:
find_section_with_procedure_info("procedure")
