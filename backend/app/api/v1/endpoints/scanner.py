from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.scanner_service import ScannerService

router = APIRouter()


@router.get("/repositories/{repository_name}/scan")
async def scan_repository(repository_name: str):

    from app.utils.repository import get_repository_path

    repository_path = get_repository_path(repository_name)

    files = ScannerService.scan_repository(str(repository_path))

    return {
        "repository": repository_name,
        "total_files": len(files),
        "files": files,
    }