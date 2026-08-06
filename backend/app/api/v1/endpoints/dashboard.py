from fastapi import APIRouter

router = APIRouter()


@router.get("/{repository_name}/summary")
def get_repository_summary(repository_name: str):

    return {
        "repository_name": repository_name,
        "status": "Indexed",

        "python_files": 0,
        "classes": 0,
        "functions": 0,
        "chunks": 0,
    }