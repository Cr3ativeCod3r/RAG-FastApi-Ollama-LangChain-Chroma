import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.limiter import limiter
from app.api.routes import router as api_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app.main")


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
        description="A containerized Retrieval-Augmented Generation (RAG) backend with FastAPI, LangChain, Ollama, and ChromaDB.",
        lifespan=lifespan,
    )

    # Attach SlowAPI limiter state and handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Request Body Size Limit Middleware (Buffer overflow protection)
    @app.middleware("http")
    async def limit_payload_size(request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length = int(content_length)
                if length > settings.MAX_REQUEST_BODY_SIZE_BYTES:
                    return JSONResponse(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        content={
                            "detail": f"Payload too large. Maximum allowed size is {settings.MAX_REQUEST_BODY_SIZE_BYTES} bytes."
                        },
                    )
            except ValueError:
                pass
        return await call_next(request)

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API Routers
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.include_router(api_router)  # Also expose without prefix for convenience

    return app


app = create_app()
