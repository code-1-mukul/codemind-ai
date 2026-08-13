from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings

import json

router = APIRouter()


@router.get("/{repository_name}/summary")
def get_repository_summary(repository_name: str):

    analysis_path = (
        Path(settings.ANALYSIS_STORAGE_DIR)
        / f"{repository_name}.json"
    )

    if not analysis_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository analysis not found."
        )

    with open(
        analysis_path,
        "r",
        encoding="utf-8"
    ) as file:

        analysis = json.load(file)

    python_files = len(analysis["files"])

    classes = sum(
        len(file["classes"])
        for file in analysis["files"]
    )

    functions = sum(
        len(file["functions"])
        for file in analysis["files"]
    )

    metadata_path = (
        Path(settings.METADATA_STORAGE_DIR)
        / f"{repository_name}.json"
    )

    chunks = 0

    if metadata_path.exists():

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            metadata = json.load(file)

        chunks = len(metadata.get("entries", []))

    imports = sum(
        len(file["imports"])
        for file in analysis["files"]
    )

    return {
        "repository_name": repository_name,
        "status": "Indexed",
        "python_files": python_files,
        "classes": classes,
        "functions": functions,
        "chunks": chunks,
        "imports": imports,
    }