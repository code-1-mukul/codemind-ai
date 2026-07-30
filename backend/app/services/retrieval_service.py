from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.metadata_service import MetadataService
import numpy as np
from pathlib import Path
from app.core.config import settings


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.metadata_service = MetadataService()

    def search(
        self,
        repository_name: str,
        query: str,
        top_k: int = 5,
        ):
            #Perform semantic search over the indexed repository.
            
            # Generate embedding for the query
            query_embedding = self.embedding_service.embed(query)

            index_path = (
                Path(settings.FAISS_STORAGE_DIR)
                / f"{repository_name}.index"
            )

            self.vector_store_service.load(str(index_path))

            # Search the vector index
            distances, indices = self.vector_store_service.search(
                query_embedding=query_embedding,
                top_k=top_k,
            )

            # Retrieve metadata
            results = []

            for score, chunk_id in zip(
                distances[0],
                indices[0],
            ):

                if chunk_id == -1:
                    continue

                entry = self.metadata_service.get_chunk_by_id(
                    repository_name,
                    int(chunk_id),
                )

                if entry is None:
                    continue

                results.append(
                    {
                        "score": float(score),
                        "file_path": entry.chunk.file_path,
                        "chunk_type": entry.chunk.type,
                        "chunk_name": entry.chunk.name,
                        "content": entry.chunk.source_code,
                    }
                )

            return {
                "query": query,
                "results": results,
            }