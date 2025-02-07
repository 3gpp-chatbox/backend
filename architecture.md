your_project/
│── data/                        # Folder containing 6 PDF files
│── backend/                      # Backend-related files
│   ├── preprocess_pdfs.py        # Extract text & preprocess PDFs
│   ├── store_data_chroma.py      # Store preprocessed data in ChromaDB
│   ├── store_data_faiss.py       # Store preprocessed data in FAISS
│   ├── store_knowledge_graph.py  # Store data in Neo4j (if using a KG)
│   ├── query_data.py             # Search/query from stored database
│   ├── app.py                    # Flask/FastAPI backend (for frontend)
│── frontend/                     # React frontend
│── requirements.txt               # Python dependencies
│── README.md                      # Project documentation
