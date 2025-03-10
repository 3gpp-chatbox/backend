import sqlite3
import re

# Read the Markdown file
with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Connect to SQLite database
conn = sqlite3.connect('section_content_0228.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    section_name TEXT NOT NULL,
    parent_section_id TEXT,
    parent_section_name TEXT,
    section_level INTEGER
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS content (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id TEXT,
    section_name TEXT,
    parent_section_id TEXT,
    parent_section_name TEXT,
    section_level INTEGER,
    content_chunk TEXT,
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
);
''')

# Regex to match headings like # 5 ..., ## 5.1 ..., ### 5.4.1 ...
heading_pattern = re.compile(r'^(#{1,6})\s+(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)

# Track Parent Sections
parent_sections = {}  # Stores {level: section_id}
parent_section_names = {}  # Stores {level: section_name}

# Iterate through matched headings
for match in heading_pattern.finditer(md_content):
    heading_level = len(match.group(1))  # Number of # (heading level)
    section_id = match.group(2).strip()  # Extract section ID (e.g., "5", "5.1")
    section_name = match.group(4).strip()  # Extract section name

    parent_section_id = None
    parent_section_name = None

    # If not top-level heading, find parent section
    if heading_level > 1:
        parent_section_id = parent_sections.get(heading_level - 1)
        parent_section_name = parent_section_names.get(heading_level - 1)

    # Check if the section already exists (to avoid duplicates)
    cursor.execute('SELECT section_id FROM sections WHERE section_id = ?', (section_id,))
    existing_section = cursor.fetchone()

    if not existing_section:
        # Insert into sections table
        cursor.execute('''
        INSERT INTO sections (section_id, section_name, parent_section_id, parent_section_name, section_level)
        VALUES (?, ?, ?, ?, ?)
        ''', (section_id, section_name, parent_section_id, parent_section_name, heading_level))

        # Insert into content table with empty content_chunk
        cursor.execute('''
        INSERT INTO content (section_id, section_name, parent_section_id, parent_section_name, section_level, content_chunk)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (section_id, section_name, parent_section_id, parent_section_name, heading_level, ''))

    # Store parent section tracking
    parent_sections[heading_level] = section_id
    parent_section_names[heading_level] = section_name

# Commit and close connection
conn.commit()
conn.close()

print("✅ Data inserted successfully without mistakes.")
