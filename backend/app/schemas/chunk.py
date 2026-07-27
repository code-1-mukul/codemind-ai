from pydantic import BaseModel


class CodeChunk(BaseModel):
    id: str
    type: str
    name: str
    file_path: str
    source_code: str
    docstring: str | None = None