# Primary authentication and key agreement procedure - TXT file version
import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

flash_model = "gemini-2.0-flash"
new_model = "gemini-2.5-pro-exp-03-25"
pro_model = "gemini-2.0-pro-exp-02-05"

# Load the Google API Key from the .env file
load_dotenv(override=True)

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)

def extract_procedural_info_from_text(section_name, text):
    prompt = f"""
You are a **3GPP procedure extraction tool**. Using your knowledge of 3GPP procedures but **strictly based on the provided text**, extract the **decision logic, dependencies, and fallback conditions** for the procedure **"{section_name}"**.

---

## ** What to Extract (Generalized Scope)**  
Focus on elements that influence the procedural flow, including critical decisions, dependencies, and fallback paths. Ensure completeness and precision to prevent common issues such as incorrect or incomplete handling of retries, security, and rejection causes.

- **Decision Points**: Identify key branches in the flow that depend on explicit conditions (e.g., timer expiry, state changes, security mode).
- **Dependencies**: Capture steps that depend on prior actions or conditions. Pay attention to **mandatory dependencies** that impact the flow.
- **Fallback and Retry Mechanisms**: Identify conditions where alternative flows (e.g., retries, failovers) occur. Include details on backoff, retry limits, and failure handling where applicable.

 **Strict Rule**:  
Only extract **explicit** conditions and steps mentioned in the text. Do **not** infer or assume missing information, but ensure all flow-affecting conditions are captured.

---

## ** How to Extract (Error-Preventive Method)**  

### 1 **Decision Points & Outcomes**  
- Ensure that **all decision points** that **affect flow** are captured (e.g., timer expiries, state changes).  
- Avoid omitting **fallback or retry paths** that occur after failures. For example, when a **timer expires** or when a **security failure** occurs, ensure those branches are shown with their subsequent actions.  

### 2 **Dependencies (Flow-Critical Only)**  
- Identify **critical dependencies** where one step is contingent on the successful completion of a prior step. If a procedure step cannot proceed without an earlier step or condition, capture this explicitly.  
- Be **attentive to procedural flows that depend on timeouts**, retries, or security conditions. These may vary depending on the procedure but should be consistently noted when they impact the decision flow.

### 3 **Fallback Conditions**  
- Ensure **fallback flows** are captured, especially in the event of failures or network-specific conditions. For instance, if a registration attempt fails due to an authentication issue, capture any retries or alternative flows (e.g., limited service or network recovery attempts).  
- **Retries**: If retry conditions are provided, include the **retry count** and any **maximum retry limits** mentioned.  
- **Timeouts**: If there are timeout conditions or time-based decisions (e.g., timer expiry), ensure these are captured with any associated actions that follow.

---

## ** Output Format (Flexible & Detailed for Flow Graph)**  
The extracted information should be structured as follows, ensuring a consistent format for future analysis or Flow Property Graph construction:

{{
  "decision_points": [
    {{
      "step": Step number,
      "condition": "Explicit condition causing decision",
      "outcomes": [
        {{
          "outcome": "Success",
          "next_step": X
        }},
        {{
          "outcome": "Failure - Retry",
          "next_step": Y,
          "reason": "Reason for failure (e.g., timeout, authentication failure)",
          "outcome_type": "retry"
        }},
        {{
          "outcome": "Failure - Alternative Flow",
          "next_step": Z,
          "reason": "Fallback reason (e.g., limited service, alternative action)",
          "outcome_type": "fallback"
        }}
      ]
    }}
  ],
  "dependencies": [
    {{
      "step": X,
      "depends_on": ["Step Y"],
      "type": "hard",  # Indicate if dependency is hard or soft
      "reason": "Reason for dependency (e.g., 'Step X depends on Step Y completing successfully')"
    }}
  ],
  "timeouts": [
    {{
      "step": A,
      "timeout_condition": "Explicit timeout condition",
      "timeout_action": "Action taken after timeout"
    }}
  ]
}}

Provided Context:
{text}
"""


    model_to_use = flash_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
        },
    )

    # Extract the text content from the response
    procedural_info = response.text.strip() if hasattr(response, 'text') else str(response)

    return procedural_info

def read_text_file(file_path):
    """Reads content from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_procedural_info_to_json(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(procedural_info)
    print(f"Procedural info saved to {file_path}")

def clean_json(file_path):
    """Remove Markdown-style triple backticks (```json ... ```) from the JSON file."""
    try:
        with open(file_path, "r") as f:
            raw_data = f.read()

        # Remove Markdown code block indicators (```json and ```)
        cleaned_data = raw_data.strip().replace("```json", "").replace("```", "").strip()

        # Overwrite the file with cleaned JSON
        with open(file_path, "w") as f:
            f.write(cleaned_data)

    except Exception as e:
        print(f"Error cleaning JSON: {e}")

def process_text_file(input_file_path, section_name):
    """Processes content from a text file instead of database."""
    text_content = read_text_file(input_file_path)
    if text_content is None:
        return None
        
    procedural_info = extract_procedural_info_from_text(section_name, text_content)
    return procedural_info

# Example usage: Processing a text file
input_file_path = "5.5.1.2.txt"  # Path to your input text file
section_name = "Registration procedure for initial registration"  # Name of the section/procedure

procedural_info = process_text_file(input_file_path, section_name)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "v05-step2-flashmodel.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
    clean_json("v05-step2-flashmodel.json")
else:
    print("Failed to clean json file")