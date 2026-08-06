from pathlib import Path

from app.parsers.parser import ParserService
from app.schemas.analysis import RepositoryAnalysis
from app.services.chunking_service import ChunkingService
from app.services.indexing_service import IndexingService


class AnalysisService:

    def __init__(self):
        self.parser = ParserService()
        self.chunking_service = ChunkingService()
        self.indexing_service = IndexingService()

    def analyze_repository(
        self,
        repository_name: str,
        repository_path: Path,
    ) -> RepositoryAnalysis:

        analysis = RepositoryAnalysis(
            repository_name=repository_name,
            files=[],
        )

        for file_path in repository_path.rglob("*"):

            if not file_path.is_file():
                continue

            if file_path.suffix != ".py":
                continue

            try:
                file_analysis = self.parser.parse(file_path)
                analysis.files.append(file_analysis)

            except Exception as e:
                print(f"Skipping {file_path}: {e}")

        chunks = self.chunking_service.create_chunks(
            analysis
        )

        print(f"Number of chunks: {len(chunks)}")

        self.indexing_service.embed_chunks(
            repository_name=repository_name,
            chunks=chunks,
        )

        return analysis