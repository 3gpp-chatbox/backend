import sqlite3
from typing import Dict, List, Optional
import json
from pydantic import BaseModel

class ProcedureMetadata(BaseModel):
    References: List[str]

class Procedure(BaseModel):
    procedure_name: str
    category: str
    metadata: ProcedureMetadata

class DBHandler:
    def __init__(self, db_path: str = "DB/procedures.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database with taxonomy tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedure_category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedure (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER REFERENCES procedure_category(id) ON DELETE CASCADE,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedure_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    procedure_id INTEGER REFERENCES procedure(id) ON DELETE CASCADE,
                    ref_sections TEXT NOT NULL
                )
            ''')
            conn.commit()

    def store_procedure(self, procedure: Procedure):
        """Store a procedure with its metadata"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Insert procedure category if it doesn't exist
            cursor.execute('''
                INSERT OR IGNORE INTO procedure_category (name) VALUES (?)
            ''', (procedure.category,))

            # Get the category ID
            cursor.execute('SELECT id FROM procedure_category WHERE name = ?', (procedure.category,))
            category_id = cursor.fetchone()[0]

            # Insert procedure
            cursor.execute('''
                INSERT OR IGNORE INTO procedure (category_id, name) VALUES (?, ?)
            ''', (category_id, procedure.procedure_name))

            # Get the procedure ID
            cursor.execute('SELECT id FROM procedure WHERE name = ?', (procedure.procedure_name,))
            procedure_id = cursor.fetchone()[0]

            # Insert metadata
            cursor.execute('''
                INSERT OR REPLACE INTO procedure_metadata (
                    procedure_id, ref_sections
                ) VALUES (?, ?)
            ''', (
                procedure_id,
                json.dumps(procedure.metadata.References)
            ))

            conn.commit()

    def get_procedures(self, category: Optional[str] = None) -> List[Procedure]:
        """Retrieve procedures with optional category filter"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Base query
            query = '''
                SELECT 
                    pc.name as category,
                    p.name as procedure_name,
                    m.ref_sections
                FROM procedure p
                JOIN procedure_category pc ON p.category_id = pc.id
                JOIN procedure_metadata m ON p.id = m.procedure_id
            '''
            params = ()
            if category:
                query += " WHERE pc.name = ?"
                params = (category,)

            query += " ORDER BY pc.name, p.name"

            cursor.execute(query, params)
            procedures = []
            for row in cursor.fetchall():
                try:
                    references = json.loads(row[2])
                except (json.JSONDecodeError, TypeError):
                    references = []

                procedures.append(Procedure(
                    procedure_name=row[1],
                    category=row[0],
                    metadata=ProcedureMetadata(References=references)
                ))

            return procedures