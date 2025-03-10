import re
import sqlite3

import re
import sqlite3

with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Corrected regular expression
toc_pattern = r'(\d+(\.\d+)*)\s+([^\d]+)\s+(\d+)$'

matches = re.findall(toc_pattern, md_content, re.MULTILINE)

conn = sqlite3.connect('toc-1.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS toc (
    section_id TEXT,
    section_name TEXT,
    page_number INTEGER
)''')

for match in matches:
    section_id = match[0]
    section_name = match[2].strip()
    page_number = int(match[3])

    cursor.execute("INSERT INTO toc (section_id, section_name, page_number) VALUES (?, ?, ?)",
                    (section_id, section_name, page_number))

conn.commit()
conn.close()

print(f"{len(matches)} entries inserted into the database.")