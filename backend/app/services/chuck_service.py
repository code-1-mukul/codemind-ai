from app.schemas.analysis import RepositoryAnalysis
from app.schemas.chunk import CodeChunk


class ChunkingService:

    def create_chunks(
        self,
        analysis: RepositoryAnalysis,
    ) -> list[CodeChunk]:

        chunks = []

        for file in analysis.files:
            for class_info in file.classes:
                chunks.append(
                    CodeChunk(
                        id=f"{file.file_path}:{class_info.name}",
                        type="class",
                        name=class_info.name,
                        file_path=file.file_path,
                        source_code=class_info.source_code,
                        docstring=class_info.docstring,
                    )
                )

            for function_info in file.functions:
                chunks.append(
                    CodeChunk(
                        id=f"{file.file_path}:{function_info.name}",
                        type="function",
                        name=function_info.name,
                        file_path=file.file_path,
                        source_code=function_info.source_code,
                        docstring=function_info.docstring,
                    )
                )

        return chunks