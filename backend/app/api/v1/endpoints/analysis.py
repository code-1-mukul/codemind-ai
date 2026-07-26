from fastapi import APIRouter, HTTPException

from app.services.analysis_service import AnalysisService
from app.services.repository_service import RepositoryService
from app.core.config import settings

router = APIRouter()

analysis_service = AnalysisService()
repository_service = RepositoryService()


@router.post("/{repository_name}/analyze")
def analyze_repository(repository_name: str):

    repository_path = repository_service.get_repository_path(
        repository_name,
        settings.UPLOAD_DIR,
        )

    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return analysis_service.analyze_repository(
        repository_name=repository_name,
        repository_path=repository_path,
    )