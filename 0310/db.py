import re
import chromadb
from sentence_transformers import SentenceTransformer

# ✅ Load embedding model
model_embedding = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ Use persistent ChromaDB storage
client = chromadb.PersistentClient(path="./chroma_db")

# ✅ Ensure the collection exists
collection_name = "3gpp_sections"
collections = [c.name for c in client.list_collections()]
if collection_name in collections:
    collection = client.get_collection(collection_name)
    print(f"Using existing ChromaDB collection: {collection_name}")
else:
    collection = client.create_collection(collection_name)
    print(f"Created new ChromaDB collection: {collection_name}")

# ✅ Function to load and chunk Markdown file
def load_and_chunk_md(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    section_pattern = re.compile(r'^(?P<number>\d+(\.\d+)*)(?:\s+(?P<title>.+))?$')

    sections = []
    current_section = None
    current_content = []

    for line in content.split("\n"):
        match = section_pattern.match(line.strip())
        if match:
            if current_section is not None:
                sections.append((current_section, " ".join(current_content) if current_content else "[No content]"))

            current_section = match.group("number")
            title = match.group("title") or "[No title]"
            current_content = [title]
        else:
            current_content.append(line.strip())

    if current_section is not None:
        sections.append((current_section, " ".join(current_content) if current_content else "[No content]"))

    chunks, ids = [], []
    seen_ids = set()  # To track unique ids
    for section_num, text in sections:
        sentences = re.split(r'(?<!\d)\. (?!\d)', text)
        for j, sentence in enumerate(sentences):
            if sentence.strip():
                # Create a unique ID by appending section number, sentence number, and a counter to avoid duplicates
                unique_id = f"section_{section_num}_sentence_{j}"

                # Ensure no duplicate IDs by appending a counter if needed
                counter = 1
                original_id = unique_id
                while unique_id in seen_ids:
                    unique_id = f"{original_id}_{counter}"
                    counter += 1

                seen_ids.add(unique_id)
                chunks.append(sentence.strip())
                ids.append(unique_id)

    return chunks, ids

# ✅ Load and chunk Markdown file
MD_FILE = "24501-j11.md"
chunks, ids = load_and_chunk_md(MD_FILE)

# ✅ Check that we have valid data before embedding
if len(chunks) == 0:
    print("⚠️ No valid content to embed. Exiting script.")
else:
    # ✅ Create embeddings (even for sections with no content)
    embeddings = model_embedding.encode(chunks)

    # ✅ Split embeddings into smaller batches
    BATCH_SIZE = 5000  # Adjust this value based on the error message
    for i in range(0, len(chunks), BATCH_SIZE):
        batch_embeddings = embeddings[i:i + BATCH_SIZE]
        batch_ids = ids[i:i + BATCH_SIZE]
        batch_chunks = chunks[i:i + BATCH_SIZE]

        # ✅ Store in ChromaDB
        collection.add(
            embeddings=batch_embeddings.tolist(),
            ids=batch_ids,
            documents=batch_chunks
        )

    print("✅ ChromaDB collection populated successfully!")

