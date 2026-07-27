from app.services.embedding_service import EmbeddingService
from fastapi import APIRouter

embedding_service = EmbeddingService()

router = APIRouter()

@router.get("/test-embedding")
def test_embedding():

    vector = embedding_service.embed(
        "def add(a, b): return a + b"
    )

    return {
        "dimension": len(vector),
        "first_10_values": vector[:10],
    }