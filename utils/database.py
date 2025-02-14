from typing import Optional
from neo4j import GraphDatabase
from chromadb import Client
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self._uri = os.getenv("NEO4J_URI")
        self._user = os.getenv("NEO4J_USERNAME")
        self._password = os.getenv("NEO4J_PASSWORD")
        self._driver = None

    def connect(self):
        if not self._driver:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password)
            )
        return self._driver

class ChromaDBConnection:
    def __init__(self):
        self._client: Optional[Client] = None
        self._collection_name = "3gpp_nas_specs"

    def connect(self):
        if not self._client:
            self._client = Client()
        return self._client

    def get_collection(self):
        client = self.connect()
        return client.get_or_create_collection(self._collection_name) 