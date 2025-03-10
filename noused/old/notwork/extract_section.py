import re
import sqlite3
import re
import sqlite3

with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Regular expression to capture section IDs and names
section_pattern = r'^(#+)\s+([\d\.]+)\s+(.+)$' #Added capture of digits and dots.

matches = re.findall(section_pattern, md_content, re.MULTILINE)

conn = sqlite3.connect('section.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS section (
    section_id TEXT,
    section_name TEXT
)''')

for match in matches:
    section_id = match[1].strip() #Get the digits and dots.
    section_name = match[2].strip() #Get the section name.

    cursor.execute("INSERT INTO section (section_id, section_name) VALUES (?, ?)",
                    (section_id, section_name))

conn.commit()
conn.close()

print(f"{len(matches)} entries inserted into the database.")