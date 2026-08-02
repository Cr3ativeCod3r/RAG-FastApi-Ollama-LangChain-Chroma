import logging
from typing import AsyncIterator
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.domain.ports import IDocumentLoader, IVectorStore, ILLMService
from app.core.config import Settings

logger = logging.getLogger(__name__)


class RagService:
    """Application service orchestrating document ingestion and RAG querying.
    Adheres to Dependency Inversion: depends on domain ports (interfaces).
    """

    def __init__(
        self,
        loader: IDocumentLoader,
        vector_store: IVectorStore,
        llm_service: ILLMService,
        settings: Settings,
    ):
        self.loader = loader
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.settings = settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.CHUNK_SIZE,
            chunk_overlap=self.settings.CHUNK_OVERLAP,
        )

    def ingest_documents(self, file_path: str | None = None, reset_collection: bool = False) -> dict:
        """Load, chunk, and index documents from the Excel file."""
        target_path = file_path or self.settings.EXCEL_FILE_PATH
        logger.info(f"Starting ingestion process for file: {target_path}")

        # 1. Load documents via domain port
        raw_documents = self.loader.load(target_path)
        logger.info(f"Loaded {len(raw_documents)} raw row records from {target_path}")

        if not raw_documents:
            return {
                "file_path": target_path,
                "raw_records_count": 0,
                "chunks_indexed": 0,
                "message": "No data found in the document.",
            }

        # 2. Split into chunks if necessary (for large cells/text)
        chunked_documents = self.text_splitter.split_documents(raw_documents)
        logger.info(f"Created {len(chunked_documents)} chunks from raw documents.")

        # 3. Optional collection reset
        if reset_collection:
            self.vector_store.clear()

        # 4. Store in Vector DB via domain port
        indexed_count = self.vector_store.add_documents(chunked_documents)

        return {
            "file_path": target_path,
            "raw_records_count": len(raw_documents),
            "chunks_indexed": indexed_count,
            "message": "Successfully ingested and indexed knowledge base into ChromaDB.",
        }

    def query(self, question: str, top_k: int | None = None) -> dict:
        """Retrieve relevant context and generate answer for the question."""
        k = top_k or self.settings.TOP_K_RESULTS
        logger.info(f"Querying RAG service with question: '{question}', top_k={k}")

        # 1. Retrieve top matching documents
        retrieved_docs = self.vector_store.similarity_search(query=question, k=k)

        # 2. Generate response via LLM service
        answer = self.llm_service.generate_answer(query=question, context_documents=retrieved_docs)

        # 3. Format source metadata
        sources = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in retrieved_docs
        ]

        return {
            "query": question,
            "answer": answer,
            "sources": sources,
            "retrieved_count": len(retrieved_docs),
        }

    async def query_stream(self, question: str, top_k: int | None = None) -> AsyncIterator[str]:
        """Stream generated response tokens for the question."""
        k = top_k or self.settings.TOP_K_RESULTS
        retrieved_docs = self.vector_store.similarity_search(query=question, k=k)
        async for token in self.llm_service.stream_answer(query=question, context_documents=retrieved_docs):
            yield token
