import os
from dotenv import load_dotenv
import google.generativeai as genai
from neo4j import GraphDatabase

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

def check_neo4j():
    load_dotenv()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    print(f"Attempting to connect to Neo4j at {uri}")
    print(f"Using username: {user}")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✅ Successfully connected to Neo4j!")
        
        # Try a simple query
        with driver.session() as session:
            result = session.run("RETURN 1 as num")
            record = result.single()
            print(f"Test query result: {record['num']}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {str(e)}")
        return False
    finally:
        try:
            driver.close()
        except:
            pass

if __name__ == "__main__":
    check_api_key()
    print("\nTesting Neo4j connection:")
    check_neo4j() 