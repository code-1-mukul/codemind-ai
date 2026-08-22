from pathlib import Path
import ast

from app.schemas.analysis import (
    ClassInfo,
    FileAnalysis,
    FunctionInfo,
    ImportInfo,
    DependencyInfo,
    CallInfo,
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
        calls = []

        # ---------------------------------------------------------
        # 1. Detect file/data dependencies
        # ---------------------------------------------------------

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

                # Example:
                # pickle.load(open("model.pkl", "rb"))
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "load"
                ):

                    if node.args:

                        file_node = node.args[0]

                        if isinstance(file_node, ast.Call):

                            target = self._get_string_argument(
                                file_node
                            )

                            if target:
                                dependencies.append(
                                    DependencyInfo(
                                        target=target,
                                        relation="loads",
                                    )
                                )

                # Example:
                # pickle.dump(model, open("model.pkl", "wb"))
                elif (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "dump"
                ):

                    if len(node.args) >= 2:

                        file_node = node.args[1]

                        if isinstance(file_node, ast.Call):

                            target = self._get_string_argument(
                                file_node
                            )

                            if target:
                                dependencies.append(
                                    DependencyInfo(
                                        target=target,
                                        relation="produces",
                                    )
                                )

        # ---------------------------------------------------------
        # 2. Detect function and method calls
        # ---------------------------------------------------------

        class CallVisitor(ast.NodeVisitor):

            def __init__(self):
                self.calls = []
                self.current_class = None
                self.current_function = None

            def _get_caller_name(self):

                if self.current_function:

                    if self.current_class:
                        return (
                            f"{self.current_class}."
                            f"{self.current_function}"
                        )

                    return self.current_function

                return "module"

            def _get_callee_name(self, node):

                if isinstance(node, ast.Name):
                    return node.id

                if isinstance(node, ast.Attribute):

                    return node.attr

                return None

            def visit_ClassDef(self, node):

                previous_class = self.current_class

                self.current_class = node.name

                for child in node.body:
                    self.visit(child)

                self.current_class = previous_class

            def visit_FunctionDef(self, node):

                previous_function = self.current_function

                self.current_function = node.name

                # Visit decorators, default values, annotations,
                # and the function body.
                self.generic_visit(node)

                self.current_function = previous_function

            def visit_AsyncFunctionDef(self, node):

                previous_function = self.current_function

                self.current_function = node.name

                self.generic_visit(node)

                self.current_function = previous_function

            def visit_Call(self, node):

                callee = self._get_callee_name(node.func)

                if callee:

                    caller = self._get_caller_name()

                    self.calls.append(
                        CallInfo(
                            caller=caller,
                            callee=callee,
                            line_number=node.lineno,
                        )
                    )

                self.generic_visit(node)

        call_visitor = CallVisitor()
        call_visitor.visit(tree)

        calls.extend(call_visitor.calls)

        # ---------------------------------------------------------
        # 3. Create base file analysis
        # ---------------------------------------------------------

        analysis = FileAnalysis(
            file_path=str(file_path),
            dependencies=dependencies,
            calls=calls,
        )

        # ---------------------------------------------------------
        # 4. Extract imports, functions, and classes
        # ---------------------------------------------------------

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
                            source_lines[
                                node.lineno - 1 : node.end_lineno
                            ]
                        ),
                    )
                )

            elif isinstance(node, ast.ClassDef):

                class_info = ClassInfo(
                    name=node.name,
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node),
                    source_code="\n".join(
                        source_lines[
                            node.lineno - 1 : node.end_lineno
                        ]
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
                                    source_lines[
                                        child.lineno - 1 : child.end_lineno
                                    ]
                                ),
                            )
                        )

                analysis.classes.append(class_info)

        return analysis