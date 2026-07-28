from pydantic import BaseModel

from app.schemas.chunk import CodeChunk


class EmbeddedChunk(BaseModel):
    chunk: CodeChunk
    embedding: list[float]