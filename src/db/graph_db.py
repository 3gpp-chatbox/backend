import os
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
from src.lib.logger import get_logger

# Set up logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv(override=True)


def get_neo4j_connection():
    """Create a Neo4j database connection using environment variables."""
    try:
        logger.info("Attempting to connect to Neo4j database...")
        uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
        username = os.getenv("NEO4J_USERNAME", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")

        driver = GraphDatabase.driver(uri, auth=(username, password))
        # Verify connection is working
        with driver.session() as session:
            session.run("RETURN 1")

        logger.info("Successfully connected to Neo4j database")
        return driver
    except Exception as e:
        logger.error(f"Neo4j database connection error: {str(e)}")
        raise


def close_neo4j_connection(driver):
    """Close the Neo4j database connection."""
    if driver is not None:
        logger.info("Closing Neo4j database connection")
        driver.close()


def clear_database(driver):
    """Remove all nodes and relationships from the database."""
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        # Get all constraints
        constraints = session.run("SHOW CONSTRAINTS").data()
        # Drop each constraint
        for constraint in constraints:
            session.run(f"DROP CONSTRAINT {constraint['name']}")
        logger.info("Database cleared")


def create_constraints(driver):
    """Create necessary constraints for the database."""
    with driver.session() as session:
        # Create constraints for both State and Event nodes
        session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:State) REQUIRE n.id IS UNIQUE"
        )
        session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Event) REQUIRE n.id IS UNIQUE"
        )
        logger.info("Constraints created")


def import_node(driver, node):
    """Import a single node into Neo4j."""
    with driver.session() as session:
        # Create base node with common properties
        # Based on node type, create node with appropriate label
        if node["type"] == "State":
            query = """
            MERGE (n:State {id: $id})
            SET n.entity = $entity,
                n.nodeType = $type,
                n.description = $description,
                n.document_id = $document_id,
                n.section_reference = $section_reference,
                n.other_references = $other_references,
                n.state = $state
            """
            state = node["properties"]["state"]
            session.run(
                query,
                id=node["id"],
                entity=node["entity"],
                type=node["type"],
                description=node["properties"]["description"],
                document_id=node["metadata"]["document_id"],
                section_reference=node["metadata"]["section_reference"],
                other_references=node["metadata"]["other_references"],
                state=state,
            )
        else:  # Event type
            query = """
            MERGE (n:Event {id: $id})
            SET n.entity = $entity,
                n.nodeType = $type,
                n.description = $description,
                n.document_id = $document_id,
                n.section_reference = $section_reference,
                n.other_references = $other_references,
                n.eventType = $eventType
            """
            event_type = node["properties"]["eventType"]
            session.run(
                query,
                id=node["id"],
                entity=node["entity"],
                type=node["type"],
                description=node["properties"]["description"],
                document_id=node["metadata"]["document_id"],
                section_reference=node["metadata"]["section_reference"],
                other_references=node["metadata"]["other_references"],
                eventType=event_type,
            )


def import_nodes(driver, nodes):
    """Import all nodes into Neo4j."""
    logger.info(f"Importing {len(nodes)} nodes...")
    for node in nodes:
        import_node(driver, node)
    logger.info("All nodes imported successfully")


def import_edge(driver, edge):
    """Import a single edge into Neo4j."""
    with driver.session() as session:
        # Base relationship properties
        params = {
            "id": edge["id"],
            "from_id": edge["from"],
            "to_id": edge["to"],
            "type": edge["type"],
            "description": edge["properties"]["description"],
        }

        # Add message properties for Action relationships
        if edge["type"] == "Action":
            params["messageType"] = edge["properties"]["messageType"]
            # Convert parameters list to JSON string for Neo4j storage
            params["parameters"] = json.dumps(edge["properties"]["parameters"])

            query = """
            MATCH (source {id: $from_id})
            MATCH (target {id: $to_id})
            CREATE (source)-[r:ACTION {
                id: $id,
                relationType: $type,
                description: $description,
                messageType: $messageType,
                parameters: $parameters
            }]->(target)
            """
        else:  # Transition type
            query = """
            MATCH (source {id: $from_id})
            MATCH (target {id: $to_id})
            CREATE (source)-[r:TRANSITION {
                id: $id,
                relationType: $type,
                description: $description
            }]->(target)
            """

        session.run(query, params)  # Remove ** to pass parameters directly


def import_edges(driver, edges):
    """Import all edges into Neo4j."""
    logger.info(f"Importing {len(edges)} relationships...")
    for edge in edges:
        import_edge(driver, edge)
    logger.info("All relationships imported successfully")


def create_procedure_node(driver, procedure_name):
    """Create a procedure node and link it to all nodes."""
    with driver.session() as session:
        session.run(
            """
        CREATE (p:Procedure {name: $name})
        WITH p
        MATCH (n:State)
        CREATE (p)-[:CONTAINS]->(n)
        WITH p
        MATCH (n:Event)
        CREATE (p)-[:CONTAINS]->(n)
        """,
            name=procedure_name,
        )
    logger.info(f"Created procedure node for '{procedure_name}'")


def import_flow_graph(json_file_path, clear=True):
    """Import the complete flow graph into Neo4j."""
    driver = None
    try:
        # Load JSON data
        with open(json_file_path, "r") as file:
            data = json.load(file)

        logger.info(f"Loading flow graph: {data['procedureName']}")

        # Connect to Neo4j
        driver = get_neo4j_connection()

        # Clear database if requested
        if clear:
            clear_database(driver)

        # Create constraints
        create_constraints(driver)

        # Import nodes and edges
        import_nodes(driver, data["nodes"])
        import_edges(driver, data["edges"])

        # Create procedure node
        create_procedure_node(driver, data["procedureName"])

        logger.info(f"Successfully imported flow graph: {data['procedureName']}")
        return True

    except Exception as e:
        logger.error(f"Error importing flow graph: {str(e)}")
        return False
    finally:
        if driver:
            close_neo4j_connection(driver)


# Test the connection if this file is run directly
if __name__ == "__main__":
    try:
        # Example: Import flow graph
        result = import_flow_graph("output/flow_graph.json")
        if result:
            logger.info("Flow graph import test successful")

        # Connect and run simple query to get procedure graph
        driver = get_neo4j_connection()
        with driver.session() as session:
            # Get all nodes in the procedure
            print("\nNodes:")
            nodes = session.run("""
                MATCH (p:Procedure {name: 'Initial Registration Procedure'})
                MATCH (p)-[:CONTAINS]->(n)
                RETURN DISTINCT n 
            """)
            for record in nodes:
                node = record["n"]
                print(node.labels)
                if "State" in node.labels:
                    print(f"State: {node['entity']} in {node['state']}")
                else:
                    print(f"Event: {node['entity']} - {node['eventType']}")

        close_neo4j_connection(driver)

    except Exception as e:
        logger.error(f"Test connection failed: {e}")
