from fastapi import FastAPI
from pathlib import Path


from app.core.config import settings
from app.api.v1.router import api_router

Path(settings.UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to CodeMind AI 🚀"
    }