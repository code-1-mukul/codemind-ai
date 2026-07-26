from collections import Counter
from pathlib import Path

from app.schemas.summary import LargestFile, RepositorySummary
from app.services.scanner_service import ScannerService


class SummaryService:

    @classmethod
    def generate_summary(cls, repository_path: str):

        repository = Path(repository_path)

        files = ScannerService.scan_repository(repository_path)

        total_files = len(files)

        total_directories = sum(
            1
            for path in repository.rglob("*")
            if path.is_dir()
            and path.name not in ScannerService.IGNORE_DIRS
        )

        total_size = sum(file.size for file in files)

        language_counter = Counter(file.language for file in files)

        largest = max(files, key=lambda file: file.size)

        return RepositorySummary(
            repository=repository.name,
            total_files=total_files,
            total_directories=total_directories,
            total_size=total_size,
            languages=dict(language_counter),
            largest_file=LargestFile(
                name=largest.name,
                size=largest.size,
            ),
        )