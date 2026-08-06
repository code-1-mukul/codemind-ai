from app.schemas.embedding import EmbeddedChunk
from app.schemas.chunk import CodeChunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.metadata_service import MetadataService
from pathlib import Path
from app.core.config import settings

class IndexingService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.metadata_service = MetadataService()

    def embed_chunks(
        self,
        repository_name:str,
        chunks: list[CodeChunk],
    ) -> list[EmbeddedChunk]:

        embedded_chunks = []

        texts = [
            chunk.source_code
            for chunk in chunks
        ]

        print("Started embdeddings...")

        embeddings = self.embedding_service.embed_batch(
            texts
        )

        print("Embeddings completed.")

        dimension = len(embeddings[0])

        self.vector_store.create_index(dimension)

        self.vector_store.add_embeddings(embeddings)

        Path(settings.FAISS_STORAGE_DIR).mkdir(
            parents=True,
            exist_ok=True,
        )

        index_path = (
            Path(settings.FAISS_STORAGE_DIR)
            / f"{repository_name}.index"
        )

        self.vector_store.save(str(index_path))

        embedded_chunks = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):

            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=embedding,
                )
            )

        self.metadata_service.save_metadata(
                    repository_name,
                    embedded_chunks,
        )

        return embedded_chunks