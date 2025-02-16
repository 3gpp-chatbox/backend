from data_extractor import GraphExtractor
from docx import Document
import os
import json

def main():
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_folder, "config.py")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        neo4j_uri = config_module.NEO4J_URI
        neo4j_user = config_module.NEO4J_USER
        neo4j_password = config_module.NEO4J_PASSWORD

        extractor = GraphExtractor(neo4j_uri, neo4j_user, neo4j_password)

        docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")
        try:
            doc = Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            extractor.process_document(text) # Pass even if it is empty
        except FileNotFoundError:
            print(f"Error: Could not find .docx file at {docx_path}")
            exit(1)
        except Exception as e:
            print(f"An error occurred during document processing: {e}")
            exit(1)

    except (ImportError, AttributeError) as e:
        print(f"Error: Could not import configuration. Make sure config.py exists in the project root. {e}")
        exit(1)

if __name__ == "__main__":
    main()