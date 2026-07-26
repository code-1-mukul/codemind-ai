from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.tree_service import TreeService

router = APIRouter()


@router.get("/repositories/{repository_name}/tree")
async def get_project_tree(repository_name: str):

    from app.utils.repository import get_repository_path

    repository_path = get_repository_path(repository_name)

    tree = TreeService.build_tree(str(repository_path))

    return tree