from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import repository
from app.api.v1.endpoints import scanner
from app.api.v1.endpoints import tree
from app.api.v1.endpoints import summary
from app.api.v1.endpoints import analysis
from app.api.v1.endpoints import chunk
from app.api.v1.endpoints import retrieval
from app.api.v1.endpoints import question_answer
from app.api.v1.endpoints import chat
from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import architecture

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

api_router.include_router(
    analysis.router,
    prefix="/repository",
    tags=["Analysis"]
)

api_router.include_router(
    chunk.router,
    prefix="/chunk",
    tags=["Chunk"],
)

api_router.include_router(
    retrieval.router,
    prefix="/repository",
    tags=["Semantic Retrieval"]
)

api_router.include_router(
    question_answer.router,
    prefix="/question_answer",
    tags=["Question Answering"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

api_router.include_router(
    architecture.router,
    prefix="/architecture",
    tags=["Architecture"]
)
