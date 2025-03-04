# src/extract_and_store.py
from dotenv import load_dotenv
import src.lib.doc_processor as doc_processor
import src.lib.store_chunks as store_chunks

load_dotenv(override=True)


# Load the docx file inside data/
docx_file_path = "data/24501-j11.docx"

sections_to_exclude = [
    "annex",
    "appendix",
    "abbreviations",
    "scope",
    "references",
    "foreword",
    "void",
]

stripped_doc_path = doc_processor.remove_sections(
    file_path=docx_file_path, excluded_sections=sections_to_exclude
)

# Load the stripped document
doc = doc_processor.load_document(stripped_doc_path)


# Extract sections from the document
section_tree = doc_processor.extract_section_tree(doc=doc)

toc = doc_processor.extract_table_of_contents_mini(section_tree=section_tree)

# Extract doc_id from file path (e.g. "24501-j11" from "data/24501-j11.docx")
doc_id = docx_file_path.split("/")[-1].replace(".docx", "")

# Store the sections in the database
doc_name = doc.core_properties.title
store_chunks.store_chunks(
    sections_tree=section_tree, doc_name=doc_name, toc=toc, doc_id=doc_id
)
