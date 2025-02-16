# 3GPP Document Analysis Backend

This project provides a backend system for analyzing and querying 3GPP technical specification documents using vector databases (ChromaDB) and knowledge graphs (Neo4j).

## Project Overview

This system processes 3GPP technical specification PDFs and stores their content in both vector databases (ChromaDB) and graph databases (Neo4j) for efficient querying and knowledge extraction. It includes capabilities for document preprocessing, entity extraction, and various querying methods.

## Directory Structure

```
├── data/                      # Contains 3GPP specification PDFs
│   └── TS*.pdf               # Various 3GPP technical specifications
├── utils/                     # Utility functions and helpers
│   ├── validator.py          # Data validation utilities
│   ├── database.py          # Database connection handlers
│   ├── preprocessing.py      # Text preprocessing utilities
│   ├── query_interface.py    # Query interface implementations
│   └── refined_extractor.py  # Enhanced entity extraction
├── app.py                    # FastAPI backend application
├── extract_3gpp_entities.py  # Main entity extraction script
├── preprocess_pdfs.py        # PDF preprocessing script
├── store_data_chroma.py      # ChromaDB data storage
├── store_data_neo4j.py       # Neo4j data storage
├── query_data.py             # Data querying interface
└── requirements.txt          # Project dependencies
```

## Features

- PDF document preprocessing and text extraction
- Entity extraction from 3GPP specifications
- Vector database storage using ChromaDB for semantic search
- Knowledge graph storage using Neo4j for relationship queries
- Flexible querying interface
- FastAPI backend for frontend integration

## Prerequisites

- Python 3.8+
- Neo4j Database (for knowledge graph storage)
- ChromaDB (for vector storage)
- Google API Key (for embeddings generation)

## Installation

1. Clone the repository

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

1. Create a `.env` file in the root directory with the following configurations:
   ```env
   # Neo4j Configuration
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password_here

   # ChromaDB Configuration
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   
   # Google API for embeddings
   GOOGLE_API_KEY=your_google_api_key_here
   ```

2. Set up Neo4j:
   - Download and install [Neo4j Desktop](https://neo4j.com/download/)
   - Create a new database
   - Start the database
   - Make sure the credentials match your `.env` file

## Usage

The system requires a specific order of operations:

1. **Store Document Embeddings in ChromaDB**:
   ```bash
   python store_data_chroma.py
   ```
   This creates vector embeddings of your documents for semantic search.

2. **Extract and Store Entities in Neo4j**:
   ```bash
   python extract_3gpp_entities.py
   ```
   This extracts entities and relationships from the documents and stores them in Neo4j.

3. **Query Data** (after both storage steps are complete):
   ```bash
   python query_data.py
   ```

4. **Run the API**:
   ```bash
   uvicorn app:app --reload
   ```
   Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

The FastAPI backend provides several endpoints for querying and retrieving information. Access the API documentation at `http://localhost:8000/docs` when running the server.

## Neo4j Queries

For detailed Neo4j query examples and patterns, refer to `neo4j_queries.md`.

## Troubleshooting

1. **Neo4j Connection Issues**:
   - Ensure Neo4j is running
   - Verify credentials in `.env`
   - Check if port 7687 is accessible

2. **ChromaDB Issues**:
   - Verify Google API key is valid
   - Check CHROMA_PERSIST_DIRECTORY exists
   - Ensure enough disk space for embeddings

3. **PDF Processing Issues**:
   - Verify PDFs are in the data directory
   - Check PDF file permissions
   - Ensure PDFs are valid and not corrupted

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.