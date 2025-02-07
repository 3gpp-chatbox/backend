import os
from dotenv import load_dotenv
import google.generativeai as genai

def check_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ API key not found in .env file")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello!")
        print("✅ API key is valid and working!")
        return True
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    check_api_key() 