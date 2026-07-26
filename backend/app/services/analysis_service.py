from pathlib import Path

from app.parsers.parser import ParserService
from app.schemas.analysis import RepositoryAnalysis


class AnalysisService:

    def __init__(self):
        self.parser = ParserService()

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

        return analysis