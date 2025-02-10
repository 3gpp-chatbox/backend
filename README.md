## Installation-and-run-locally

1. Clone the repository
```bash
    git clone <repository_url>
    cd rag-backend
```
2. Set Up a Virtual Environment:
```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```
3. Install dependencies
```bash
    pip install -r requirements.txt
``` 
4. Create config.py and include Gemini API key: 
```bash
    Gemini_API_KEY="your-gemini-api-key-here"
```
5. Run the Backend: 
```bash
    uvicorn main:app --reload
```