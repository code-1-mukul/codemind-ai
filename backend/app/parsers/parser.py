from pathlib import Path

from app.parsers.python_parser import PythonParser
from app.schemas.analysis import FileAnalysis


class ParserService:
    """
    Chooses the correct parser based on file extension.
    """

    def __init__(self):
        self.parsers = {
            ".py": PythonParser(),
        }

    def parse(self, file_path: Path)->FileAnalysis:
        parser = self.parsers.get(file_path.suffix)

        if parser is None:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        return parser.parse(file_path)