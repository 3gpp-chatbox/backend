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
conn = sqlite3.connect('section_content_summary.db')  # Your DB file
cursor = conn.cursor()

# Query: Fetch level 7 sections under parent sections starting with "5" 
cursor.execute('''
    SELECT content_id, section_id, parent_section_id, section_level, content_chunk, full_section_heading
    FROM content
    WHERE section_id LIKE '5%' AND section_level = 7
''')

# Retrieve level 7 sections
level_7_sections = cursor.fetchall()

# If no level 7 sections, fallback to level 6
if not level_7_sections:
    cursor.execute('''
        SELECT content_id, section_id, parent, section_level, content_chunk, full_section_heading
        FROM content
        WHERE section_id LIKE '5%' AND section_level = 6
    ''')

    # Retrieve level 6 sections
    level_6_sections = cursor.fetchall()
    sections_to_process = level_6_sections
else:
    sections_to_process = level_7_sections

# Group sections by their parent
parent_dict = {}
for section in sections_to_process:
    content_id, section_id, parent, section_level, content_chunk, full_heading = section
    if parent not in parent_dict:
        parent_dict[parent] = []
    parent_dict[parent].append((content_id, section_id, content_chunk, full_heading, section_level))


# Choose one family to test (let's take the first parent and its children)
parent = list(parent_dict.keys())[0]
children = parent_dict[parent]

# Generate the summary for the selected family
parent_content = None
parent_heading = None

# Find and store the parent's content (if available)
for content_id, section_id, content_chunk, full_heading, level in children:
    if parent_content is None:
        cursor.execute('SELECT content_chunk, full_section_heading FROM content WHERE section_id = ?', (parent,))
        parent_data = cursor.fetchone()
        parent_content = parent_data[0]
        parent_heading = parent_data[1]

# Now, summarize the family (parent + children)
summaries = []
for content_id, section_id, content_chunk, child_heading, level in children:
    # Combine parent content and child content
    combined_content = f"Parent Section: {parent_heading}\n{parent_content}\n\nChild Section: {child_heading}\n{content_chunk}"
    
    # Generate the summary using the LLM
    prompt = f"""you are 3gpp expert and NAS specification expert, you know the structure of document.
    Summarize the following 3GPP specification text by extracting important entities, relationships, and conditions. Focus on state transitions, actions, events, and dependencies. Provide a high-level overview:\n\n{combined_content}"""
    response = model.generate_content(prompt).text.strip()

    # Store the summary
    summaries.append({
        'content_id': content_id,
        'section_id': section_id,
        'summary': response,
        'combined_content': combined_content,  
        'parent_heading': parent_heading,
        'child_heading': child_heading
    })

# Save the summaries to a file (JSON format)
with open('family_summary_test.json', 'w') as f:
    json.dump(summaries, f, indent=4)

# Save to markdown file for better viewing
with open('family_summary_test_with_combined_content.md', 'w') as f:
    for summary in summaries:
        f.write(f"### Parent Heading: {summary['parent_heading']}\n\n")
        f.write(f"### Child Heading: {summary['child_heading']}\n\n")
        f.write(f"**Combined Content**:\n{summary['combined_content']}\n\n")
        f.write(f"**Summary**:\n{summary['summary']}\n\n")

# Output the first summary as a sample
print(summaries[0])