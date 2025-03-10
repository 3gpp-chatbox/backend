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
model = genai.GenerativeModel('gemini-2.0-flash')


JSON_FILE = "data.json"

def load_json():
    """Load JSON from file."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def correct_json(error_info):
    """Send invalid JSON and error details to Google AI (Gemini) for correction."""
    json_data = load_json()
    if json_data is None:
        print("Error: Failed to load JSON file.")
        return

    prompt = f"""
    The following JSON is invalid due to the errors provided. Please correct it:
    
    **Invalid JSON:**  
    ```json
    {json.dumps(json_data, indent=2)}
    ```
    
    **Errors:**  
    {error_info}
    
    Return only the corrected JSON without explanations.if there is ```json and ``` at the beginning and end of the response, remove them.
    """

    # Send request to Google AI (Gemini) model
    model = genai.GenerativeModel("gemini-pro")  # Use "gemini-pro" for text tasks
    response = model.generate_content(prompt)

    corrected_json = response.text.strip()  # Get the response text

    try:
        # Save corrected JSON back to file
        with open(JSON_FILE, "w") as f:
            f.write(corrected_json)
        print("JSON corrected and saved.")
    except Exception as e:
        print(f"Error saving corrected JSON: {e}")

if __name__ == "__main__":
    # Get error details from command line argument (passed from main.py)
    error_info = sys.argv[1] if len(sys.argv > 1) else "Unknown error"
    correct_json(error_info)
