from pathlib import Path

from app.schemas.file import FileMetadata


class ScannerService:

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "React",
        ".tsx": "React TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".md": "Markdown",
        ".yml": "YAML",
        ".yaml": "YAML",
        ".toml": "TOML",
    }

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        "node_modules",
        "venv",
        ".idea",
        ".vscode",
        "dist",
        "build",
    }

    @classmethod
    def scan_repository(cls, repository_path: str):

        repository = Path(repository_path)

        files = []

        for file in repository.rglob("*"):

            if not file.is_file():
                continue

            if any(part in cls.IGNORE_DIRS for part in file.parts):
                continue

            extension = file.suffix.lower()

            language = cls.LANGUAGE_MAP.get(extension, "Unknown")

            relative_path = file.relative_to(repository)

            metadata = FileMetadata(
                name=file.name,
                path=str(relative_path),
                extension=extension,
                size=file.stat().st_size,
                language=language,
            )

            files.append(metadata)

        return files