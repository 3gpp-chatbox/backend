import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')


# Function to extract procedural flow from a JSON object using Gemini
def extract_procedural_info_from_json(json_data):
    # Structured prompt for the model
    prompt = f"""
    Convert the following JSON representation into a flow property graph using Mermaid syntax.

    **Guidelines:**
    1. **State Nodes**: Represent these as `[label (state)]`.
    2. **Action Nodes**: Represent these as `[label (action)]`.
    3. **Event Transitions**: Represent these edges as `--> |Event Name|`, where the event name should be the label for the transition between states/actions.
    4. **Metadata & Parameters**: If relevant, include them as node attributes or as part of the event labels.
    5. **Node Labels**: All node labels should be enclosed in double quotes (e.g., `"Label"`).
    6. **Ensure no extra spaces** inside curly braces `{{}}` or parentheses `()`.
    7. **Mermaid Syntax**: Return only valid Mermaid syntax, with no extra text or explanation.
    8. **Ensure edges are well-labeled**: All event transitions between states/actions should be explicitly labeled with the event name.

    Below is the input JSON data:

    ```json
    {json.dumps(json_data, indent=2)}
    ```

    **Output only valid Mermaid syntax**, with no extra text or explanation.
    """


    # Send request to Gemini API to extract procedural information
    response = model.generate_content(prompt)
    return response.text.strip()


# Function to read JSON data from a file
def read_json_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Function to save extracted procedural info as a Mermaid file
def save_procedural_info_to_mmd(procedural_info, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")


# Main function to process a document from a JSON file
def process_document(file_path):
    # Step 1: Read the JSON content from the file
    json_data = read_json_from_file(file_path)

    # Step 2: Extract procedural flow from the JSON data
    procedural_info = extract_procedural_info_from_json(json_data)

    return procedural_info


# Example usage: Processing a JSON file and saving the Mermaid diagram
input_file_path = "data.json"  # Replace with the actual path of your .json file
output_file_path = "output.mmd"  # Output file path for the Mermaid diagram

# Process the document
procedural_info = process_document(input_file_path)

# Save the extracted procedural info as a Mermaid file
save_procedural_info_to_mmd(procedural_info, output_file_path)
