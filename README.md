# 3GPP Document Analysis Backend

This backend system is designed to download, process, and analyze 3GPP specification documents. It includes functionality for document downloading, procedure extraction, and graph-based analysis of 3GPP procedures.

## Project Structure

- `main.py` - FastAPI backend server implementation
- `download_3gpp_docs.py` - Script for downloading and managing 3GPP specification documents
- `extract_procedures/` - Module for extracting and analyzing procedures from 3GPP documents
  - `graph_extractor.py` - Implements procedure extraction and graph generation
  - `example_usage.py` - Examples of using the extraction functionality
- `3GPP_Documents/` - Directory where downloaded specifications are stored
- `requirements.txt` - Project dependencies

## Features

- Automated download of 3GPP specification documents
- Document processing and procedure extraction
- Graph-based analysis of procedures
- RESTful API endpoints for accessing the functionality
- Support for multiple 3GPP specifications (TS 24.501, TS 23.501, TS 23.502, TS 38.331, TS 24.301)

## Installation and Setup

1. Clone the repository
```bash
git clone <repository_url>
cd rag-backend
```

2. Set Up a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Install Spacy Language Model:
```bash
python -m spacy download en_core_web_sm
```

5. Create config.py and include Gemini API key: 
```bash
Gemini_API_KEY="your-gemini-api-key-here"
```

6. Download 3GPP Documents (Optional):
```bash
python download_3gpp_docs.py
```

7. Run the Backend: 
```bash
uvicorn main:app --reload
```

## Dependencies

Key dependencies include:
- FastAPI - Backend framework
- PyMuPDF - PDF handling
- Spacy - Natural language processing
- Sentence-transformers - Text embeddings
- Networkx - Graph processing
- Google Generative AI - For advanced text processing
- Various other data processing and machine learning libraries

## Usage

1. First, ensure all 3GPP documents are downloaded using the download script
2. Start the backend server
3. Use the API endpoints to:
   - Access document content
   - Extract procedures
   - Generate and analyze procedure graphs
   - Query document information

## Development

The project uses modern Python practices and includes:
- Type hints for better code maintainability
- Modular design for easy extension
- Comprehensive documentation
- Error handling for robust operation

## Notes

- Ensure sufficient disk space for downloaded 3GPP documents
- Some operations may require significant processing power
- API key is required for Gemini AI functionality