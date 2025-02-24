



import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file


# Load .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')



# Function to extract procedural flow from a text file using Gemini
def extract_procedural_info_from_text(text):
    # Structured prompt for the model
    prompt = f"""
    Read the text carefully:

    {text}

   Remember, all your analysis and corrections should be based on the text I provide, and you should not make any assumptions.  
   convert the json in text to flow property graph using mermaid format.only return the mermaid code.
   Do not include ` ```mermaid ` and ` ``` ` in your response.
    """

    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to save extracted procedural info as JSON
def save_procedural_info_to_mmd(procedural_info, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

# Main function to process a document from a text file
def process_document(file_path):
    # Step 1: Read the content from the text file
    text = read_text_from_file(file_path)

    # Step 2: Extract procedural flow from the text
    procedural_info = extract_procedural_info_from_text(text)

    return procedural_info

# Example usage: Processing a text file instead of a database
input_file_path = "your_text_file.txt"  # Replace with the actual path of your .txt file
output_file_path = "procedure5-4-7-fpg.json"  # Output file path with .json extension

# Process the document
procedural_info = process_document("procedure-5-5-1-2-2.txt")

# Save the extracted procedural info to a .json file
save_procedural_info_to_mmd(procedural_info, "procedure-5-5-1-2-2-json-to-mmd.mmd")
