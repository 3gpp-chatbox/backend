
import sys
from preprocessor import TextPreprocessor
import os
from textChunker import TextChunker
def main():    
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_folder, "config.py")   
    docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")

    preprocessor = TextPreprocessor()
    cleaned_text = preprocessor.preprocess(docx_path)


    # parse text into a text file
    with open("cleaned_document.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("Cleaned text saved to cleaned_document.txt")

    chunker = TextChunker(n_clusters=15)
    chunks = chunker.chunk_text(" ".join(cleaned_text))
    

    # Write the resulting chunks to a text file
    with open("text_chunks.txt", "w") as file:
        for i, chunk in enumerate(chunks):
            file.write(f"Chunk {i+1}:")
            file.write(chunk + "\n")
            # Add a separator line between chunks
            file.write("-" * 100 + "\n")

if __name__ == "__main__":
    main()


