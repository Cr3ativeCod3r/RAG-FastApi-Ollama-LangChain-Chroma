from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    # Project metadata
    PROJECT_NAME: str = "Excel RAG API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Ollama settings (Lightweight default for 8GB RAM machines)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"
    TEMPERATURE: float = 0.1

    # ChromaDB settings
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION_NAME: str = "excel_rag_collection"

    # Ingestion settings
    EXCEL_FILE_PATH: str = "documents/knowledge_base.xlsx"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 4

    # Security & Guardrails settings
    MAX_QUERY_LENGTH: int = 2000
    MAX_REQUEST_BODY_SIZE_BYTES: int = 1_048_576  # 1 MB
    LLM_TIMEOUT_SECONDS: float = 60.0
    REQUEST_TIMEOUT_SECONDS: float = 90.0

    # Rate limiting settings
    RATE_LIMIT_DEFAULT: str = "60/minute"
    RATE_LIMIT_QUERY: str = "20/minute"
    RATE_LIMIT_INGEST: str = "5/minute"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
