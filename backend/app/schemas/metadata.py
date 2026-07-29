from pydantic import BaseModel

from app.schemas.chunk import CodeChunk


class MetadataEntry(BaseModel):
    id: int
    chunk: CodeChunk


class MetadataFile(BaseModel):
    entries: list[MetadataEntry]