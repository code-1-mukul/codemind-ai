import json
from pathlib import Path

from app.core.config import settings
from app.schemas.analysis import RepositoryAnalysis


class AnalysisStorageService:

    def save_analysis(
        self,
        analysis: RepositoryAnalysis,
    ):

        storage_dir = Path(settings.ANALYSIS_STORAGE_DIR)

        storage_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            storage_dir
            / f"{analysis.repository_name}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                analysis.model_dump(),
                file,
                indent=4,
                ensure_ascii=False,
            )

    def load_analysis(
            self,
            repository_name:str,
    ) -> RepositoryAnalysis:

        storage_dir = Path(settings.ANALYSIS_STORAGE_DIR)

        file_path = storage_dir/f"{repository_name}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Analysis not found for repository: {repository_name}")
        with open(file_path,"r",encoding="utf-8") as file:
            data = json.load(file)

        return RepositoryAnalysis.model_validate(data)