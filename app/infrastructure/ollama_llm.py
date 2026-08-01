import logging
from typing import AsyncIterator
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.domain.ports import ILLMService
from app.core.config import Settings

logger = logging.getLogger(__name__)

RAG_SYSTEM_PROMPT = """You are an intelligent, precise assistant answering user questions based strictly on the provided context retrieved from an Excel knowledge base.

Instructions:
1. Answer the question accurately and concisely using ONLY the provided Context.
2. If the answer cannot be determined from the context, politely state that the knowledge base does not contain this information. Do not fabricate answers.
3. When referencing facts, you may mention the source details if relevant.

Context:
{context}
"""


class OllamaLLMService(ILLMService):
    """Ollama implementation of the ILLMService domain port."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._llm = ChatOllama(
            base_url=self.settings.OLLAMA_BASE_URL,
            model=self.settings.OLLAMA_MODEL,
            temperature=self.settings.TEMPERATURE,
        )
        self._embeddings = OllamaEmbeddings(
            base_url=self.settings.OLLAMA_BASE_URL,
            model=self.settings.OLLAMA_EMBED_MODEL,
        )
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", RAG_SYSTEM_PROMPT),
            ("human", "{question}"),
        ])
        self._chain = self._prompt | self._llm | StrOutputParser()

    @property
    def embeddings(self) -> OllamaEmbeddings:
        """Expose embeddings for vector store integration."""
        return self._embeddings

    def _format_context(self, context_documents: list[Document]) -> str:
        """Format retrieved documents into a string for the prompt context."""
        if not context_documents:
            return "No relevant context found in the knowledge base."

        formatted_docs = []
        for i, doc in enumerate(context_documents, 1):
            source = doc.metadata.get("source", "unknown")
            sheet = doc.metadata.get("sheet_name", "Sheet1")
            row = doc.metadata.get("row_index", "?")
            formatted_docs.append(
                f"--- Document {i} [Source: {source}, Sheet: {sheet}, Row: {row}] ---\n{doc.page_content}"
            )
        return "\n\n".join(formatted_docs)

    def generate_answer(self, query: str, context_documents: list[Document]) -> str:
        """Generate answer synchronously for the user query."""
        context_str = self._format_context(context_documents)
        try:
            return self._chain.invoke({"context": context_str, "question": query})
        except Exception as e:
            logger.error(f"Error invoking Ollama LLM: {e}")
            raise

    async def stream_answer(self, query: str, context_documents: list[Document]) -> AsyncIterator[str]:
        """Stream answer tokens asynchronously."""
        context_str = self._format_context(context_documents)
        async for chunk in self._chain.astream({"context": context_str, "question": query}):
            yield chunk
