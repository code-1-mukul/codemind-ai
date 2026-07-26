from pydantic import BaseModel


class FileMetadata(BaseModel):
    name: str
    path: str
    extension: str
    size: int
    language: str