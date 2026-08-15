from pathlib import Path
import ast

from app.schemas.analysis import (
    ClassInfo,
    FileAnalysis,
    FunctionInfo,
    ImportInfo,
    DependencyInfo,
)


class PythonParser:

    def _get_string_argument(self, node):
        if not isinstance(node, ast.Call):
            return None

        if not node.args:
            return None

        first_arg = node.args[0]

        if isinstance(first_arg, ast.Constant):
            if isinstance(first_arg.value, str):
                return first_arg.value

        return None

    def parse(self, file_path: Path) -> FileAnalysis:
        try:
            source_code = file_path.read_text(encoding="utf-8")
            source_lines = source_code.splitlines()
        except UnicodeDecodeError:
            raise ValueError(f"Cannot read file: {file_path}")
        tree = ast.parse(source_code)

        dependencies = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                # Example:
                # pd.read_csv("dataset.csv")
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr in {
                        "read_csv",
                        "read_json",
                        "read_excel",
                    }
                ):
                    target = self._get_string_argument(node)

                    if target:
                        dependencies.append(
                            DependencyInfo(
                                target=target,
                                relation="reads",
                            )
                        )
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "load"
                ):
                    if node.args:

                        file_node = node.args[0]

                        if isinstance(file_node, ast.Call):

                            target = self._get_string_argument(file_node)

                            if target:
                                dependencies.append(
                                    DependencyInfo(
                                        target=target,
                                        relation="loads",
                                    )
                                )
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "dump"
                ):
                    if len(node.args) >= 2:

                        file_node = node.args[1]

                        if isinstance(file_node, ast.Call):

                            target = self._get_string_argument(file_node)

                            if target:
                                dependencies.append(
                                    DependencyInfo(
                                        target=target,
                                        relation="produces",
                                    )
                                )
            

        analysis = FileAnalysis(
            file_path=str(file_path),
            dependencies=dependencies,
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