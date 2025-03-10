import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load API key for LLM
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Connect to the SQLite database
conn = sqlite3.connect('section_content_summary.db')
cursor = conn.cursor()

# Fetch Level 7 or Level 6 Sections
def fetch_sections(level):
    cursor.execute('''
        SELECT content_id, section_id, parent_section_id, section_level, content_chunk, full_section_heading
        FROM content
        WHERE section_id LIKE '5%' AND section_level = ?
    ''', (level,))
    return cursor.fetchall()

# Try Level 7 first, fallback to Level 6
sections_to_process = fetch_sections(7) or fetch_sections(6)

# Group by Parent Section
parent_dict = {}
for content_id, section_id, parent, section_level, content_chunk, full_heading in sections_to_process:
    if parent not in parent_dict:
        parent_dict[parent] = []
    parent_dict[parent].append((content_id, section_id, content_chunk, full_heading, section_level))

# Choose One Family to Test (First Parent)
test_parent = list(parent_dict.keys())[0]
test_children = parent_dict[test_parent]

# Fetch Parent Content
cursor.execute('SELECT content_chunk, full_section_heading FROM content WHERE section_id = ?', (test_parent,))
parent_data = cursor.fetchone()
parent_content, parent_heading = parent_data if parent_data else ("", "")

# Build the combined prompt
combined_prompt = f"""You are a 3GPP expert and JSON expert and IT expert. You know NAS specification structure and the document structured very well.
Below is a parent section and its children sections, please summarize each child section one by one first, and then with children section summaries, combine parent itself content, to summarize parent as well. And generate for each of them a knowledge graph.
Summarization method is: focusing on entities, events, and state transitions.

Please provide the knowledge graph in valid JSON format, using the following structure:
"knowledge_graph": {{
    "nodes": [
        {{"id": "...", 
        "label": "...",
         "type": "Entity/State/Procedure/etc."}},
        // ... more nodes
    ],
    "edges": [
        {{"source": "...", 
        "target": "...", 
        "relation": "...", 
        "condition": "Optional condition"}},
        // ... more edges
    ]
}}

When summarizing the parent section, please ensure that it provides a high-level overview of the relationships between the child sections and the key concepts they introduce.

Output example:
Child Section: 5.1.3.2.1.2.1 5GMM-NULL
Summary: ...
Knowledge Graph: {...}

Child Section: 5.1.3.2.1.2.2 5GMM-DEREGISTERED
Summary: ...
Knowledge Graph: {...}

Parent Section: 5.1.3.2.1.2 Main states
Summary: ...
Knowledge Graph: {...}

\n\nParent Section: {parent_heading}\n{parent_content}\n\n"""

for content_id, section_id, content_chunk, child_heading, level in test_children:
    combined_prompt += f"Child Section: {child_heading}\n{content_chunk}\n\n"

# Save the combined prompt
with open(f'combined_prompt_{test_parent}.txt', 'w') as prompt_file:
    prompt_file.write(combined_prompt)

# Generate summary and knowledge graph in a single LLM call
response = model.generate_content(combined_prompt).text.strip()




# The LLM must be told to output the summary and knowledge graph for each child in a way that is easy to split.
# This will be refined based on the actual output.

# Save Outputs for One Family
#with open(f'family_summary_test_{test_parent}.json', 'w') as f:
#    json.dump(response, f, indent=4)

with open(f'family_summary_test_{test_parent}.json', "w", encoding='utf-8') as file:
        file.write(response)

print(f"Pipeline Execution Completed for Family: {test_parent}")