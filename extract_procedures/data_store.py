import json
import os
from typing import Dict, Any

class DataStore:
    def __init__(self, base_dir: str = "data"):
        """Initialize data storage"""
        self.base_dir = base_dir
        self._create_dirs()
        
    def _create_dirs(self):
        """Create directory structure"""
        directories = [
            'raw',           # Raw text from documents
            'preprocessed',   # Cleaned and structured text
            'entities',      # Extracted entities
            'relationships', # Extracted relationships
            'graphs'         # Graph data
        ]
        
        for dir_name in directories:
            dir_path = os.path.join(self.base_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
    
    def save_data(self, data: Any, category: str, filename: str):
        """Save data to appropriate directory"""
        file_path = os.path.join(self.base_dir, category, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def load_data(self, category: str, filename: str) -> Dict:
        """Load data from storage"""
        file_path = os.path.join(self.base_dir, category, filename)
        
        if not os.path.exists(file_path):
            return {}
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f) 