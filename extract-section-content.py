import re
import sqlite3

import re
import sqlite3

with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

section_pattern = r'^(#+)\s+([\d\.]+)\s+(.+)$'
lines = md_content.splitlines()

conn = sqlite3.connect('section_content_chunked_id.db')  # Changed database name
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS section (
    section_id TEXT,
    section_name TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS content (
    section_id TEXT,
    chunk_id INTEGER,
    content_chunk TEXT,
    FOREIGN KEY (section_id) REFERENCES section(section_id)
)''')

current_section_id = None
current_content = []

for line in lines:
    section_match = re.match(section_pattern, line)
    if section_match:
        # Store previous section's content chunks
        if current_section_id and current_content:
            content_text = "\n".join(current_content).strip()
            chunks = content_text.split("\n\n")
            for chunk_id, chunk in enumerate(chunks): #enumerate adds chunk_id
                if chunk.strip():
                    cursor.execute("INSERT INTO content (section_id, chunk_id, content_chunk) VALUES (?, ?, ?)",
                                   (current_section_id, chunk_id, chunk.strip()))
            current_content = []

        # Store new section
        current_section_id = section_match.group(2).strip()
        section_name = section_match.group(3).strip()
        cursor.execute("INSERT INTO section (section_id, section_name) VALUES (?, ?)",
                       (current_section_id, section_name))
    elif current_section_id:
        current_content.append(line)

# Store the last section's content chunks
if current_section_id and current_content:
    content_text = "\n".join(current_content).strip()
    chunks = content_text.split("\n\n")
    for chunk_id, chunk in enumerate(chunks): #enumerate adds chunk_id
        if chunk.strip():
            cursor.execute("INSERT INTO content (section_id, chunk_id, content_chunk) VALUES (?, ?, ?)",
                           (current_section_id, chunk_id, chunk.strip()))

conn.commit()
conn.close()

print("Sections and content chunks with chunk IDs stored in the database.")