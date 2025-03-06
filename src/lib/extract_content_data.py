from src.db import db_connection
from src.lib.logger import get_logger

logger = get_logger(__name__)


def generate_markdown(doc_id: str, target_headings: list[str]) -> str:
    """Generate a markdown document from specified document sections.

    This function retrieves sections from a document based on given headings and their subheadings,
    and formats them into a markdown string. It maintains the hierarchical structure of the sections
    using markdown heading syntax.

    Args:
        doc_id (int): The unique identifier of the document to extract sections from.
        target_headings (list[str]): A list of heading strings to extract, along with their
            subsections. Each heading should match exactly with the stored heading in the database.

    Returns:
        str: A formatted markdown string containing the requested sections with proper heading
            levels and content. If no matching sections are found, returns an error message.

    Raises:
        Exception: If there's any database error during the extraction process. The specific
            exception details are logged before being re-raised.

    """
    logger.info(
        f"Generating markdown for doc_id={doc_id}, target_headings={target_headings}"
    )
    try:
        conn = db_connection.get_db_connection()
        cur = conn.cursor()

        # Step 1: Check if the document exists
        cur.execute("SELECT * FROM documents WHERE doc_id = %s", (doc_id,))

        result = cur.fetchone()
        if not result:
            logger.error(f"Document {doc_id} not found in the database")
            return f"Document {doc_id} not found in the database"

        doc_name = result.get("doc_name")

        # Step 2: Get all target paths for the given headings
        cur.execute(
            "SELECT heading, path FROM sections WHERE doc_id = %s AND heading = ANY (%s)",
            (doc_id, target_headings),
        )
        results = cur.fetchall()

        if not results:
            logger.warning(f"No headings {target_headings} found in document {doc_id}")
            return f"No headings {target_headings} found in document {doc_id}"

        target_paths: list[str] = [result.get("path") for result in results]
        logger.debug(f"Found target paths: {target_paths}")

        # Step 3: Get all sections under these paths
        # Modify the query to use <@ ANY for multiple paths
        cur.execute(
            """
            SELECT heading, level, content
            FROM sections
            WHERE doc_id = %s AND path <@ ANY (%s)
            ORDER BY path
            """,
            (doc_id, target_paths),
        )
        sections = cur.fetchall()
        logger.debug(f"Found {len(sections)} sections under paths {target_paths}")

        # Step 4: Generate markdown
        markdown_lines: list[str] = []

        # Define document title in the markdown
        markdown_lines.append(f"# {doc_name}")
        markdown_lines.append("")  # Blank line after title

        # Iterate over sections and create markdown
        for section in sections:
            heading: str = section.get("heading")
            level: int = section.get("level")
            content: str | None = section.get("content")
            # Create markdown heading
            heading_md = "#" * (level + 1) + " " + heading
            markdown_lines.append(heading_md)
            # markdown_lines.append("")  # Blank line after heading
            if content:
                markdown_lines.append(content.strip())
                markdown_lines.append("")  # Blank line after content

        result = "\n".join(markdown_lines).strip()  # Remove trailing newlines
        logger.info(f"Successfully generated markdown with {len(markdown_lines)} lines")
        return result

    except Exception as e:
        logger.error(f"Error generating markdown: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()


# Example usage
# markdown = generate_markdown(doc_id=1, target_heading="4_general")
if __name__ == "__main__":
    markdown = generate_markdown(
        doc_id=1,
        target_headings=[
            "4_general",
            "5_elementary_procedures_for_5GS_mobility_management",
        ],
    )
    print(markdown)
