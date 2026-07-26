from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import repository
from app.api.v1.endpoints import scanner
from app.api.v1.endpoints import tree
from app.api.v1.endpoints import summary

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    repository.router,
    tags=["Repository"]
)

api_router.include_router(
    scanner.router,
    tags=["Scanner"]
)

api_router.include_router(
    tree.router,
    tags=["Project Tree"]
)

api_router.include_router(
    summary.router,
    tags=["Summary"]
)