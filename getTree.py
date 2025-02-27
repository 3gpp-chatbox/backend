from pydantic import BaseModel, Field
from typing import Dict, List
import google.generativeai as genai
import json
from DBHandler import DBHandler
import os
import sys

# Define Pydantic models
class Metadata(BaseModel):              
    References: List[str] = Field(default_factory=list, description="Relevant specification sections")

class Procedure(BaseModel):
    procedure_name: str = Field(..., description="Name of the procedure")
    metadata: Metadata

class MobilityManagementProcedures(BaseModel):
    procedures: Dict[str, List[Procedure]] = Field(..., description="Procedures organized by category")

class TaxonomyExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API, configure the model, and load it"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 4096,
        }
        

    def _create_taxonomy_prompt(self) -> str:
        """Create prompt for taxonomy extraction"""
        return """Extract NAS-NR related Mobility Management (MM) procedures from 3GPP TS 24.501.

For each procedure, provide:
1. Procedure name and category
2. Metadata:
    - Relevant spec references (as array)
Ensure the output matches the structured JSON schema defined for Mobility Management procedures.
"""

    def _log_token_usage(self, response):
        """Log token usage from Gemini response"""
        try:
            # Get candidates (responses) from the response object
            candidates = response.candidates
            if not candidates:
                print("No candidates in response")
                return

            # Get token counts from the first candidate
            token_counts = candidates[0].token_count
            if token_counts:
                print("\nToken Usage:")
                print(f"Total tokens: {token_counts}")
        except AttributeError as e:
            print(f"Could not access token count: {e}")
        except Exception as e:
            print(f"Error logging token usage: {e}")

    def extract_taxonomy(self) -> MobilityManagementProcedures:
        """Extract and validate taxonomy using Gemini"""
        try:
            # Get response from LLM
            response = self.model.generate_content(
                self._create_taxonomy_prompt(),
                generation_config=self.generation_config,
                safety_settings=[],  # Add safety settings if needed
            )
             # Log token usage
            if response.usage_metadata:
                total_tokens = response.usage_metadata.total_token_count
                print(f"Token Usage: {total_tokens} tokens")
            else:
                print("Token Usage: Not available.")
            
            if not response.text:
                print("Error: Gemini returned an empty response")
                return None

            # Log token usage
            self._log_token_usage(response)
            
            print("\nGemini response:", response.text)
            try:
                # Parse the response into JSON
                structured_output = json.loads(response.text)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON response from Gemini - {e}")
                return None

            # Validate using Pydantic
            taxonomy = MobilityManagementProcedures(**structured_output)
            return taxonomy

        except Exception as e:
            print(f"Error extracting taxonomy: {e}")
            return None

def main():
    """Main function to extract and store taxonomy"""

    root_folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(root_folder)
    from config import Gemini_API_KEY

    if not Gemini_API_KEY:
        print("Error: Gemini API key not found")
        return

    try:
        # Initialize extractor and database
        extractor = TaxonomyExtractor(Gemini_API_KEY)
        db = DBHandler()

        # Extract taxonomy
        print("\nExtracting MM procedure taxonomy...")
        taxonomy = extractor.extract_taxonomy()

        if not taxonomy:
            print("Failed to extract taxonomy")
            return

        # Store procedures in database
        print("\nStoring procedures in database...")
        for category, procedures in taxonomy.procedures.items():
            print(f"\nProcessing category: {category}")
            for proc in procedures:
                try:
                    # Create a Procedure instance with category
                    procedure = Procedure(
                        procedure_name=proc.procedure_name,
                        category=category,
                        metadata=proc.metadata
                    )
                    # Store the procedure
                    db.store_procedure(procedure)
                    print(f"✓ Stored procedure: {proc.procedure_name}")
                except Exception as e:
                    print(f"✗ Failed to store {proc.procedure_name}: {e}")

        print("\n✓ Taxonomy extraction and storage complete")

    except Exception as e:
        print(f"\n✗ Error in main process: {e}")

if __name__ == "__main__":
    main()