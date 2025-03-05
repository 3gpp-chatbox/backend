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
        # Check if APOC is available, use it if possible
        try:
            session.run(
                "CALL apoc.schema.assert({}, {})"
            )  # Drop all constraints and indexes
            session.run(
                "MATCH (n) DETACH DELETE n"
            )  # Delete all nodes and relationships
            logger.info("Database cleared with APOC")
        except Exception:
            # Fallback without APOC
            constraints = session.run(
                "SHOW CONSTRAINTS YIELD name RETURN collect(name) AS names"
            ).single()["names"]
            if constraints:
                session.run(
                    "UNWIND $names AS name CALL { DROP CONSTRAINT $name } IN TRANSACTIONS",
                    {"names": constraints},
                )
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared without APOC")


def create_constraints(driver):
    """Create uniqueness constraints for node IDs."""
    with driver.session() as session:
        session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:State) REQUIRE n.id IS UNIQUE"
        )
        session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Event) REQUIRE n.id IS UNIQUE"
        )
        session.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Procedure) REQUIRE n.name IS UNIQUE"
        )
    logger.info("Constraints created")


def import_nodes(driver, nodes, procedure_name):
    """Import State and Event nodes with properties and metadata."""
    with driver.session() as session:
        for node in nodes:
            if "id" not in node or not node["id"]:
                logger.error(f"Node missing 'id': {node}")
                raise ValueError(f"Node missing 'id': {node}")
            # Convert nested objects to JSON strings
            properties_json = json.dumps(node["properties"])
            metadata_json = json.dumps(node["metadata"])

            query = """
                CREATE (n:{node_type})
                SET n.id = $id,
                    n.procedureName = $procedureName,
                    n.entity = $entity,
                    n.properties = $properties_json,
                    n.metadata = $metadata_json
                RETURN n
            """
            try:
                session.run(
                    query.format(node_type=node["type"]),
                    {
                        "id": str(node["id"]),  # Ensure ID is a string
                        "procedureName": procedure_name,
                        "entity": node["entity"],
                        "properties_json": properties_json,
                        "metadata_json": metadata_json,
                    },
                )
            except Exception as e:
                logger.error(f"Failed to import node {node['id']}: {str(e)}")
                raise
        logger.info(f"Imported {len(nodes)} nodes for procedure: {procedure_name}")


def import_edges(driver, edges):
    """Import edges (relationships) between nodes."""
    with driver.session() as session:
        for edge in edges:
            # Convert properties to JSON string
            properties_json = json.dumps(edge["properties"])
            query = """
                MATCH (from) WHERE from.id = $from_id
                MATCH (to) WHERE to.id = $to_id
                CREATE (from)-[r:{rel_type}]->(to)
                SET r.id = $edge_id,
                    r.properties = $properties_json
            """
            try:
                session.run(
                    query.format(rel_type=edge["type"]),
                    {
                        "from_id": str(edge["from"]),  # Ensure IDs are strings
                        "to_id": str(edge["to"]),
                        "edge_id": str(edge["id"]),
                        "properties_json": properties_json,
                    },
                )
            except Exception as e:
                logger.error(f"Failed to import edge {edge['id']}: {str(e)}")
                raise
        logger.info(f"Imported {len(edges)} edges")


def create_procedure_node(driver, procedure_name):
    """Create Procedure node and link it to its State and Event nodes."""
    query = """
        MERGE (p:Procedure {name: $name})
        WITH p
        MATCH (n:State {procedureName: $name})
        CREATE (p)-[:CONTAINS]->(n)
        WITH p
        MATCH (n:Event {procedureName: $name})
        CREATE (p)-[:CONTAINS]->(n)
    """
    with driver.session() as session:
        session.run(query, {"name": procedure_name})
    logger.info(f"Created Procedure node: {procedure_name}")


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

        import_nodes(driver, data["nodes"], data["procedureName"])
        import_edges(driver, data["edges"])
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
        # Import flow graph
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
                    props = json.loads(node["properties"])
                    if "State" in node.labels:
                        print(f"State: {node['entity']} in {props.get('state', 'N/A')}")
                    else:
                        print(f"Event: {node['entity']} - {props.get('eventType', 'N/A')}")

                # Print the flow with unique paths
                print("\nFlow:")
                flow = session.run("""
                    MATCH (p:Procedure {name: 'Initial Registration Procedure'})
                    MATCH (start)-[r:Action|Transition]->(end)
                    WHERE start.procedureName = p.name
                      AND end.procedureName = p.name
                    RETURN DISTINCT start.id as from, type(r) as rel_type, end.id as to
                    ORDER BY from, rel_type, to
                """)
                for record in flow:
                    props = {
                        'from': record['from'],
                        'rel_type': record['rel_type'],
                        'to': record['to']
                    }
                    print(f"{props['from']} -[{props['rel_type']}]-> {props['to']}")

            close_neo4j_connection(driver)

    except Exception as e:
        logger.error(f"Test connection failed: {e}")

    with open("output","r") as file:
        data = json.load(file)

        print(data)

