from fastapi import Depends
from app.core.config import Settings, get_settings
from app.domain.ports import IDocumentLoader, IVectorStore, ILLMService
from app.infrastructure.excel_loader import ExcelDocumentLoader
from app.infrastructure.chroma_db import ChromaVectorStore
from app.infrastructure.ollama_llm import OllamaLLMService
from app.services.rag_service import RagService


def get_document_loader() -> IDocumentLoader:
    """Provide instance of DocumentLoader."""
    return ExcelDocumentLoader()


def get_llm_service(
    settings: Settings = Depends(get_settings),
) -> OllamaLLMService:
    """Provide Ollama LLM service."""
    return OllamaLLMService(settings=settings)


def get_vector_store(
    settings: Settings = Depends(get_settings),
    llm_service: OllamaLLMService = Depends(get_llm_service),
) -> IVectorStore:
    """Provide Chroma Vector Store instance."""
    return ChromaVectorStore(
        settings=settings,
        embedding_function=llm_service.embeddings,
    )


def get_rag_service(
    loader: IDocumentLoader = Depends(get_document_loader),
    vector_store: IVectorStore = Depends(get_vector_store),
    llm_service: OllamaLLMService = Depends(get_llm_service),
    settings: Settings = Depends(get_settings),
) -> RagService:
    """Provide RagService dependency."""
    return RagService(
        loader=loader,
        vector_store=vector_store,
        llm_service=llm_service,
        settings=settings,
    )
