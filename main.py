import subprocess
import time
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# File paths
JSON_FILE = "data.json"
MERMAID_FILE = "graph.mmd"

def run_extraction():
    """Run the extraction script to create the JSON file."""
    print("Running extraction script...")
    subprocess.run(["python", "extract_json.py"])

def run_validation():
    """Run the validation script and return validation result."""
    print("Running validation script...")
    result = subprocess.run(["python", "validate_json.py"], capture_output=True, text=True)
    return result.stdout.strip()

def run_correction(error_info):
    """Run the correction script if the JSON is invalid."""
    print("Running AI correction script...")
    subprocess.run(["python", "correct_json.py", error_info])

def convert_to_mermaid(json_file):
    """Convert the JSON procedure into Mermaid syntax using the Gemini model."""
    with open(json_file, "r") as f:
        json_data = json.load(f)

    # Create the prompt for the model
    prompt = f"""
    Convert the following JSON representation of a network procedure into a flow property graph using Mermaid syntax.
    
    **Guidelines:**
    - **State nodes** should be represented as `[label (state)]`.
    - **Action nodes** should be `[label (action)]`.
    - **Events** should be labeled edges `--> |Event Name|`.
    - **Metadata & parameters** should be included if relevant.
    - **Ensure valid Mermaid syntax and return only the diagram with no extra text.**
    - **Ensure that All node labels are enclosed in double quotes .There are no extra spaces inside {{}} brackets.**

    ```json
    {json.dumps(json_data, indent=2)}
    ```
    
    **Output only valid Mermaid syntax**, with no extra text.
    """

    # Call Gemini LLM to generate the Mermaid diagram
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    while True:
        # Step 1: Extract JSON
        run_extraction()

        if not os.path.exists(JSON_FILE):
            print("Error: JSON file not found. Retrying extraction...")
            time.sleep(2)
            continue

        # Step 2: Validate JSON
        validation_result = run_validation()

        if "VALID JSON" in validation_result:
            print("JSON is valid! Proceeding with conversion...")

            # Step 3: Convert JSON to Mermaid using the inline convert_to_mermaid function
            with open(JSON_FILE, "r") as f:
                json_data = json.load(f)

            # Generate Mermaid diagram using Gemini LLM
            prompt = f"""
            Convert the following JSON representation of a network procedure into a flow property graph using Mermaid syntax.


            **Guidelines:**
    - **State nodes** should be represented as `[label (state)]`.
    - **Action nodes** should be represented as `[label (action)]`.
    - **Event nodes** should be represented as `[label (event)]`.
    - **Edges (Transitions)** should be represented as `--> |Event Label|` where **Event Label** should be the description of the event that triggers the transition. Avoid any quotes or spaces around the event label.
    - **Metadata & parameters** (e.g., "timer types" or "conditions") should be included in the edge label in parentheses where relevant, separated by commas.
    - Ensure that the generated Mermaid diagram follows **valid Mermaid syntax** and **returns only the diagram with no extra text**.
    - Ensure **valid syntax** and **clear distinction between state, event, and action nodes**.
    - **If there are any complex event conditions or parameters** (e.g., timers, messages), **include them inside parentheses** after the event label in a readable way.
     - **Ensure that All node labels are enclosed in double quotes .There are no extra spaces inside {{}} brackets.**


            ```json
            {json.dumps(json_data, indent=2)}
            ```

            **Output only valid Mermaid syntax**, with no extra text.
            """
            mermaid_output = model.generate_content(prompt).text.strip()

            # Save the Mermaid diagram to a file
            with open(MERMAID_FILE, "w") as f:
                f.write(mermaid_output)
            print(f"Mermaid diagram saved successfully to {MERMAID_FILE}!")

            break  # Exit the loop after successful conversion

        else:
            print("Invalid JSON detected. Running correction...")
            run_correction(validation_result)  # Step 4: AI Correction
            time.sleep(2)  # Optional delay before retrying

if __name__ == "__main__":
    main()
