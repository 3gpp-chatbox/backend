import re
import sqlite3

# Open the markdown file
# Open the markdown file with UTF-8 encoding to handle special characters
with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()


# Regular expression to capture the ToC pattern (Section ID, Section Name, Page Number)
toc_pattern = r'(\d+\.\d+(\.\d+)*)\s+([^\d]+)\s+(\d+)$'

# Find all matches in the Markdown content (multiline search)
matches = re.findall(toc_pattern, md_content, re.MULTILINE)

# Connect to SQLite (or another DB like MySQL/PostgreSQL)
conn = sqlite3.connect('toc.db')
cursor = conn.cursor()

# Create the ToC table in the database (if it doesn't exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS toc (
    section_id TEXT,
    section_name TEXT,
    page_number INTEGER
)''')

# Insert extracted ToC data into the database
for match in matches:
    section_id = match[0]
    section_name = match[2].strip()  # Remove extra spaces
    page_number = int(match[3])

    cursor.execute("INSERT INTO toc (section_id, section_name, page_number) VALUES (?, ?, ?)",
                   (section_id, section_name, page_number))

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"{len(matches)} entries inserted into the database.")
