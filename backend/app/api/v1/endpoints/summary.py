from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.summary_service import SummaryService

router = APIRouter()


@router.get("/repositories/{repository_name}/summary")
async def get_repository_summary(repository_name: str):

    from app.utils.repository import get_repository_path

    repository_path = get_repository_path(repository_name)

    return SummaryService.generate_summary(str(repository_path))