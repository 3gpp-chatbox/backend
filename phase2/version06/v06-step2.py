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

## ** What to Extract (Precise & Flow-Critical Elements)**  
Focus on elements that influence the procedural flow, ensuring **all decision points, dependencies, retries, and fallback paths** are captured **without assumptions**. If any required information is missing, explicitly flag it.

- **Decision Points**: Identify all **explicit decision points** (e.g., timer expiry, state transitions, security mode status).
- **Dependencies**: Capture both **hard dependencies** (strict requirements) and **soft dependencies** (preferred conditions that influence flow).
- **Fallback & Retry Mechanisms**: Extract **all retry conditions, retry limits, backoff strategies, and alternative flows**.
- **Timeout Handling**: Ensure **all timeouts** are documented, along with **post-timeout actions** (e.g., retry, failure transition, state change).

 **Strict Rule**:  
Do **not** infer missing details, but **flag potential implicit dependencies** if they are critical for procedure correctness.

---

## ** How to Extract (Error-Resilient Methodology)**  

### **1 Decision Points & Outcomes**  
- Identify all flow-changing **decision points** (e.g., timer expiry, authentication success/failure).
- For **each decision point**, extract **all possible outcomes**, ensuring no retry/fallback paths are missed.

### **2 Dependencies (Hard vs. Soft Classification)**  
- A **hard dependency** means a step **cannot occur** unless the previous step is successfully completed.
- A **soft dependency** is a recommended or preferred step but does **not strictly prevent** the next action.
- If a **dependency is missing** in the text but seems **critical to the flow**, **flag it explicitly**.

### **3 Retries & Fallback Paths (Complete Extraction)**  
- **Retries**: If a procedure supports retries, capture **retry conditions, retry limits, and retry intervals**.
- **Backoff Strategy**: If retries occur, specify if **fixed, exponential, or network-defined backoff** is used.
- **Fallback Conditions**: Extract all **alternative flows**, including **partial service, rejection handling, or alternative authentication**.

### **4 Timeouts & Post-Timeout Actions**  
- Extract all **timeouts** (e.g., `T3510`, `T3550`).
- Clearly document **what happens when a timer expires**: Does the system retry? Does it trigger a fallback? Does it enter failure mode?
- If the timeout action is **not explicitly stated**, **flag the missing information**.


---

## **🔹 Output Format (Flexible & Detailed for Flow Graph)**  
The extracted information should be structured as follows, ensuring a consistent format for future analysis or Flow Property Graph construction:

{{
  "decision_points": [
    {{
      "step": x,
      "condition": "Explicit condition causing decision",
      "outcomes": [
        {{
          "outcome": "Success",
          "next_step": Y
        }},
        {{
          "outcome": "Failure - Retry",
          "next_step": Z,
          "reason": "Reason for failure (e.g., timeout, authentication failure)",
          "outcome_type": "retry"
        }},
        {{
          "outcome": "Failure - Alternative Flow",
          "next_step": W,
          "reason": "Fallback reason (e.g., limited service, alternative action)",
          "outcome_type": "fallback"
        }}
      ]
    }}
  ],
  "dependencies": [
    {{
      "step": Y,
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
       "retry_count": 3,
      "backoff_strategy": "fixed"

    }}
  ],
   "flagged_missing_info": [
    {{
      "issue": "Potential missing implicit dependency",
      "step": "X",
      "reason": "Step X likely requires security authentication before proceeding"
    }},
    {{
      "issue": "Unclear timeout action",
      "step": "B",
      "reason": "The text does not specify what happens after T3550 expires"
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
    save_procedural_info_to_json(procedural_info, "v06-step2.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
    clean_json("v06-step2.json")
else:
    print("Failed to clean json file")