from fastapi import APIRouter

from app.schemas.retrieval import (
    SearchRequest,
    SearchResponse,
)
from app.services.retrieval_service import RetrievalService

router = APIRouter()

retrieval_service = RetrievalService()

@router.post(
    "/{repository_name}/search",
    response_model=SearchResponse,
)
def search_repository(
    repository_name: str,
    request: SearchRequest,
    ):
        """
        Perform semantic search on an indexed repository.
        """

        results = retrieval_service.search(
            repository_name=repository_name,
            query=request.query,
            top_k=request.top_k,
        )

        return results