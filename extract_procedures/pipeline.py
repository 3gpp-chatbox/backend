from raw_extracting import extract_text_from_docx
from preprocess import TextPreprocessor
from entity_recognition import EntityRecognizer
from relationship_extraction import RelationshipExtractor
from data_store import DataStore

class Pipeline:
    def __init__(self, spec_name: str = "TS_23_501"):
        self.spec_name = spec_name
        self.store = DataStore()
        
    def run(self):
        """Run the complete extraction pipeline"""
        # Step 1: Extract raw text
        raw_text = extract_text_from_docx(self.spec_name)
        self.store.save_data(
            {'text': raw_text},
            'raw',
            f'{self.spec_name}_raw.json'
        )
        
        # Step 2: Clean text
        preprocessor = TextPreprocessor(self.spec_name)
        clean_text = preprocessor.clean_text()
        
        # Step 3: Extract sections and entities
        recognizer = EntityRecognizer(self.spec_name)
        sections = recognizer.extract_sections()
        entities = recognizer.extract_entities()
        
        # Save preprocessed data
        self.store.save_data(
            sections,
            'preprocessed',
            f'{self.spec_name}_sections.json'
        )
        
        # Save entities
        self.store.save_data(
            {'entities': entities},
            'entities',
            f'{self.spec_name}_entities.json'
        )
        
        # Step 4: Extract relationships
        extractor = RelationshipExtractor(self.spec_name)
        relationships = extractor.get_relationship_summary()
        self.store.save_data(
            relationships,
            'relationships',
            f'{self.spec_name}_relationships.json'
        )
        
        return {
            'raw_text': raw_text,
            'clean_text': clean_text,
            'sections': sections,
            'entities': entities,
            'relationships': relationships
        }

def main():
    pipeline = Pipeline()
    results = pipeline.run()
    
    # Print summary
    print("\nPipeline Results:")
    print(f"Raw text: {len(results['raw_text'])} characters")
    print(f"Clean text: {len(results['clean_text'])} characters")
    print(f"Sections: {len(results['sections'])} found")
    print(f"Entities: {sum(len(v) for v in results['entities'].values())} total")
    print(f"Relationships: {sum(len(v) for v in results['relationships'].values())} total")

if __name__ == "__main__":
    main() 