import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from src.lib.logger import get_logger


logger = get_logger(__name__)

# Load environment variables
load_dotenv(override=True)


def get_db_connection():
    """Create a database connection using environment variables."""
    try:
        logger.info("Attempting to connect to database...")
        conn_string = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_USER')} "
            f"password={os.getenv('DB_PASSWORD')} "
            f"port={os.getenv('DB_PORT', '5432')}"
        )
        connection = psycopg.connect(conn_string, row_factory=dict_row)
        logger.info("Successfully connected to database")
        return connection
    except psycopg.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def close_connection(connection):
    """Close the database connection."""
    if connection is not None:
        logger.info("Closing database connection")
        connection.close()


# Test the connection if this file is run directly
if __name__ == "__main__":
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Test basic query
                cur.execute("SELECT 1")

                doc_name = "test_doc"
                # Test insert
                cur.execute(
                    "INSERT INTO documents (doc_name) VALUES (%s) RETURNING doc_id",
                    (doc_name,),
                )
                conn.commit()
                logger.info("Database test query successful")
    except Exception as e:
        logger.error(f"Test connection failed: {e}")
