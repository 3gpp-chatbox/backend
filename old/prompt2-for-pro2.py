import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

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

    Remember, all your analysis and extraction should be based on the text I provide, and you should not make any assumptions. 
    If the text contains a procedure in Mermaid Flowchart code, please correct any mistakes in the Mermaid code and return only the corrected Mermaid code—no other words. 
    If the Mermaid flowchart content is incorrect according to the text description, correct it first, then return only the correct Mermaid code.Ensure that All node labels are enclosed in double quotes .There are no extra spaces inside {{}} brackets.remember remove ```mermaid and ``` if there are any
    """

    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()


# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Function to save extracted procedural info as plain text
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
output_file_path = "getpro-from-p2.mmd"  # Output file path

# Process the document
procedural_info = process_document("pro2-output-1.txt")

# Save the extracted procedural info
save_procedural_info_to_mmd(procedural_info, "getpro2-from-p2-1.mmd")
