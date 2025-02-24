import re
import sqlite3

with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

section_pattern = r'^(#+)\s+([\d\.]+)\s+(.+)$'
lines = md_content.splitlines()

conn = sqlite3.connect('section_content_with_level.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS section (
    section_id TEXT,
    section_name TEXT,
    section_level INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS content (
    section_id TEXT,
    section_name TEXT,
    section_level INTEGER,
    chunk_id INTEGER,
    content_chunk TEXT,
    FOREIGN KEY (section_id) REFERENCES section(section_id)
)''')

current_section_id = None
current_section_name = None
current_section_level = None #Added this.
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
                    cursor.execute("INSERT INTO content (section_id, section_name, section_level, chunk_id, content_chunk) VALUES (?, ?, ?, ?, ?)",
                                   (current_section_id, current_section_name, current_section_level, chunk_id, chunk.strip())) #Added level.
            current_content = []

        # Store new section
        current_section_id = section_match.group(2).strip()
        current_section_name = section_match.group(3).strip()
        current_section_level = len(section_match.group(1)) #Added this.
        cursor.execute("INSERT INTO section (section_id, section_name, section_level) VALUES (?, ?, ?) ",
                       (current_section_id, current_section_name, current_section_level)) #Added level.
    elif current_section_id:
        current_content.append(line)

# Store the last section's content chunks
if current_section_id and current_content:
    content_text = "\n".join(current_content).strip()
    chunks = content_text.split("\n\n")
    for chunk_id, chunk in enumerate(chunks):
        if chunk.strip():
            cursor.execute("INSERT INTO content (section_id, section_name, section_level, chunk_id, content_chunk) VALUES (?, ?, ?, ?, ?)",
                           (current_section_id, current_section_name, current_section_level, chunk_id, chunk.strip())) #Added level.

conn.commit()
conn.close()

print("Sections and content chunks with section levels stored in the database.")