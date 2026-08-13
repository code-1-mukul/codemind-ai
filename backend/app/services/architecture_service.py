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

        module_to_file = {}

        for file in analysis.files:

            path = Path(file.file_path)

            parts = list(path.with_suffix("").parts)

            # Find the "app" package inside the path
            if "app" in parts:

                app_index = parts.index("app")

                module_parts = parts[app_index:]

                module_name = ".".join(module_parts)

                module_to_file[module_name] = file.file_path

        for file in analysis.files:

            path = Path(file.file_path)

            group = None

            parts = path.parts

            if "app" in parts:

                app_index = parts.index("app")

                relative_parts = parts[app_index + 1:]

                if relative_parts:

                    # File directly inside app/
                    if len(relative_parts) == 1:
                        group = "app"

                    # File inside a subdirectory of app/
                    else:
                        group = relative_parts[0]

            nodes.append(
                ArchitectureNode(
                    id=file.file_path,
                    label=path.name,
                    type="file",
                    group=group,
                )
            )

        existing_edges = set()

        for file in analysis.files:

            source_id = file.file_path

            for imported_module in file.imports:

                module = imported_module.module

                target_file = None
        
                # Direct module match

                if module in module_to_file:

                    target_file = module_to_file[module]

                # Handle imports from a module
                #
                # Example:
                #
                # app.services.analysis_service.AnalysisService
                #
                # → app.services.analysis_service

                else:

                    module_parts = module.split(".")

                    for i in range(
                        len(module_parts),
                        0,
                        -1,
                    ):

                        candidate = ".".join(
                            module_parts[:i]
                        )

                        if candidate in module_to_file:

                            target_file = module_to_file[
                                candidate
                            ]

                            break

                # Create internal relationship

                if target_file is not None:

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