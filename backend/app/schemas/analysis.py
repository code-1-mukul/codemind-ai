from pydantic import BaseModel, Field


class ImportInfo(BaseModel):
    module: str = Field(..., description="Imported module name")


class FunctionInfo(BaseModel):
    name: str
    line_number: int
    docstring: str | None = None
    source_code: str | None = None


class ClassInfo(BaseModel):
    name: str
    line_number: int
    docstring: str | None = None
    source_code: str | None = None
    methods: list[FunctionInfo] = Field(default_factory=list)

class DependencyInfo(BaseModel):
    target: str
    relation: str

class CallInfo(BaseModel):
    caller: str
    callee: str
    line_number: int


class FileAnalysis(BaseModel):
    file_path: str
    imports: list[ImportInfo] = []
    functions: list[FunctionInfo] = []
    classes: list[ClassInfo] = []
    dependencies: list[DependencyInfo] = Field(default_factory=list)
    calls: list[CallInfo] = Field(default_factory=list)


class RepositoryAnalysis(BaseModel):
    repository_name: str
    files: list[FileAnalysis]