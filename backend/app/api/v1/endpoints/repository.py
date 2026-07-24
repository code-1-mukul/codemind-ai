from fastapi import APIRouter

from app.core.config import settings
from app.schemas.repository import (
    RepositoryCloneRequest,
    RepositoryCloneResponse
)
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.post(
    "/repositories/clone",
    response_model=RepositoryCloneResponse
)
async def clone_repository(request: RepositoryCloneRequest):

    result = RepositoryService.clone_repository(
        repo_url=str(request.repo_url),
        upload_dir=settings.UPLOAD_DIR
    )

    return result