import fitz  # PyMuPDF
import re

def clean_text(text: str) -> str:
    """Cleans extracted PDF text by removing TOC, headers, footers and unnecessary whitespace."""
    cleaned = text
    cleaned = re.sub(r'ETSI\s+ETSI TS \d+\s+\d+\s+V\d+\.\d+\.\d+\s+\(\d{4}-\d{2}\)', '', cleaned)
    cleaned = re.sub(r'3GPP TS \d+\.\d+ version \d+\.\d+\.\d+ Release \d+', '', cleaned)
    cleaned = re.sub(r'ETSI\s+\d+ Route des Lucioles.*?non lucratif.*?Grasse.*?Important notice.*?authorization of ETSI\.', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\n\s*\d+\s*\n', '\n', cleaned)
    cleaned = re.sub(r'\f', ' ', cleaned)
    toc_patterns = [
        r'Table of Contents.*?(?=\d+\s+Scope)',
        r'Contents.*?(?=\d+\s+Scope)',
        r'(?:\n\d+\.[\d\.]*\s+.*?(?=\n)){3,}'
    ]
    for pattern in toc_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'^\s*\d+\.[\d\.]*\s+', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'(?m)^\s*\d+\s*$', '', cleaned)
    cleaned = re.sub(r'\s*\.\.\.\.*\s*\d+', '', cleaned)
    cleaned = re.sub(r'Reference RTS/TSGC-\d+.*?Keywords.*?\n', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\n\s*\n+', '\n\n', cleaned)
    cleaned = re.sub(r'^\.*\s*$', '', cleaned, flags=re.MULTILINE)
    return cleaned.strip()

def remove_custom_stopwords(text):
    custom_stopwords = [
        r"\bshall\b", r"\bmay\b", r"\bis defined\b", r"\bthe following\b",
        r"\baccording to\b", r"\bfor example\b", r"\brespectively\b",
        r"\bwhere applicable\b", r"\bherein\b", r"\bthereof\b",
        r"\bhereby\b", r"\bthereby\b", r"\btherefore\b", r"\bhowever\b"
    ]
    for stopword in custom_stopwords:
        text = re.sub(stopword, "", text, flags=re.IGNORECASE)
    return text

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file and cleans it."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        if text:
            print("Text extracted successfully!")
            text = clean_text(text)
            text = remove_custom_stopwords(text) # Add custom stop word removal
            if not text:
                print("Warning: Text was empty after cleaning.")
        else:
            print("Warning: No text extracted from the PDF.")
        return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return ""

def save_text_chunks_by_chapter(text, chunk_size=1500): # Increased chunk size
    """Splits text into smaller chunks for retrieval, respecting chapter and natural text boundaries."""
    if not text:
        print("No text available to chunk.")
        return []
    chapter_pattern = r"(Chapter\s+\d+[:\s]+.*)"
    chapters = re.split(chapter_pattern, text)
    chunks = []
    current_chapter = ""
    for i, part in enumerate(chapters):
        if re.match(chapter_pattern, part):
            current_chapter = part.strip()
            if i > 0:
                current_chunk = []
                current_size = 0
            continue
        if not part.strip():
            continue
        paragraphs = [p.strip() for p in part.split('\n\n') if p.strip()]
        current_chunk = []
        current_size = 0

        # Paragraph Merging
        merged_paragraphs = []
        temp_paragraph = ""
        for paragraph in paragraphs:
            if len(temp_paragraph + paragraph) < chunk_size / 3: #merge if less than 1/3 chunk size.
                temp_paragraph += " " + paragraph
            else:
                merged_paragraphs.append(temp_paragraph.strip())
                temp_paragraph = paragraph
        merged_paragraphs.append(temp_paragraph.strip()) #append the last paragraph

        for paragraph in merged_paragraphs:
            if len(paragraph) > chunk_size:
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', paragraph)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    if current_size + len(sentence) > chunk_size and current_chunk:
                        chunks.append(current_chapter + " " + ' '.join(current_chunk))
                        current_chunk = []
                        current_size = 0
                    current_chunk.append(sentence)
                    current_size += len(sentence) + 1
            else:
                if current_size + len(paragraph) > chunk_size and current_chunk:
                    chunks.append(current_chapter + " " + ' '.join(current_chunk))
                    current_chunk = []
                    current_size = 0
                current_chunk.append(paragraph)
                current_size += len(paragraph) + 2
        if current_chunk:
            chunks.append(current_chapter + " " + ' '.join(current_chunk))
    print(f"Text split into {len(chunks)} chunks.")
    chunks = [chunk for chunk in chunks if len(chunk) > 100] # Increased min chunk size
    return chunks

def preprocess_pdf(pdf_path, chunk_size=1500):
    """Preprocesses a PDF and returns chunks."""
    text = extract_text_from_pdf(pdf_path)
    if text:
        return save_text_chunks_by_chapter(text, chunk_size)
    return []

def save_chunks_to_markdown(chunks, output_file="output.md"):
    """Saves text chunks to a markdown file."""
    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"## Chunk {i + 1}\n\n")
            f.write(chunk + "\n\n")
            f.write("---\n\n")
    print(f"Chunks saved to {output_file}")

if __name__ == "__main__":
    pdf_file_path = "data/TS 24.501.pdf"
    text_chunks = preprocess_pdf(pdf_file_path, chunk_size=2000)
    if text_chunks:
        save_chunks_to_markdown(text_chunks)
    else:
        print("Preprocessing failed.")