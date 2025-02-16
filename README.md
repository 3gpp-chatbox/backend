# 3GPP Document Analysis Backend

This project provides a backend system for analyzing and querying 3GPP technical specification documents using vector databases and knowledge graphs.

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
- Vector database storage using ChromaDB
- Knowledge graph storage using Neo4j
- Flexible querying interface
- FastAPI backend for frontend integration

## Prerequisites

- Python 3.8+
- Neo4j Database (for knowledge graph storage)
- ChromaDB (for vector storage)

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

4. To deactivate the virtual environment when you're done:
   ```bash
   deactivate
   ```

## Environment Setup

Create a `.env` file in the root directory with the following configurations:

```env
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
CHROMA_PERSIST_DIRECTORY=path_to_chroma_storage
```

## Usage

1. **Preprocess PDFs**:
   ```bash
   python preprocess_pdfs.py
   ```

2. **Extract Entities**:
   ```bash
   python extract_3gpp_entities.py
   ```

3. **Store Data**:
   ```bash
   python store_data_chroma.py  # For vector database
   python store_data_neo4j.py   # For knowledge graph
   ```

4. **Query Data**:
   ```bash
   python query_data.py
   ```

5. **Run the API**:
   ```bash
   uvicorn app:app --reload
   ```

## API Endpoints

The FastAPI backend provides several endpoints for querying and retrieving information. Access the API documentation at `http://localhost:8000/docs` when running the server.

## Neo4j Queries

For detailed Neo4j query examples and patterns, refer to `neo4j_queries.md`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.