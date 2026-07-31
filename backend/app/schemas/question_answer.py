from pydantic import BaseModel
from typing import List


class AskRequest(BaseModel):
    repository_name: str
    question: str


class SourceChunk(BaseModel):
    score: float
    file_path: str
    chunk_type: str
    chunk_name: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceChunk]