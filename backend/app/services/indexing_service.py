from app.schemas.embedding import EmbeddedChunk
from app.schemas.chunk import CodeChunk
from app.services.embedding_service import EmbeddingService


class IndexingService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> list[EmbeddedChunk]:

        embedded_chunks = []

        for chunk in chunks:

            embedding = self.embedding_service.embed(
                chunk.source_code
            )

            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=embedding,
                )
            )

        return embedded_chunks