import faiss
import numpy as np
import os

class VectorStoreService:

    def __init__(self):

        self.index = None

    def create_index(self, dimension:int) -> None:
        # Create an faiss index for storing embedding vectors
        self.index = faiss.IndexFlatIP(dimension)

    def add_embeddings(self, embeddings: list[list[float]]) -> None:
        # Add embeddings to faiss index
        if self.index is None:
            raise ValueError("FAISS index has not been created")

        embeddings = np.array(embeddings,dtype=np.float32)

        self.index.add(embeddings)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> tuple[np.ndarray, np.ndarray]:
        #Search for the most similar embeddings in the FAISS index.

        if self.index is None:
            raise ValueError("FAISS index has not been created.")

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32,
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        return scores, indices

    def save(self, file_path: str) -> None:
        #Save the FAISS index to disk.

        if self.index is None:
            raise ValueError("No FAISS index to save.")

        faiss.write_index(self.index, file_path)

    def load(self, file_path: str) -> None:
        #Load a FAISS index from disk.


        self.index = faiss.read_index(file_path)

    

    
