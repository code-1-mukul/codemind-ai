from pathlib import Path

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

            nodes.append(
                ArchitectureNode(
                    id=file.file_path,
                    label=path.name,
                    type="file",
                    group=None,
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
    ) -> ArchitectureGraph:

        module_nodes = {}
        module_edge_counts = {}

        # Create one node for each group

        for node in graph.nodes:

            group = node.group

            if group is None:
                group = "external"

            if group not in module_nodes:

                module_nodes[group] = ArchitectureNode(
                    id=f"group:{group}",
                    label=group,
                    type="module",
                    group=group,
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

    def build_analysis_flow(self) -> DataFlowGraph:

        nodes = [
            FlowNode(
                id="repository",
                label="Repository",
                type="input",
            ),
            FlowNode(
                id="analysis_service",
                label="Analysis Service",
                type="service",
            ),
            FlowNode(
                id="parser",
                label="Parser",
                type="processing",
            ),
            FlowNode(
                id="repository_analysis",
                label="Repository Analysis",
                type="data",
            ),
            FlowNode(
                id="analysis_storage",
                label="Analysis Storage",
                type="storage",
            ),
            FlowNode(
                id="chunking_service",
                label="Chunking Service",
                type="service",
            ),
            FlowNode(
                id="chunks",
                label="Code Chunks",
                type="data",
            ),
            FlowNode(
                id="indexing_service",
                label="Indexing Service",
                type="service",
            ),
            FlowNode(
                id="embedding_service",
                label="Embedding Service",
                type="service",
            ),
            FlowNode(
                id="embeddings",
                label="Embeddings",
                type="data",
            ),
            FlowNode(
                id="vector_store",
                label="Vector Store",
                type="storage",
            ),
        ]

        edges = [
            FlowEdge(
                source="repository",
                target="analysis_service",
                relation="input",
            ),
            FlowEdge(
                source="analysis_service",
                target="parser",
                relation="parses",
            ),
            FlowEdge(
                source="parser",
                target="repository_analysis",
                relation="produces",
            ),
            FlowEdge(
                source="repository_analysis",
                target="analysis_storage",
                relation="stores",
            ),
            FlowEdge(
                source="repository_analysis",
                target="chunking_service",
                relation="input",
            ),
            FlowEdge(
                source="chunking_service",
                target="chunks",
                relation="produces",
            ),
            FlowEdge(
                source="chunks",
                target="indexing_service",
                relation="input",
            ),
            FlowEdge(
                source="indexing_service",
                target="embedding_service",
                relation="generates",
            ),
            FlowEdge(
                source="embedding_service",
                target="embeddings",
                relation="produces",
            ),
            FlowEdge(
                source="embeddings",
                target="vector_store",
                relation="stores",
            ),
        ]

        return DataFlowGraph(
            nodes=nodes,
            edges=edges,
        )