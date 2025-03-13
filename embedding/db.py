import os
import re
import uuid  # Import uuid module to generate unique IDs
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize the Persistent Chroma client with a specific path for persistent storage
client = chromadb.PersistentClient(path="./chroma_db")  # Using PersistentClient

# Set up the collection (persistent storage will be used)
collection = client.get_or_create_collection("sections")  # Chroma will store the collection in the specified path

# Initialize the SentenceTransformer model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the Markdown file
with open('24501-j11.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Regex to match headings like # 5 ..., ## 5.1 ..., ### 5.4.1 ...
heading_pattern = re.compile(r'^(#{1,7})\s+(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)

# Track Parent Sections
parent_sections = {}  # Stores {level: section_id}
parent_section_names = {}  # Stores {level: section_name}

# Store vectors and metadata for Chroma
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

    # Extract content chunk under the heading
    content_start_index = match.end()
    next_heading_match = heading_pattern.search(md_content, content_start_index)
    content_end_index = next_heading_match.start() if next_heading_match else len(md_content)
    content_chunk = md_content[content_start_index:content_end_index].strip()

    # Combine section_id, section_name, and content_chunk to form a document for embedding
    document = f"{section_id}: {section_name} - {content_chunk}"

    # Generate embedding for the document using the model
    embedding = model.encode(document)

    # Generate a unique ID for the document using uuid
    document_id = str(uuid.uuid4())  # This generates a random unique UUID

    # Ensure that parent_section_id and parent_section_name are not None
    parent_section_id = parent_section_id if parent_section_id is not None else ""
    parent_section_name = parent_section_name if parent_section_name is not None else ""

    # Add section and its embedding to the Chroma collection
    collection.add(
        ids=[document_id],  # The unique ID for the document (generated using uuid)
        documents=[document],  # This is the document metadata we are storing
        metadatas=[{
            "section_id": section_id,
            "section_name": section_name,
            "parent_section_id": parent_section_id,
            "parent_section_name": parent_section_name,
            "section_level": heading_level
        }],
        embeddings=[embedding]  # The embedding for the document
    )

    # Store parent section tracking
    parent_sections[heading_level] = section_id
    parent_section_names[heading_level] = section_name

# Commit the data (Chroma handles this automatically, but ensure the collection is finalized)
print("✅ Data inserted successfully into Chroma.")
