import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv(override=True)

def get_db_connection():
    """Create a database connection using environment variables."""
    try:
        logging.info("Attempting to connect to database...")
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432'),
            cursor_factory=RealDictCursor
        )
        logging.info("Successfully connected to database")
        return connection
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def close_connection(connection):
    """Close the database connection."""
    if connection is not None:
        logging.info("Closing database connection")
        connection.close()

# Test the connection if this file is run directly
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        doc_name = "lala"
        cur.execute(
            "INSERT INTO documents (doc_name) VALUES (%s) RETURNING doc_id",
            (doc_name,)
        )
        conn.commit()
        logging.info("Database test query successful")
    except Exception as e:
        logging.error(f"Test connection failed: {e}")
    finally:
        if cur:
            cur.close()
        close_connection(conn)
