# Project Workflow

## 1. Pipeline Directory

### Document Preprocessing
- **Convert Documents**: Convert DOCX and PDF documents to Markdown format for easier text manipulation.
- **Clean Text**: Normalize whitespace, remove extraneous punctuation, and standardize text casing to ensure consistency.

### Chunking
- **Document-Based Chunking**: Split the text into meaningful units based on document structure.
- **Semantic Chunking**: Further divide the text into contextually meaningful units using semantic analysis techniques.

## 2. Extracting Information with `extract.py`

### Data Extraction
- **Initialize Language Model**: Use a language model (e.g., Gemini 2.0 Flash) to process semantic chunks.
- **Extract Procedures**: Retrieve relevant chunks and extract detailed information about 5G network registration procedures.
- **Validate and Structure Data**: Use Pydantic models to validate and structure the extracted data for consistency and accuracy.

### Error Handling
- **Robust Error Management**: Implement try-except blocks to handle exceptions and ensure smooth processing.
- **Logging**: Use structured logging to track data extraction and processing steps for transparency and debugging.

## 3. Storing Data in Neo4j

### Graph Construction
- **Generate Nodes and Edges**: Create nodes representing network elements and states, and edges representing relationships and transitions.
- **Use Neo4j**: Store the graph data in Neo4j, enabling complex queries and analysis of relationships.

### Data Storage & Visualization
- **Store Structured Data**: Save the structured data in JSON format for easy access and manipulation.
- **Visualize with Mermaid.js**: Convert the graph data into visual flowcharts using Mermaid.js for clear and intuitive presentation.

### Database Management
- **Ensure APOC Availability**: Verify that APOC procedures are available in the Neo4j instance for enhanced graph operations.
- **Batch Operations**: Use batch processing to efficiently store large volumes of data in Neo4j.

---

This workflow outlines the sequential steps from document preprocessing to data extraction and storage in Neo4j, providing a clear and organized view of the project's processes. 