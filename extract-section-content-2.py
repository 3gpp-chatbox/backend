import re
import sqlite3

import re
import sqlite3

with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

section_pattern = r'^(#+)\s+([\d\.]+)\s+(.+)$'
lines = md_content.splitlines()

conn = sqlite3.connect('section_content_with_name.db')  # Changed database name
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS section (
    section_id TEXT,
    section_name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS content (
    section_id TEXT,
    section_name TEXT,
    chunk_id INTEGER,
    content_chunk TEXT,
    FOREIGN KEY (section_id) REFERENCES section(section_id)
)''')

current_section_id = None
current_section_name = None #add this.
current_content = []

for line in lines:
    section_match = re.match(section_pattern, line)
    if section_match:
        # Store previous section's content chunks
        if current_section_id and current_content:
            content_text = "\n".join(current_content).strip()
            chunks = content_text.split("\n\n")
            for chunk_id, chunk in enumerate(chunks):
                if chunk.strip():
                    cursor.execute("INSERT INTO content (section_id, section_name, chunk_id, content_chunk) VALUES (?, ?, ?, ?)",
                                   (current_section_id, current_section_name, chunk_id, chunk.strip())) #add current_section_name
            current_content = []

        # Store new section
        current_section_id = section_match.group(2).strip()
        current_section_name = section_match.group(3).strip() #add this.
        cursor.execute("INSERT INTO section (section_id, section_name) VALUES (?, ?)",
                       (current_section_id, current_section_name))
    elif current_section_id:
        current_content.append(line)

# Store the last section's content chunks
if current_section_id and current_content:
    content_text = "\n".join(current_content).strip()
    chunks = content_text.split("\n\n")
    for chunk_id, chunk in enumerate(chunks):
        if chunk.strip():
            cursor.execute("INSERT INTO content (section_id, section_name, chunk_id, content_chunk) VALUES (?, ?, ?, ?)",
                           (current_section_id, current_section_name, chunk_id, chunk.strip())) #add current_section_name

conn.commit()
conn.close()

print("Sections and content chunks with section names stored in the database.")