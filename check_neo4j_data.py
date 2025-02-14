from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

def check_neo4j_data():
    # Load environment variables
    load_dotenv()
    
    # Get Neo4j credentials
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    
    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            # Count total nodes
            result = session.run("MATCH (n) RETURN count(n) as count")
            total_nodes = result.single()["count"]
            print(f"\n📊 Total nodes in database: {total_nodes}")
            
            # Count nodes by type
            result = session.run("""
                MATCH (n:Entity)
                RETURN n.type as type, count(*) as count
                ORDER BY count DESC
            """)
            print("\n📑 Nodes by type:")
            for record in result:
                print(f"  - {record['type']}: {record['count']} nodes")
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(*) as count
                ORDER BY count DESC
            """)
            print("\n🔗 Relationships by type:")
            for record in result:
                print(f"  - {record['type']}: {record['count']} relationships")
            
            # Sample of actual data
            print("\n📝 Sample of nodes and their relationships:")
            result = session.run("""
                MATCH (n)-[r]->(m)
                RETURN n.name as from, type(r) as relation, m.name as to
                LIMIT 5
            """)
            for record in result:
                print(f"  {record['from']} --[{record['relation']}]--> {record['to']}")
                
        driver.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_neo4j_data() 