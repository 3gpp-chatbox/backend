import sqlite3
import re

# Read the Markdown file
with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Connect to SQLite database
conn = sqlite3.connect('section_content_0310.db')
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
    full_section_heading TEXT,  -- New column for full heading
   
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
);
''')

# Regex to match headings like # 5 ..., ## 5.1 ..., ### 5.4.1 ...
heading_pattern = re.compile(r'^(#{1,7})\s+(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)

# Split Content by Headings
sections = heading_pattern.split(md_content)

# Track Parent Sections
parent_sections = {}  # Stores {level: section_id}
parent_section_names = {}  # Stores {level: section_name}

# Iterate through sections
for i in range(1, len(sections), 5):
    heading_level = len(sections[i])  # #, ##, ### -> Number of #
    section_id = sections[i + 1].strip()  # Extracted Section ID like 5, 5.1, 5.4.1
    section_name = sections[i + 3].strip()  # Section Title Name
    full_section_heading = f"{section_id} {section_name}"  # Combine for full heading
    content_chunk = sections[i + 4].strip() if (i + 4) < len(sections) else ''  # Content below the heading

    parent_section_id = None
    parent_section_name = None

    # If not top-level heading, find parent section
    if heading_level > 1:
        parent_section_id = parent_sections.get(heading_level - 1)
        parent_section_name = parent_section_names.get(heading_level - 1)

    # Insert into sections table (if not already there)
    cursor.execute('''
    INSERT OR IGNORE INTO sections (section_id, section_name, parent_section_id, parent_section_name, section_level)
    VALUES (?, ?, ?, ?, ?)
    ''', (section_id, section_name, parent_section_id, parent_section_name, heading_level))

    # Insert into content table
    cursor.execute('''
    INSERT OR REPLACE INTO content (section_id, section_name, parent_section_id, parent_section_name, section_level, content_chunk, full_section_heading)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (section_id, section_name, parent_section_id, parent_section_name, heading_level, content_chunk, full_section_heading))

    # Store parent section tracking
    parent_sections[heading_level] = section_id
    parent_section_names[heading_level] = section_name

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Database created successfully with full headings and content chunks.")
