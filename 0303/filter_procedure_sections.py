import sqlite3
import google.generativeai as genai

import os
import json
from pydantic import ValidationError
import sqlite3
import os
from dotenv import load_dotenv
import re
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')


# Step 1: Filter Procedure Sections
def filter_procedure_sections():
    with sqlite3.connect('section_content_0228.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT section_id, section_name, parent_section_id, parent_section_name, section_level 
            FROM sections 
            WHERE section_name LIKE '%Procedure%'
            ORDER BY section_id;
        ''')
        return cursor.fetchall()


# Step 2: Build Recursive Tree
def build_recursive_tree(procedure_sections):
    section_dict = {}

    # Store all sections in dictionary
    for section in procedure_sections:
        section_id, section_name, parent_section_id, parent_section_name, section_level = section
        section_dict[section_id] = {
            "section_name": section_name,
            "parent_section_id": parent_section_id,
            "children": [],
            "section_level": section_level
        }

    # Assign children to parents
    for section_id, section_data in section_dict.items():
        parent_id = section_data["parent_section_id"]
        if parent_id in section_dict:
            section_dict[parent_id]["children"].append(section_id)

    return section_dict



# Step 3: Store the Recursive Tree in a File
def store_tree_in_file(output_filename, tree):
    with open(output_filename, 'w') as f:
        json.dump(tree, f, indent=4)


# Step 3: Fetch Content
def fetch_content(section_id):
    with sqlite3.connect('section_content_0228.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT content_chunk FROM content WHERE section_id = ? ORDER BY content_id
        ''', (section_id,))
        chunks = cursor.fetchall()
        return "\n".join(chunk[0] for chunk in chunks if chunk[0])


# Step 4: Merge Parent + Children Content 🌶️
#def merge_content(tree, section_id):
 #   content = fetch_content(section_id)

    # Merge Children Content 🔥 Recursively
  #  for child_id in tree[section_id]["children"]:
 #       content += "\n\n" + merge_content(tree, child_id)

 #   return content



def extract_procedural_info_from_text(section_name, text):
    """Extracts procedural information from the text and returns separate JSON and description outputs."""
    prompt = f"""
    Below is the chunk text of a section, read it carefully first:

    {text}

    Remember, all your analysis should be based on the chunk text i provided, and you should not make any assumptions.
    

    This section is named: {section_name},  and it is mainly about one procedure.the section name is also procedure name(or key info for procedure name). analyze the text i provided,focus on that procedure,extract the information about procedure.Structure the procedure into a  **flow property graph JSON representation** using SON format.
    response  not contain anything but json code,

    **IMPORTANT: Return the responses in the exact format like below:**,
    below is example:
Core Components to Identify

□ States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or

IDs.

(this is an json example of a procedure example):

     {{
      "procedure_name": "procedure name here ",
  "description": " description here  ",
 
      "nodes": [
        {{
          "id": "UE_Powered_On",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "UE_Attaching",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "Attach_Request_Received",
          "type": "event",
          "properties": {{
            "message_type": "Attach Request"
          }},
          "parameters": ["IMSI", "TAI"]
        }}
      ],
      "edges": [
        {{
          "from": "UE_Powered_On",
          "to": "UE_Attaching",
          "action": "Send_Attach_Request",
          "properties": {{
            "parameters": ["IMSI", "TAI"],
            "metadata": {{
              "timestamp": "T0"
            }}
          }}
        }},
        {{
          "from": "UE_Attaching",
          "to": "MME_Processing",
          "event": "Attach_Request_Received",
          "properties": {{}}
        }}
      ]
    }}



    """

    response = model.generate_content(prompt).text.strip()
    return response


# Step 5: Store Results in File with Cleaned JSON Data
def store_results_in_file(output_filename, section_id, json_data):
    """Store the flow graph JSON data into a file."""
    
    # Print the json_data for debugging purposes
    print(f"Storing result for section {section_id}:")

    # Clean up the JSON response by removing extraneous markdown formatting
    # Strip markdown code block formatting like ```json and ```

    cleaned_json_data = re.sub(r'```json|```', '', json_data).strip()

    # Check if the cleaned_json_data is empty
    if not cleaned_json_data:
        print(f"❌ No valid JSON data for Section {section_id}. Skipping...")
        return  # Skip storing this section if the data is empty

    try:
        # Try to parse the cleaned json_data as JSON
        flow_graph = json.loads(cleaned_json_data)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to decode JSON for Section {section_id}: {e}")
        print(f"Response Data: {cleaned_json_data}")  # Print the problematic data for further investigation
        return  # Skip storing this section if the JSON is invalid

    # Check if the file exists, create if not
    if not os.path.exists(output_filename):
        with open(output_filename, 'w') as outfile:
            # Start with an empty list for results if the file doesn't exist
            json.dump([], outfile, indent=4)

    # Append the result to the file
    with open(output_filename, 'r+') as outfile:
        data = json.load(outfile)
        # Add the new result
        data.append({
            "section_id": section_id,
            "flow_graph": flow_graph
        })
        # Move to the beginning of the file to overwrite
        outfile.seek(0)
        # Write the updated content back to the file
        json.dump(data, outfile, indent=4)

# Main Execution Pipeline 🔥
if __name__ == '__main__':
    # Define the output filename here, before it's used
    output_filename = 'procedure_flow_graphs.json'


    # Step 1: Filter Procedure Sections
    procedure_sections = filter_procedure_sections()
    print(f"Total Procedure Sections Found: {len(procedure_sections)}")

    # Step 2: Build Tree
    procedure_tree = build_recursive_tree(procedure_sections)
    print(f"Total Parent Sections: {len([k for k, v in procedure_tree.items() if v['children']])}")


    # Step 3: Save the Tree to a File (before any LLM processing)
    output_filename = "procedure_tree.json"
    store_tree_in_file(output_filename, procedure_tree)
    print(f"Recursive Tree saved to {output_filename}")


    # Step 3: Merge Content for All Sections
    # for section in procedure_sections:
      #   section_id = section[0]
      #   merged_content = merge_content(procedure_tree, section_id)
      #   print(f"✅ Merged Content Length for Section {section_id}: {len(merged_content)}")

        # Step 4: Extract Procedural Information from Merged Content using Gemini
      #   json_response = extract_procedural_info_from_text(section[1], merged_content)
        
       #  if json_response:
            #print(f"Flow Graph JSON for Section {section_id}:")
            #print(json_response)  # Print or store the flow graph JSON
       #         # Step 5: Store the Result in the File
       #      store_results_in_file(output_filename, section_id, json_response)
       #  else:
       #      print(f"❌ No flow graph generated for Section {section_id}")
