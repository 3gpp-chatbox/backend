from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

class TextChunker:
    def __init__(self, model_name="all-MiniLM-L6-v2", n_clusters=5):
        self.model = SentenceTransformer(model_name)
        self.n_clusters = n_clusters

    def chunk_text(self, text: str):
        # Split text into sentences
        sentences = [sent.strip() for sent in text.split('.') if sent.strip()]

        # Generate embeddings for each sentence
        embeddings = self.model.encode(sentences)

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(embeddings)

        # Group sentences by cluster
        clustered_chunks = {i: [] for i in range(self.n_clusters)}
        for idx, cluster_id in enumerate(clusters):
            clustered_chunks[cluster_id].append(sentences[idx])

        # Combine sentences in each cluster into text chunks
        chunks = [" ".join(clustered_chunks[i]) for i in range(self.n_clusters)]

        return chunks

