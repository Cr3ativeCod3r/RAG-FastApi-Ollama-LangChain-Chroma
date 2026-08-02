from abc import ABC, abstractmethod
from typing import AsyncIterator, Any
from langchain_core.documents import Document


class IDocumentLoader(ABC):
    """Abstract interface for loading raw documents into LangChain Documents."""

    @abstractmethod
    def load(self, file_path: str) -> list[Document]:
        """Load documents from the specified file path."""
        pass


class IVectorStore(ABC):
    """Abstract interface for vector database storage and retrieval."""

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> int:
        """Add and embed documents into the vector database. Returns count of inserted docs."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> list[Document]:
        """Retrieve the top k most relevant documents for a given query."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear/delete the current collection."""
        pass


class ILLMService(ABC):
    """Abstract interface for interacting with Language Models."""

    @abstractmethod
    def generate_answer(self, query: str, context_documents: list[Document]) -> str:
        """Generate a response for the given query using retrieved context documents."""
        pass

    @abstractmethod
    async def stream_answer(self, query: str, context_documents: list[Document]) -> AsyncIterator[str]:
        """Stream response tokens for the given query using retrieved context documents."""
        pass
