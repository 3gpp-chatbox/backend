'''
Query the chunk table in the /DB/chunkdb database and retrieve all title values.
Construct a prompt for an LLM (Large Language Model). This prompt should:
Include the retrieved titles as context.
Instruct the LLM to analyze the titles based on keywords, terminology, and other indicators suggestive of 5G NAS procedures.
Specifically request the LLM to identify the titles with the highest probability of containing 5G NAS procedures.
Request the LLM to return its response as a JSON object, where the keys could be descriptive labels (e.g., "most_relevant_titles", "potentially_relevant_titles") and the values are lists of the corresponding titles.
Send the prompt to the LLM.
Parse the LLM's JSON response.

'''
import sqlite3
import json
import google.generativeai as genai
from typing import Dict, List, Set
from pydantic import BaseModel, Field

class ProcedureCategory(BaseModel):
    most_relevant_titles: List[str] = Field(default_factory=list)
    related_titles: List[str] = Field(default_factory=list)

class ProcedureIndicators(BaseModel):
    registration_keywords: List[str] = Field(default_factory=list)
    session_keywords: List[str] = Field(default_factory=list)

class TaxonomyResponse(BaseModel):
    Registration_Procedures: ProcedureCategory
    Session_Management_Procedures: ProcedureCategory
    procedure_indicators: ProcedureIndicators

class TitleAnalyzer:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    def retrieve_titles(self, db_path: str) -> List[str]:
        """Retrieve all titles from the chunk database"""
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT title FROM chunks")
                titles = [row[0] for row in cursor.fetchall() if row[0]]
                print(f"Retrieved {len(titles)} unique titles from database")
                return titles
        except Exception as e:
            print(f"Error retrieving titles: {e}")
            return []

    def analyze_titles(self, titles: List[str]) -> Dict:
        """Analyze titles using LLM to identify relevant procedures"""
        if not titles:
            return {"error": "No titles provided for analysis"}

        prompt = self._create_analysis_prompt(titles)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            if response.text:
                return self._parse_response(response.text)
            return {"error": "Empty response from LLM"}
            
        except Exception as e:
            print(f"Error analyzing titles: {e}")
            return {"error": str(e)}

    def _create_analysis_prompt(self, titles: List[str]) -> str:
        """Create prompt for title analysis"""
        titles_text = "\n".join([f"- {title}" for title in titles])
        
        return f"""You are a 3GPP specification expert. Analyze the following titles and categorize them according to the 3GPP 24.501 procedure taxonomy.

Taxonomy Structure:
1. Top-Level Categories:
   - Registration Procedures
   - Session Management Procedures

2. Second-Level: Individual Procedures:
   - Registration Procedures:
     - Initial Registration
     - Periodic Registration
     - Deregistration
   - Session Management Procedures:
     - Session Establishment
     - Session Modification
     - Session Release

Titles to analyze:
{titles_text}

Instructions:
1. Analyze each title and categorize it according to the taxonomy above
2. Return results in the following JSON format, ensuring it is valid JSON:

{{
    "Registration_Procedures": {{
        "most_relevant_titles": [
            "title1",
            "title2"
        ],
        "related_titles": [
            "title3",
            "title4"
        ]
    }},
    "Session_Management_Procedures": {{
        "most_relevant_titles": [
            "title5",
            "title6"
        ],
        "related_titles": [
            "title7",
            "title8"
        ]
    }},
    "procedure_indicators": {{
        "registration_keywords": [
            "keyword1",
            "keyword2"
        ],
        "session_keywords": [
            "keyword3",
            "keyword4"
        ]
    }}
}}

Focus on identifying titles that:
1. Directly describe procedures (e.g., "Initial registration procedure")
2. Contain procedure-related content (e.g., "States and state transitions")
3. Include relevant terminology (e.g., "registration", "session", "PDU")

Return a valid JSON object only. Do not include code block markers or any additional text.
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse and validate LLM response using Pydantic"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '')
            
            # Find and extract JSON content
            if not cleaned_text.startswith('{'):
                start_idx = cleaned_text.find('{')
                end_idx = cleaned_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    cleaned_text = cleaned_text[start_idx:end_idx + 1]
                else:
                    return {"error": "No valid JSON found in response"}

            # Clean any remaining whitespace
            cleaned_text = cleaned_text.strip()

            try:
                # Parse JSON and validate with Pydantic
                data = json.loads(cleaned_text)
                validated_data = TaxonomyResponse(**data)
                return validated_data.dict()
            except json.JSONDecodeError as e:
                # If initial parse fails, try to fix common JSON issues
                cleaned_text = (
                    cleaned_text
                    .replace('\n', '')  # Remove newlines
                    .replace('    ', '')  # Remove indentation
                    .replace('...', '')   # Remove ellipsis
                )
                # Try parsing again
                data = json.loads(cleaned_text)
                validated_data = TaxonomyResponse(**data)
                return validated_data.dict()
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:200]}...")
            print(f"Cleaned text: {cleaned_text[:200]}...")
            return {"error": "Invalid JSON format in response"}
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Response text: {response_text[:200]}...")
            return {"error": str(e)}

def main(db_path: str, api_key: str):
    """Main function to retrieve and analyze titles"""
    analyzer = TitleAnalyzer(api_key)
    
    # Retrieve titles from database
    print("Retrieving titles from database...")
    titles = analyzer.retrieve_titles(db_path)
    
    if not titles:
        print("No titles found in database")
        return
    
    # Analyze titles using LLM
    print("Analyzing titles according to procedure taxonomy...")
    result = analyzer.analyze_titles(titles)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    # Print results by category
    categories = ["Registration_Procedures", "Session_Management_Procedures"]
    for category in categories:
        print(f"\n{category.replace('_', ' ')}:")
        print("\nMost Relevant Titles:")
        for title in result[category]["most_relevant_titles"]:
            print(f"- {title}")
            
        print("\nRelated Titles:")
        for title in result[category]["related_titles"]:
            print(f"- {title}")
    
    # Print keywords
    print("\nProcedure Indicators:")
    for key, values in result["procedure_indicators"].items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(", ".join(values))

if __name__ == "__main__":
    import os
    import sys
    
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(root_folder)
    from config import Gemini_API_KEY

    API_KEY = Gemini_API_KEY
    DB_PATH = os.path.join(root_folder, "DB", "chunks.db")
    
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
    else:
        main(DB_PATH, API_KEY)