from fastapi import APIRouter

from app.core.config import settings
from app.services.analysis_service import AnalysisService
from app.services.chunking_service import ChunkingService
from app.services.repository_service import RepositoryService
from app.services.indexing_service import IndexingService

router = APIRouter()

repository_service = RepositoryService()
analysis_service = AnalysisService()
chunking_service = ChunkingService()
indexing_service = IndexingService()


@router.get("/test-chunks/{repository_name}")
def test_chunks(repository_name: str):

    repository_path = repository_service.get_repository_path(
        repository_name,
        settings.UPLOAD_DIR,
    )

    analysis = analysis_service.analyze_repository(
        repository_name=repository_name,
        repository_path=repository_path
    )

    chunks = chunking_service.create_chunks(analysis)

    embedded_chunks = indexing_service.embed_chunks(repository_name,chunks)

    return {
        "repository": repository_name,
        "total_chunks": len(embedded_chunks),
        "embedding_dimension": len(
            embedded_chunks[0].embedding
        ),
        "first_chunk_name": embedded_chunks[0].chunk.name,
        "first_chunk_type": embedded_chunks[0].chunk.type,
        "first_10_embedding_values":
            embedded_chunks[0].embedding[:10],
    }