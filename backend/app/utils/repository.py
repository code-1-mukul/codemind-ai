from pathlib import Path

from fastapi import HTTPException

from app.core.config import settings


def get_repository_path(repository_name: str) -> Path:
    """
    Returns repository path if it exists.
    Raises 404 otherwise.
    """

    repository_path = Path(settings.UPLOAD_DIR) / repository_name

    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository not found."
        )

    return repository_path