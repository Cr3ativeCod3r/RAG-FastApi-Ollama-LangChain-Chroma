import logging
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.domain.ports import IVectorStore
from app.core.config import Settings

logger = logging.getLogger(__name__)


class ChromaVectorStore(IVectorStore):
    """ChromaDB implementation of the IVectorStore domain port."""

    def __init__(self, settings: Settings, embedding_function: Embeddings):
        self.settings = settings
        self.embedding_function = embedding_function
        self._client = self._init_chroma_client()
        self._vector_store = Chroma(
            client=self._client,
            collection_name=self.settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_function,
        )

    def _init_chroma_client(self) -> chromadb.ClientAPI:
        """Initialize Chroma HTTP client or fallback to local persistent client."""
        try:
            # Connect to Chroma HTTP server (Docker or standalone)
            client = chromadb.HttpClient(
                host=self.settings.CHROMA_HOST,
                port=self.settings.CHROMA_PORT,
            )
            client.heartbeat()
            logger.info(f"Connected to ChromaDB server at {self.settings.CHROMA_HOST}:{self.settings.CHROMA_PORT}")
            return client
        except Exception as e:
            logger.warning(
                f"Could not connect to ChromaDB HTTP server ({e}). Initializing local ephemeral/persistent client."
            )
            return chromadb.PersistentClient(path="./chroma_data")

    def add_documents(self, documents: list[Document]) -> int:
        """Embed and store documents into Chroma collection."""
        if not documents:
            return 0
        self._vector_store.add_documents(documents)
        logger.info(f"Successfully added {len(documents)} documents to ChromaDB collection.")
        return len(documents)

    def similarity_search(self, query: str, k: int = 4) -> list[Document]:
        """Perform similarity search for top k documents."""
        return self._vector_store.similarity_search(query=query, k=k)

    def clear(self) -> None:
        """Delete and recreate the Chroma collection."""
        try:
            self._client.delete_collection(self.settings.CHROMA_COLLECTION_NAME)
            logger.info(f"Deleted Chroma collection: {self.settings.CHROMA_COLLECTION_NAME}")
        except Exception as e:
            logger.warning(f"Error resetting collection: {e}")

        self._vector_store = Chroma(
            client=self._client,
            collection_name=self.settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_function,
        )
