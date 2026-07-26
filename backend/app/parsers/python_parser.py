from pathlib import Path
import ast

from app.schemas.analysis import (
    ClassInfo,
    FileAnalysis,
    FunctionInfo,
    ImportInfo,
)


class PythonParser:
    def parse(self, file_path: Path) -> FileAnalysis:
        try:
            source_code = file_path.read_text(encoding="utf-8")
            source_lines = source_code.splitlines()
        except UnicodeDecodeError:
            raise ValueError(f"Cannot read file: {file_path}")
        tree = ast.parse(source_code)

        analysis = FileAnalysis(
            file_path=str(file_path),
        )

        for node in tree.body:

            if isinstance(node, ast.Import):
                for alias in node.names:
                    analysis.imports.append(
                        ImportInfo(
                            module=alias.name,
                        )
                    )

            elif isinstance(node, ast.ImportFrom):
                analysis.imports.append(
                    ImportInfo(
                        module=node.module or "",
                    )
                )

            elif isinstance(node, ast.FunctionDef):
                analysis.functions.append(
                    FunctionInfo(
                        name=node.name,
                        line_number=node.lineno,
                        docstring=ast.get_docstring(node),
                        source_code="\n".join(
                            source_lines[node.lineno - 1 : node.end_lineno]
                        ),
                    )
                )

            elif isinstance(node, ast.ClassDef):

                class_info = ClassInfo(
                    name=node.name,
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node),
                    source_code="\n".join(
                        source_lines[node.lineno - 1 : node.end_lineno]
                    ),
                )

                for child in node.body:

                    if isinstance(child, ast.FunctionDef):
                        class_info.methods.append(
                            FunctionInfo(
                                name=child.name,
                                line_number=child.lineno,
                                docstring=ast.get_docstring(child),
                                source_code="\n".join(
                                    source_lines[node.lineno - 1 : node.end_lineno]
                                ),
                            )
                        )

                analysis.classes.append(class_info)

        return analysis