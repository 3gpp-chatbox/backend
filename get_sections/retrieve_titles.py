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
from typing import Dict, List, Tuple

class TitleAnalyzer:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0.2,  # Lower temperature for more focused analysis
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
        """Analyze titles using LLM to identify relevant 5G NAS procedures"""
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
        
        return f"""Analyze the following titles and identify those most likely to contain 5G NAS (Non-Access Stratum) procedures.

Titles to analyze:
{titles_text}

Instructions:
1. Analyze each title for keywords and terminology related to 5G NAS procedures
2. Consider terms like: registration, authentication, security, identity, session management
3. Categorize titles based on their relevance to 5G NAS procedures
4. Return results in the following JSON format:

{{
    "most_relevant_titles": [
        // Titles with highest probability of containing NAS procedures
        // These should contain clear NAS-related keywords
    ],
    "potentially_relevant_titles": [
        // Titles that might contain NAS procedures
        // These have some relevant keywords or context
    ],
    "related_keywords_found": [
        // List of NAS-related keywords found in the titles
    ]
}}

Focus on:
- Registration procedures
- Authentication procedures
- Security procedures
- Session management procedures
- Identity management
- NAS signalling
- 5G mobility management

Return ONLY the JSON object. No additional text.
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse and validate LLM response"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            if not cleaned_text.startswith('{'):
                start_idx = cleaned_text.find('{')
                end_idx = cleaned_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    cleaned_text = cleaned_text[start_idx:end_idx + 1]
                else:
                    return {"error": "No valid JSON found in response"}

            # Parse JSON
            result = json.loads(cleaned_text)
            
            # Validate required keys
            required_keys = {"most_relevant_titles", "potentially_relevant_titles", "related_keywords_found"}
            if not all(key in result for key in required_keys):
                return {"error": "Missing required keys in response"}
                
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return {"error": "Invalid JSON format in response"}
        except Exception as e:
            print(f"Error parsing response: {e}")
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
    print("Analyzing titles for NAS procedures...")
    result = analyzer.analyze_titles(titles)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    # Print results
    print("\nAnalysis Results:")
    print(f"\nMost Relevant Titles ({len(result['most_relevant_titles'])}):")
    for title in result['most_relevant_titles']:
        print(f"- {title}")
        
    print(f"\nPotentially Relevant Titles ({len(result['potentially_relevant_titles'])}):")
    for title in result['potentially_relevant_titles']:
        print(f"- {title}")
        
    print("\nRelated Keywords Found:")
    print(", ".join(result['related_keywords_found']))

if __name__ == "__main__":
    import os
    import sys
    
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(root_folder)
    from config import Gemini_API_KEY

    API_KEY= Gemini_API_KEY
    DB_PATH = os.path.join(root_folder, "DB", "chunks.db")
    
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
    else:
        main(DB_PATH, API_KEY)