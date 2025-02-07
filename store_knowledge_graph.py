from neo4j import GraphDatabase

URI = "bolt://localhost:7687"  # Adjust if needed
USERNAME = "neo4j"  # Default user
PASSWORD = "testtest"  # Replace with the correct password

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def create_entity(tx, name, entity_type):
    query = "CREATE (n:Entity {name: $name, type: $entity_type})"
    tx.run(query, name=name, entity_type=entity_type)

with driver.session() as session:
    session.execute_write(create_entity, "3GPP", "Standard Organization")

print("Node added successfully!")

def check_data(tx):
    result = tx.run("MATCH (n) RETURN n LIMIT 10")
    return [record["n"] for record in result]

with driver.session() as session:
    nodes = session.execute_read(check_data)

print("Nodes in database:", nodes)
