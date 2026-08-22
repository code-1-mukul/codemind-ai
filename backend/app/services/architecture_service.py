from pathlib import Path

import json

from app.services.llm.llm_service import LLMService

from app.schemas.analysis import RepositoryAnalysis
from app.schemas.architecture import (
    ArchitectureGraph,
    ArchitectureNode,
    ArchitectureEdge,
    FlowEdge,
    FlowNode,
    DataFlowGraph,
)

class ArchitectureService:

    def __init__(self):
        self.llm_service = LLMService()

    def infer_component_architecture(
        self,
        repository_name: str,
        analysis: RepositoryAnalysis,
        tree,
    ) -> ArchitectureGraph:

        response = self.llm_service.infer_architecture(
            repository_name=repository_name,
            project_tree=tree.model_dump(),
            analysis=analysis.model_dump(),
        )

        try:
            architecture_data = json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"LLM returned invalid architecture JSON: {e}"
            )

        for edge in architecture_data.get("edges", []):

            if "relation" not in edge and "label" in edge:
                edge["relation"] = edge.pop("label")

        return ArchitectureGraph.model_validate(
            architecture_data
        )

    def build_architecture(
    self,
    analysis: RepositoryAnalysis,
    ) -> ArchitectureGraph:

        nodes = []
        edges = []

        
        # 1. Build a lookup of all Python files in the repository
        

        file_lookup = {}

        for file in analysis.files:

            path = Path(file.file_path)

            # Convert:
            #
            # backend/app/services/test.py
            #
            # into possible module representations.
            #
            # We keep the file path as the canonical identifier.

            file_lookup[file.file_path] = path

        
        # 2. Create nodes for every analyzed file
        

        for file in analysis.files:

            path = Path(file.file_path)

            parts = path.parts

            repository_index = None

            for i, part in enumerate(parts):
                if part.endswith('.git'):
                    repository_index=i
                    break;

            group = 'root'

            if repository_index is not None:
                relative_parts = parts[repository_index+1:]

                if len(relative_parts)>1:
                    directories = relative_parts[:-1]
                    group = directories[-1]

            nodes.append(
                ArchitectureNode(
                    id=file.file_path,
                    label=path.name,
                    type="file",
                    group=group,
                )
            )


        for file in analysis.files:

            for dependency in file.dependencies:

                target = dependency.target

                # Don't create duplicate artifact nodes
                if any(node.id == target for node in nodes):
                    continue

                nodes.append(
                    ArchitectureNode(
                        id=target,
                        label=Path(target).name,
                        type="artifact",
                        group="artifacts",
                    )
                )

        
        # 3. Helper for finding an internal file from an import
        

        def find_internal_file(imported_module: str):

            # Convert:
            #
            # package.module
            #
            # into:
            #
            # package/module

            module_path = Path(
                *imported_module.split(".")
            )

            # Try possible Python representations.
            candidates = [
                module_path.with_suffix(".py"),
                module_path / "__init__.py",
            ]

            for candidate in candidates:

                candidate_str = str(candidate)

                for file_path in file_lookup:

                    normalized_file = str(
                        Path(file_path)
                    )

                    # Compare using path suffix.
                    #
                    # This allows the repository to live inside
                    # an arbitrary upload directory.

                    if normalized_file.endswith(
                        candidate_str
                    ):
                        return file_path

            return None

        
        # 4. Build dependency edges
        

        existing_edges = set()

        for file in analysis.files:

            source_id = file.file_path

            for imported_module in file.imports:

                module = imported_module.module

                target_file = find_internal_file(
                    module
                )

                # Only create an edge when the imported
                # module belongs to this repository.

                if target_file is None:
                    continue

                edge_key = (
                    source_id,
                    target_file,
                )

                if edge_key in existing_edges:
                    continue

                existing_edges.add(edge_key)

                edges.append(
                    ArchitectureEdge(
                        source=source_id,
                        target=target_file,
                        relation="imports",
                    )
                )

        for file in analysis.files:

            source_id = file.file_path

            for dependency in file.dependencies:

                edges.append(
                    ArchitectureEdge(
                        source=source_id,
                        target=dependency.target,
                        relation=dependency.relation,
                    )
                )
        return ArchitectureGraph(
            nodes=nodes,
            edges=edges,
        )

    def build_module_architecture(
        self,
        graph: ArchitectureGraph,
        tree,
    ) -> ArchitectureGraph:

        module_nodes = {}
        module_edge_counts = {}

        def collect_directories(node):
            directories = []

            if node.is_directory:
                directories.append(node.path)

                for child in node.children:
                    directories.extend(
                        collect_directories(child)
                    )

            return directories


        tree_directories = collect_directories(tree)

        for directory in tree_directories:

            if not directory:
                continue

            component_name = Path(directory).name

            module_nodes[component_name] = ArchitectureNode(
                id=f"group:{component_name}",
                label=component_name,
                type="module",
                group=component_name,
            )

        # Aggregate file-level relationships

        node_lookup = {
            node.id: node
            for node in graph.nodes
        }

        for edge in graph.edges:

            source_node = node_lookup.get(edge.source)
            target_node = node_lookup.get(edge.target)

            if source_node is None or target_node is None:
                continue

            source_group = source_node.group or "external"
            target_group = target_node.group or "external"

            # Ignore relationships inside
            # the same module.
            if source_group == target_group:
                continue

            edge_key = (
                source_group,
                target_group,
            )

            module_edge_counts[edge_key] = (
                module_edge_counts.get(edge_key, 0) + 1
            )

        # Create aggregated edges

        module_edges = []

        for (
            (source_group, target_group),
            count,
        ) in module_edge_counts.items():

            module_edges.append(
                ArchitectureEdge(
                    source=f"group:{source_group}",
                    target=f"group:{target_group}",
                    relation=f"depends_on:{count}",
                )
            )

        return ArchitectureGraph(
            nodes=list(module_nodes.values()),
            edges=module_edges,
        )

    def build_analysis_flow(
            self,
            analysis: RepositoryAnalysis,
    ) -> DataFlowGraph:

        nodes = []
        edges = []

        file_nodes = {}

        for file in analysis.files:

            file_node = FlowNode(
                id=file.file_path,
                label=Path(file.file_path).name,
                type="file",
            )

            nodes.append(file_node)
            file_nodes[file.file_path] = file_node

        for file in analysis.files:

            source_id = file.file_path

            for dependency in file.dependencies:

                edges.append(
                    FlowEdge(
                        source=source_id,
                        target=dependency.target,
                        relation=dependency.relation,
                    )
                )

        for file in analysis.files:

            for dependency in file.dependencies:

                target = dependency.target

                if target in file_nodes:
                    continue

                if any(node.id == target for node in nodes):
                    continue

                nodes.append(
                    FlowNode(
                        id=target,
                        label=Path(target).name,
                        type="data",
                    )
                )

        return DataFlowGraph(
            nodes=nodes,
            edges=edges,
        )