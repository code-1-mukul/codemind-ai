from fastapi import APIRouter, HTTPException

from app.services.analysis_storage_service import AnalysisStorageService
from app.services.architecture_service import ArchitectureService

router = APIRouter()

analysis_storage_service = AnalysisStorageService()
architecture_service = ArchitectureService()


@router.get("/repositories/{repository_name}/architecture")
def get_repository_architecture(
    repository_name: str,
):
    print("ARCHITECTURE REPOSITORY:", repository_name)

    try:

        analysis = analysis_storage_service.load_analysis(
            repository_name
        )

        file_graph = (
            architecture_service.build_architecture(
                analysis
            )
        )

        print("FILE GRAPH:", file_graph)

        print("\n===== IMPORT ANALYSIS =====")

        for file in analysis.files:

            print(f"\nFILE: {file.file_path}")

            for imported in file.imports:

                print(f"  IMPORT: {imported.module}")

        print("============================\n")

        module_graph = (
            architecture_service.build_module_architecture(
                file_graph
            )
        )

        data_flow = (
            architecture_service.build_analysis_flow()
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