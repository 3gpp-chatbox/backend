from preprocess_pdfs import read_pdfs_from_directory
from extract_3gpp_entities import extract_entities_and_relationships
from extract_mobility_entities import store_in_neo4j

if __name__ == "__main__":
    data_dir = "data"  # Specify your data directory
    documents = read_pdfs_from_directory(data_dir)
    extracted_entities, extracted_relationships = extract_entities_and_relationships(documents)
    store_in_neo4j(extracted_entities, extracted_relationships) 