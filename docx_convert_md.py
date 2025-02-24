from docx import Document
from markdownify import markdownify
import sys
import os

def docx_to_markdown(input_path, output_path=None):
    """Converts a .docx file to Markdown and saves it to a file."""
    
    # Load the .docx file
    doc = Document(input_path)
    
    # Extract text while preserving headings
    md_text = ""
    
    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            level = int(para.style.name.replace("Heading ", ""))
            md_text += f"{'#' * level} {para.text}\n\n"
        else:
            md_text += para.text + "\n\n"
    
    # Set output file name if not specified
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".md"
    
    # Save to Markdown file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    
    print(f"Converted: {input_path} -> {output_path}")

# Run from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.docx> [output.md]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    docx_to_markdown(input_file, output_file)
