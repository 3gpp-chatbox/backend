from neo4j import GraphDatabase

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "your_password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_entity(tx, entity_name):
    tx.run("MERGE (e:Entity {name: $name})", name=entity_name)

def create_relationship(tx, entity1, entity2, relation):
    tx.run("MATCH (e1:Entity {name: $e1}), (e2:Entity {name: $e2}) "
           "MERGE (e1)-[:RELATION {type: $rel}]->(e2)", e1=entity1, e2=entity2, rel=relation)

# Store some relationships
with driver.session() as session:
    session.write_transaction(create_entity, "3GPP")
    session.write_transaction(create_entity, "NAS Protocol")
    session.write_transaction(create_relationship, "3GPP", "NAS Protocol", "Defines")

print("Stored knowledge graph in Neo4j!")
