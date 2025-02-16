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
- `nas_chunks.db` - SQLite database storing extracted procedures (auto-generated)

## Features

- Automated download of 3GPP specification documents
- Document processing and procedure extraction
- Graph-based analysis of procedures
- RESTful API endpoints for accessing the functionality
- Support for multiple 3GPP specifications (TS 24.501, TS 23.501, TS 23.502, TS 38.331, TS 24.301)
- SQLite database for storing extracted procedures and relationships

## Installation and Setup

1. Clone the repository
```bash
git clone <repository_url>
cd backend
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

## API Endpoints

The backend provides several endpoints for procedure extraction and analysis:

### Document Processing
- `POST /extract-procedures` - Upload and process a single .docx file
- `GET /process-directory/{dir_name}` - Process all .docx files in a specified directory

### Data Retrieval
- `GET /procedures` - Get all extracted procedures
- `GET /summary` - Get a detailed summary of extracted data
- `GET /view-database` - View all stored chunks and their extracted information

### System Status
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Database Structure

The system uses SQLite (`nas_chunks.db`) to store extracted procedures:

### Table: chunk_results
- `id` - Unique identifier
- `chunk_text` - Original text chunk
- `nodes` - Extracted nodes (JSON)
  - states
  - messages
  - procedures
  - entities
- `edges` - Relationships between nodes (JSON)

The database is automatically created when processing documents and is gitignored.

## Procedure Extraction

The system extracts several types of information:

1. **States**
   - REGISTERED
   - DEREGISTERED
   - IDLE
   - CONNECTED
   etc.

2. **Messages**
   - Registration Request
   - Authentication Request
   - Security Mode Command
   etc.

3. **Procedures**
   - Registration
   - Authentication
   - Security
   etc.

4. **Entities**
   - UE
   - AMF
   - AUSF
   etc.

## Usage Methods

There are two ways to use the procedure extraction functionality:

### 1. Direct Script Usage (Original Method)
Use `example_usage.py` to process documents directly:
```bash
cd extract_procedures
python example_usage.py
```
This method is good for:
- Quick testing
- Processing specific documents
- Development and debugging

### 2. API Usage (Enhanced Method)
Use the FastAPI endpoints through `main.py`:
```bash
uvicorn main:app --reload
```
This method provides:
- Web interface for document processing
- Multiple endpoints for different operations
- Easy integration with frontend applications
- Detailed data viewing options

Both methods use the same underlying `GraphExtractor` class and produce the same results.

## Development

### Regenerating the Database
The database can be regenerated at any time by:
1. Deleting the existing `nas_chunks.db`
2. Processing documents through the API endpoints
3. The database will be automatically recreated with fresh data

### Adding New Features
- Add new patterns in `graph_extractor.py`
- Extend API endpoints in `main.py`
- Update database schema as needed

## Notes

- Ensure sufficient disk space for downloaded 3GPP documents
- Some operations may require significant processing power
- API key is required for Gemini AI functionality
- Database files are not version controlled (in .gitignore)
- Temporary files are automatically cleaned up after processing

## Troubleshooting

1. **Empty Database**
   - Ensure documents are processed via API endpoints
   - Check console for processing errors
   - Verify document format (.docx)

2. **Processing Errors**
   - Check document formatting
   - Verify Spacy model installation
   - Check available memory

3. **API Connection Issues**
   - Verify server is running
   - Check CORS settings
   - Ensure correct port configuration