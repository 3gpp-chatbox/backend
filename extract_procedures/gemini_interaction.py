import google.generativeai as genai
import json
import os
import sys
from typing import Dict
import re

# Add parent directory to path to import config
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from config import Gemini_API_KEY

genai.configure(api_key=Gemini_API_KEY)

def get_nas_info_from_gemini(query: str) -> Dict:
    """Queries Gemini and returns a structured dictionary."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(query, generation_config={"max_output_tokens": 1000})

        if response and hasattr(response, "text"):
            nas_info_text = response.text.strip()
            print("Gemini's response:\n", nas_info_text)

            # 1. Attempt JSON parse (most efficient):
            # try:
            #     nas_info = json.loads(nas_info_text)
            #     if isinstance(nas_info, dict) and "Procedures" in nas_info:
            #         return nas_info  # Success!
            #     else:
            #         print("Gemini's JSON is not in the expected format.")
            #         return {} # Or you could try to fix it, see below

            # except json.JSONDecodeError:
            #     print("Failed to parse Gemini response as JSON.")


            # 2. If JSON fails, try to *fix* it (if it's close):
            # Example: Remove extra commas, fix quotes, etc.  This is highly dependent
            # on the kinds of errors Gemini makes.  You'll have to inspect the
            # `nas_info_text` to see what needs fixing.  This is optional.
            # Example:
            fixed_json_text = re.sub(r',\s*}', '}', nas_info_text) # Remove trailing commas
            try:
              nas_info = json.loads(fixed_json_text)
              return nas_info
            except:
              print("Failed to fix JSON")

            # 3. If fixing JSON fails, use the robust fallback parsing:
            nas_info = parse_gemini_output(nas_info_text)
            return nas_info  # Fallback

        else:
            print("Gemini API returned an unexpected response.")
            return {}

    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        return {}

def parse_gemini_output(gemini_output: str) -> Dict: # fallback function
    """Parses Gemini's text output into a structured dictionary (old method)."""
    nas_info = {"Procedures": {}}
    current_procedure = None

    lines = gemini_output.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Procedure:"):
            current_procedure = line.split(":", 1)[1].strip()
            nas_info["Procedures"][current_procedure] = {"Messages": [], "States": []}
        elif line.startswith("Message:"):
            if current_procedure:
                message = line.split(":", 1)[1].strip()
                nas_info["Procedures"][current_procedure]["Messages"].append(message)
        elif line.startswith("State::"): # Fixed typo here
            if current_procedure:
                state = line.split(":", 1)[1].strip()
                nas_info["Procedures"][current_procedure]["States"].append(state)
    return nas_info

def main():
    query = """
    Extract NAS-NR procedures from TS 24.501 and return them in the following JSON format:
    {
        "Procedures": {
            "Registration": {
                "Messages": ["Registration Request", "Registration Accept", "Registration Complete"],
                "States": ["RM-REGISTERED", "RM-DEREGISTERED"]
            },
            "Deregistration": {
                "Messages": ["Deregistration Request", "Deregistration Accept"],
                "States": ["RM-DEREGISTERED"]
            }
        }
    }

    Only include core NAS procedures, their associated messages, and states. No descriptions or additional text.
    The response must be valid JSON.
    """
    nas_info = get_nas_info_from_gemini(query)

    if nas_info:
        with open("gemini_nas_info.json", "w") as f:
            json.dump(nas_info, f, indent=4)
        print("Gemini data saved to gemini_nas_info.json")
    else:
        print("Gemini API call failed.")

if __name__ == "__main__":
    main()