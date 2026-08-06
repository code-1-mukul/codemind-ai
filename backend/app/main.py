from fastapi import FastAPI
from pathlib import Path
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

templates = Jinja2Templates(
    directory="app/templates"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={}
    )

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )