from pydantic import BaseModel


class LargestFile(BaseModel):
    name: str
    size: int


class RepositorySummary(BaseModel):
    repository: str
    total_files: int
    total_directories: int
    total_size: int
    languages: dict[str, int]
    largest_file: LargestFile