import sqlite3
import re

# Read the Markdown file
with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Connect to SQLite database
conn = sqlite3.connect('section_content_0228.db')
cursor = conn.cursor()

# Regex to Match Headings (like # 5, ## 5.1, ### 5.4.1 ...)
heading_pattern = re.compile(r'^(#{1,6})\s+(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)

# Split Content by Headings
sections = heading_pattern.split(md_content)

# Start iterating content chunks
for i in range(1, len(sections), 5):
    heading_level = len(sections[i])  # #, ##, ### -> Number of #
    section_id = sections[i + 1].strip()  # Extracted Section ID like 5, 5.1, 5.4.1
    section_name = sections[i + 3].strip()  # Section Title Name
    content_chunk = sections[i + 4].strip() if (i + 4) < len(sections) else ''  # Content below the heading

    # Check if the section exists in the database
    cursor.execute('SELECT section_id FROM content WHERE section_id = ?', (section_id,))
    existing_section = cursor.fetchone()

    if existing_section:
        # Update content chunk in content table
        cursor.execute('''
        UPDATE content
        SET content_chunk = ?
        WHERE section_id = ?
        ''', (content_chunk, section_id))

        print(f'Inserted content for Section: {section_id}')

# Commit changes and close connection
conn.commit()
conn.close()

print("Content chunks inserted successfully.")
