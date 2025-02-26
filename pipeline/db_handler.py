import sqlite3
from typing import List, Dict
import json
import chromadb
from sentence_transformers import SentenceTransformer

class DBHandler:
    def __init__(self, db_path: str = "DB/chunks.db", persist_directory: str = "DB/chroma_db"):
        """Initialize database and ChromaDB connections"""
        self.db_path = db_path
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.init_db()

    def init_db(self):
        """Create necessary tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create chunks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    level INTEGER,
                    doc_id TEXT,
                    chunk_index INTEGER,
                    embedding_collection TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(doc_id, chunk_index)
                )
            ''')
            
            # Create procedure metadata table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedure_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    procedure_name TEXT,
                    description TEXT,
                    steps_file TEXT,
                    related_3gpp_spec_sections JSON,
                    source_document_title TEXT,
                    source_chunk_ids JSON,
                    doc_id TEXT,
                    similarity_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def store_chunks(self, chunks: List[Dict], doc_id: str) -> int:
        """Store chunks and create embeddings"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
            
            for i, chunk in enumerate(chunks):
                cursor.execute('''
                    INSERT INTO chunks (title, content, level, doc_id, chunk_index, embedding_collection)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    chunk['title'],
                    chunk['content'],
                    chunk['level'],
                    doc_id,
                    i,
                    doc_id
                ))
            conn.commit()
            return cursor.rowcount

    def get_chunks(self, doc_id: str) -> List[Dict]:
        """Retrieve chunks for a document"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, content, level, chunk_index, embedding_collection
                FROM chunks 
                WHERE doc_id = ? 
                ORDER BY chunk_index
            ''', (doc_id,))
            
            return [{
                'title': row[0],
                'content': row[1],
                'level': row[2],
                'index': row[3],
                'collection': row[4]
            } for row in cursor.fetchall()]

    def create_embeddings(self, doc_id: str, model_name: str = "all-mpnet-base-v2") -> chromadb.Collection:
        """Create and store embeddings for chunks"""
        chunks = self.get_chunks(doc_id)
        if not chunks:
            raise ValueError("No chunks found for document")

        # Create or get collection
        try:
            collection = self.chroma_client.get_collection(doc_id)
            print(f"Using existing collection: {doc_id}")
        except:
            collection = self.chroma_client.create_collection(
                name=doc_id,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {doc_id}")

        # Prepare data for embedding
        ids = [str(chunk['index']) for chunk in chunks]
        texts = [f"{chunk['title']} {chunk['content']}".strip() for chunk in chunks]
        metadatas = [{
            'title': chunk['title'],
            'level': chunk['level'],
            'index': chunk['index']
        } for chunk in chunks]

        # Add documents in batches
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch_end = min(i + batch_size, len(texts))
            collection.add(
                ids=ids[i:batch_end],
                documents=texts[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )

        return collection 

    def store_procedure_metadata(self, metadata: Dict):
        """Store procedure metadata in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO procedure_metadata (
                    procedure_name, description, steps_file,
                    related_3gpp_spec_sections, source_document_title,
                    source_chunk_ids, doc_id, similarity_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metadata['procedure_name'],
                metadata['description'],
                metadata['steps_file'],
                json.dumps(metadata['related_3gpp_spec_sections']),
                metadata['source_document_title'],
                json.dumps(metadata['source_chunk_ids']),
                metadata['doc_id'],
                metadata['similarity_score']
            ))
            conn.commit()

# Keep old class for backward compatibility
class ChunkDBHandler(DBHandler):
    def __init__(self, db_path="chunks.db"):
        super().__init__(db_path=db_path) 