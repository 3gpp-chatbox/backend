# src/lib/store_chunks.py
from typing import List
from src.lib.doc_processor import Section
from src.db import db
from src.lib.logger import get_logger

logger = get_logger(__name__)


def build_ltree_path(section: Section) -> str:
    """
    Build the ltree path for a section by traversing up through its parents.
    The path is built from the top level down to the current section.
    """
    path_parts = []
    current = section
    while current is not None:
        # Clean the heading to be ltree compatible (only alphanumeric and underscore)
        clean_heading = "".join(c for c in current.heading if c.isalnum() or c == "_")
        path_parts.insert(0, clean_heading)
        current = current.parent
    return ".".join(path_parts)


def store_section_recursive(
    cur, doc_id: str, section: Section, parent_heading: str = None
):
    """
    Recursively store a section and its subsections in the database.
    """
    # Join the content list into a single string
    content_text = " ".join(section.content) if section.content else ""

    # Build the ltree path for this section
    path = build_ltree_path(section)

    # Insert the current section
    query = """
        INSERT INTO sections (doc_id, heading, level, content, parent, path)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(
        query,
        (
            doc_id,
            section.heading,
            section.level,
            content_text,
            parent_heading or "root",
            path,
        ),
    )

    # Recursively store all subsections
    for subsection in section.subsections:
        store_section_recursive(cur, doc_id, subsection, section.heading)


def store_chunks(sections_tree: List[Section], doc_name: str, toc: str, doc_id: str):
    """
    Store the document sections in the database.

    Args:
        sections_tree (List[Section]): List of Section objects representing the document structure
        doc_name (str): Name of the document
    """
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()

        # Check if the document already exists in the database
        cur.execute("SELECT doc_id FROM documents WHERE doc_id = %s", (doc_id,))
        existing_doc = cur.fetchone()

        if existing_doc:
            logger.info(f"Document {doc_id} already exists in the database")
            # Delete existing sections for this document
            cur.execute("DELETE FROM sections WHERE doc_id = %s", (doc_id,))
            logger.info(f"Deleted existing sections for document {doc_id}")
        else:
            logger.info(f"Storing new document {doc_id} in the database")
            # Insert new document
            cur.execute(
                "INSERT INTO documents (doc_id, doc_name, toc) VALUES (%s, %s, %s)",
                (doc_id, doc_name, toc),
            )

        # Store each top-level section and its subsections
        for section in sections_tree:
            store_section_recursive(cur, doc_id, section)

        # Commit the transaction
        conn.commit()
        logger.info(
            f"Successfully stored document {doc_name} with {len(sections_tree)} top-level sections"
        )
        for section in sections_tree:
            logger.debug(f"Top-level section: {section.heading}")

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error storing chunks: {str(e)}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
