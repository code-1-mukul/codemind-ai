from pydantic import BaseModel, Field
from typing import List


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")


class SearchResult(BaseModel):
    score: float
    file_path: str
    chunk_type: str
    chunk_name: str
    content: str


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]