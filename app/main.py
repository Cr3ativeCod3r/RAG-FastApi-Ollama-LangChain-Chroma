import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.core.config import get_settings
from app.api.routes import router as api_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app.main")

# Base directories
base_dir = os.path.dirname(os.path.dirname(__file__))
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
frontend_dir = os.path.join(base_dir, "frontend")

templates = Jinja2Templates(directory=templates_dir)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    settings = get_settings()
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Ollama Target: {settings.OLLAMA_BASE_URL} (Model: {settings.OLLAMA_MODEL})")
    logger.info(f"ChromaDB Target: {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="A containerized Retrieval-Augmented Generation (RAG) backend with FastAPI, LangChain, Ollama, ChromaDB, and Jinja2 UI.",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Jinja2 Admin / Management Interface
    @app.get("/", response_class=HTMLResponse, tags=["Web UI"])
    async def index_view(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "title": "Excel RAG AI Assistant",
                "settings": settings,
            },
        )

    # Mount Static Frontend (Whitepage + Chat Widget)
    if os.path.exists(frontend_dir):
        app.mount("/whitepage", StaticFiles(directory=frontend_dir, html=True), name="whitepage")
        app.mount("/client", StaticFiles(directory=frontend_dir, html=True), name="client")

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.include_router(api_router)  # Also expose without prefix for convenience

    return app


app = create_app()
