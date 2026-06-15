import os
import pickle
import numpy as np
import logging
from typing import List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)

class VectorStore:
    def __init__(self, dim: int = 384, store_file: str = "backend/data/vector_store.pkl"):
        self.dim = dim
        self.store_file = store_file
        self.embeddings_list = []
        self.metadata = []
        
        # Initialize the local HuggingFace embeddings model
        logging.info("Initializing HuggingFaceEmbeddings (all-MiniLM-L6-v2) locally...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(store_file), exist_ok=True)
        
        if os.path.exists(store_file):
            self.load()

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding locally using SentenceTransformers via LangChain."""
        return self.embeddings.embed_query(text)

    def add_vectors(self, texts: List[str], extra_data: List[dict] = None):
        """Generates embeddings and saves them in the vector store."""
        new_embeddings = [self.get_embedding(text) for text in texts]
        self.embeddings_list.extend(new_embeddings)
        self.metadata.extend(list(zip(texts, extra_data or [None]*len(texts))))
        self.save()
        logging.info("Added %d vectors to vector store", len(texts))

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """Calculates distance between query and stored vectors using pure NumPy."""
        if not self.embeddings_list:
            return []
        
        query_vec = np.array(self.get_embedding(query))
        embeddings_matrix = np.array(self.embeddings_list)
        
        # Calculate L2 distances (Euclidean Distance)
        diff = embeddings_matrix - query_vec
        distances = np.linalg.norm(diff, axis=1)
        
        # Sort indices by distance (ascending)
        top_indices = np.argsort(distances)[:k]
        
        results = []
        for idx in top_indices:
            if idx < len(self.metadata):
                results.append((self.metadata[idx][0], float(distances[idx])))
        return results

    def clear_store(self):
        """Clear the stored vectors and metadata."""
        self.embeddings_list = []
        self.metadata = []
        self.save()
        logging.info("Vector store cleared.")

    def save(self):
        """Saves embeddings and metadata using pickle."""
        data = {
            "embeddings": self.embeddings_list,
            "metadata": self.metadata
        }
        with open(self.store_file, "wb") as f:
            pickle.dump(data, f)
        logging.info("Saved vector store to %s", self.store_file)

    def load(self):
        """Loads embeddings and metadata from the pickle file."""
        try:
            with open(self.store_file, "rb") as f:
                data = pickle.load(f)
                self.embeddings_list = data.get("embeddings", [])
                self.metadata = data.get("metadata", [])
            logging.info("Loaded %d vectors from %s", len(self.embeddings_list), self.store_file)
        except Exception as e:
            logging.error("Failed to load vector store: %s", e)
            self.embeddings_list = []
            self.metadata = []