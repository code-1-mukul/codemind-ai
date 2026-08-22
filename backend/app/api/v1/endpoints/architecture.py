from fastapi import APIRouter, HTTPException

from app.services.analysis_storage_service import AnalysisStorageService
from app.services.architecture_service import ArchitectureService
from app.services.tree_service import TreeService
from app.utils.repository import get_repository_path

router = APIRouter()

analysis_storage_service = AnalysisStorageService()
architecture_service = ArchitectureService()


@router.get("/repositories/{repository_name}/architecture")
def get_repository_architecture(
    repository_name: str,
):
    # print("ARCHITECTURE REPOSITORY:", repository_name)

    try:

        analysis = analysis_storage_service.load_analysis(
            repository_name
        )

        repository_path = get_repository_path(repository_name)

        tree = TreeService.build_tree(
            str(repository_path)
        )

        file_graph = (
            architecture_service.build_architecture(
                analysis
            )
        )

        # print("FILE GRAPH:", file_graph)

        # print("\n===== IMPORT ANALYSIS =====")

        # for file in analysis.files:

        #     print(f"\nFILE: {file.file_path}")

        #     for imported in file.imports:

        #         print(f"  IMPORT: {imported.module}")

        # print("============================\n")

        module_graph = (
            architecture_service.infer_component_architecture(
                repository_name=repository_name,
                analysis=analysis,
                tree=tree,
            )
        )

        data_flow = (
            architecture_service.build_analysis_flow(analysis)
        )

        return {
            "file_graph": file_graph,
            "module_graph": module_graph,
            "data_flow": data_flow,
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Repository analysis not found",
        )