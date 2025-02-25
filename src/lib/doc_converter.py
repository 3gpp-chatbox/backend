import logging
import os
from docling.document_converter import DocumentConverter, ConversionError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def convert_to_markdown(source_path):
    """
    Convert a document to markdown format.

    Args:
        source_path (str): Path to the source document

    Returns:
        str: Path to the generated markdown file

    Raises:
        FileNotFoundError: If source file doesn't exist
        ConversionError: If document conversion fails
        IOError: If file operations fail
        Exception: For other unexpected errors
    """
    if not os.path.exists(source_path):
        msg = f"Source file not found: {source_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Generate output path by replacing .docx extension with .md
    output_path = os.path.splitext(source_path)[0] + ".md"

    converter = None
    try:
        # Convert the document
        converter = DocumentConverter()
        logger.info(f"Converting document: {source_path}")
        result = converter.convert(source_path)

        # Write the markdown content to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.document.export_to_markdown())

        logger.info(f"Successfully created markdown file: {output_path}")
        return output_path

    except ConversionError as e:
        msg = f"Document conversion failed: {str(e)}"
        logger.error(msg)
        raise
    except IOError as e:
        msg = f"I/O error during conversion: {str(e)}"
        logger.error(msg)
        raise
    except Exception as e:
        msg = f"Unexpected error during conversion: {str(e)}"
        logger.error(msg)
        raise


# Example usage
if __name__ == "__main__":
    source = "data/24501-j11.docx"
    try:
        output_file = convert_to_markdown(source)
        print(f"Markdown file created at: {output_file}")
    except (FileNotFoundError, ConversionError, IOError) as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
