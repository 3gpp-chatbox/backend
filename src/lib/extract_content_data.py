import logging
from src.db import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_markdown(doc_id: int, target_heading: str) -> str:
    logger.info(f"Generating markdown for doc_id={doc_id}, target_heading='{target_heading}'")
    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        # Step 1: Get the target path
        cur.execute(
            "SELECT path FROM sections WHERE doc_id = %s AND heading = %s",
            (doc_id, target_heading)
        )
        result = cur.fetchone()
        if not result:
            logger.warning(f"Heading '{target_heading}' not found in document {doc_id}")
            return f"Heading '{target_heading}' not found in document {doc_id}"

        target_path = result.get("path")
        logger.debug(f"Found target path: {target_path}")

        # Step 2: Get all sections under this path
        cur.execute(
            """
            SELECT heading, level, content
            FROM sections
            WHERE path <@ %s AND doc_id = %s
            ORDER BY path
            """,
            (target_path, doc_id)
        )
        sections = cur.fetchall()
        logger.debug(f"Found {len(sections)} sections under path {target_path}")

        # Step 3: Generate markdown
        markdown_lines = []
        for section in sections:
            heading = section.get("heading")
            level = section.get("level")
            content = section.get("content")
            # Create markdown heading (e.g., "## 4_1_general")
            heading_md = "#" * level + " " + heading
            markdown_lines.append(heading_md)
            markdown_lines.append("")  # Blank line after heading
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
markdown = generate_markdown(doc_id=1, target_heading="4_general")
print(markdown)
