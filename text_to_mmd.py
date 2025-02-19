import json
import sys

def json_to_mermaid(json_file_path, output_file_path="output.mmd"):
    """Converts JSON data from a file to a Mermaid sequence diagram.

    Args:
        json_file_path: Path to the input JSON file.
        output_file_path: Path to the output Mermaid .mmd file.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        mermaid_code = "sequenceDiagram\n"

        for step in data["steps"]:
            mermaid_code += f"    Note over All: {step['step']}\n"
            for action in step.get("actions", []):
                params = ", ".join(action.get("parameters", []))
                mermaid_code += f"    participant UE\n" # or replace participants with more accurate names.
                mermaid_code += f"    participant AMF\n"
                mermaid_code += f"    participant Network\n"
                if "Send REGISTRATION REQUEST" in action['action']:
                    mermaid_code += f"    UE->>AMF: {action['action']} ({params})\n"
                elif "Send REGISTRATION ACCEPT" in action['action']:
                    mermaid_code += f"    AMF->>UE: {action['action']} ({params})\n"
                elif "Send REGISTRATION REJECT" in action['action']:
                    mermaid_code += f"    AMF->>UE: {action['action']} ({params})\n"
                elif "Send REGISTRATION COMPLETE" in action['action']:
                    mermaid_code += f"    UE->>AMF: {action['action']} ({params})\n"
                elif "Initiate 5GMM common procedures" in action['action']:
                    mermaid_code += f"    AMF->>Network: {action['action']} ({params})\n"
                elif "Skip authentication" in action['action']:
                    mermaid_code += f"    Network->>Network: {action['action']} ({params})\n"
                elif "Store information elements from REGISTRATION REQUEST" in action['action']:
                    mermaid_code += f"    AMF->>AMF: {action['action']} ({params})\n"
                elif "Start timer T3550" in action['action']:
                    mermaid_code += f"    AMF->>AMF: {action['action']} ({params})\n"
                elif "Initiate UUAA-MM procedure" in action['action']:
                    mermaid_code += f"    AMF->>AMF: {action['action']} ({params})\n"
                elif "Reset registration attempt counter" in action['action']:
                    mermaid_code += f"    UE->>UE: {action['action']} ({params})\n"
                elif "Enter state 5GMM-REGISTERED" in action['action']:
                    mermaid_code += f"    UE->>UE: {action['action']} ({params})\n"
                elif "Set 5GS update status to 5U1 UPDATED" in action['action']:
                    mermaid_code += f"    UE->>UE: {action['action']} ({params})\n"
                elif "Stop timer T3550" in action['action']:
                    mermaid_code += f"    AMF->>AMF: {action['action']} ({params})\n"
                elif "Consider parameters valid" in action['action']:
                    mermaid_code += f"    AMF->>AMF: {action['action']} ({params})\n"
                else:
                    mermaid_code += f"    UE->>UE: {action['action']} ({params})\n"

        with open(output_file_path, 'w') as out_f:
            out_f.write(mermaid_code)

        print(f"Mermaid diagram written to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: Input file '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{json_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    json_to_mermaid(input_file)