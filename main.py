import subprocess
import time
import json
import os

JSON_FILE = "data.json"

def run_extraction():
    print("Running extraction script...")
    subprocess.run(["python", "extract_json.py"])  # Step 1

def run_validation():
    print("Running validation script...")
    result = subprocess.run(["python", "validate_json.py"], capture_output=True, text=True)
    return result.stdout.strip()  # Step 2

def run_correction(error_info):
    print("Running AI correction script...")
    subprocess.run(["python", "correct_json.py", error_info])  # Step 4

def main():
    while True:
        run_extraction()  # Step 1: Extract JSON

        if not os.path.exists(JSON_FILE):
            print("Error: JSON file not found. Retrying extraction...")
            time.sleep(2)
            continue

        validation_result = run_validation()  # Step 2: Validate JSON

        if "VALID JSON" in validation_result:
            print("JSON is valid! Storing in the database...")
            # Call your database storage function here
            break
        else:
            print("Invalid JSON detected. Running correction...")
            run_correction(validation_result)  # Step 4: AI Correction
            time.sleep(2)  # Optional delay before retry

if __name__ == "__main__":
    main()
