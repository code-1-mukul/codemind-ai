from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@router.get("/info")
async def info():
    return {
        "project": "CodeMind AI",
        "version": "1.0.0",
        "author": "Mukul"
    }