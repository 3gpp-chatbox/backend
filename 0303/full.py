import sqlite3
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

import sqlite3
import google.generativeai as genai

import os
import json
from pydantic import ValidationError
import sqlite3
import os
from dotenv import load_dotenv
import re
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

DB_NAME = 'section_content_0303.db'
CHUNK_SIZE = 5000

# DB Creation (same as before)
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS sections (
        section_id TEXT PRIMARY KEY,
        section_name TEXT NOT NULL,
        parent_section_id TEXT,
        parent_section_name TEXT,
        section_level INTEGER
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS content (
        content_id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id TEXT,
        section_name TEXT,
        parent_section_id TEXT,
        parent_section_name TEXT,
        section_level INTEGER,
        content_chunk TEXT,
        status TEXT DEFAULT 'WAITING',
        chunk_index INTEGER,
        FOREIGN KEY (section_id) REFERENCES sections(section_id)
    );''')


    conn.commit()
    conn.close()

# Markdown Parsing and DB Insertion
def insert_sections(md_content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    heading_pattern = re.compile(r'^(#{1,6})\s+(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)
    parent_sections = {}
    parent_section_names = {}
    
    sections = heading_pattern.split(md_content)
    for i in range(1, len(sections), 5):
        heading_level = len(sections[i])
        section_id = sections[i + 1].strip()
        section_name = sections[i + 3].strip()
        content_chunk = sections[i + 4].strip() if (i + 4) < len(sections) else ''
        chunk_index = i // 5

        parent_section_id = parent_sections.get(heading_level - 1)
        parent_section_name = parent_section_names.get(heading_level - 1)

        cursor.execute('''INSERT OR IGNORE INTO sections (section_id, section_name, parent_section_id, parent_section_name, section_level)
        VALUES (?, ?, ?, ?, ?)''', (section_id, section_name, parent_section_id, parent_section_name, heading_level))

        cursor.execute('''INSERT INTO content (section_id, section_name, parent_section_id, parent_section_name, section_level, content_chunk, status, chunk_index)
        VALUES (?, ?, ?, ?, ?, ?, 'WAITING', ?)''', (section_id, section_name, parent_section_id, parent_section_name, heading_level, content_chunk, chunk_index))

        parent_sections[heading_level] = section_id
        parent_section_names[heading_level] = section_name

    conn.commit()
    conn.close()



if __name__ == '__main__':
    create_db()
    with open('24501-j11.md', 'r', encoding='utf-8') as file:
        md_content = file.read()
    insert_sections(md_content)
   
  