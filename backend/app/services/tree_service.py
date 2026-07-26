from pathlib import Path

from app.schemas.tree import TreeNode


class TreeService:

    @classmethod
    def build_tree(cls, repository_path: str):

        repository = Path(repository_path)

        return cls._build_node(repository, repository)

    @classmethod
    def _build_node(cls, current_path: Path, root_path: Path):

        node = TreeNode(
            name=current_path.name,
            path=str(current_path.relative_to(root_path)) if current_path != root_path else "",
            is_directory=current_path.is_dir(),
        )

        if current_path.is_dir():

            children = sorted(
                current_path.iterdir(),
                key=lambda x: (x.is_file(), x.name.lower())
            )

            for child in children:

                if child.name in {
                    ".git",
                    "__pycache__",
                    "node_modules",
                    "venv",
                    ".idea",
                    ".vscode",
                    "dist",
                    "build",
                }:
                    continue

                node.children.append(
                    cls._build_node(child, root_path)
                )

        return node