import sqlite3
from typing import List, Dict
import json

class ChunkDBHandler:
    def __init__(self, db_path="chunks.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Create the procedures table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nas_procedures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    procedure_name TEXT,
                    description TEXT,
                    steps JSON,  -- Store steps as JSON array
                    related_3gpp_spec_sections JSON,  -- Store sections as JSON array
                    source_document_title TEXT,
                    source_chunk_ids JSON,  -- Store chunk IDs as JSON array
                    doc_id TEXT,
                    similarity_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def store_nas_procedure(self, procedures: List[Dict], doc_id: str, similarity_score: float):
        """Store extracted NAS procedures in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for procedure in procedures:
                cursor.execute('''
                    INSERT INTO nas_procedures (
                        procedure_name, description, steps, 
                        related_3gpp_spec_sections, source_document_title,
                        source_chunk_ids, doc_id, similarity_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    procedure['procedure_name'],
                    procedure['description'],
                    json.dumps(procedure['steps']),
                    json.dumps(procedure['related_3gpp_spec_sections']),
                    procedure['source_document_title'],
                    json.dumps(procedure['source_chunk_ids']),
                    doc_id,
                    similarity_score
                ))
            conn.commit()

    def store_chunks(self, chunks: List[Dict], doc_id: str):
        """Store chunks in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Clear existing chunks for this document
            cursor.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
            
            # Insert new chunks
            for i, chunk in enumerate(chunks):
                cursor.execute('''
                    INSERT INTO chunks (title, content, level, doc_id, chunk_index)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    chunk['title'],
                    chunk['content'],
                    chunk['level'],
                    doc_id,
                    i
                ))
            conn.commit()
            return cursor.rowcount

    def get_chunks(self, doc_id: str) -> List[Dict]:
        """Retrieve chunks for a specific document"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, content, level, chunk_index 
                FROM chunks 
                WHERE doc_id = ? 
                ORDER BY chunk_index
            ''', (doc_id,))
            
            chunks = []
            for row in cursor.fetchall():
                chunks.append({
                    'title': row[0],
                    'content': row[1],
                    'level': row[2],
                    'index': row[3]
                })
            return chunks 

    def store_embedding_metadata(self, doc_id: str, metadata: Dict):
        """Store embedding metadata in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create metadata table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS embedding_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doc_id TEXT,
                    dimension INTEGER,
                    index_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO embedding_metadata (doc_id, dimension, index_path)
                VALUES (?, ?, ?)
            ''', (
                doc_id,
                metadata['dimension'],
                metadata['index_path']
            ))
            conn.commit() 