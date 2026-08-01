from typing import Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(default="ok", example="ok")
    version: str = Field(default="1.0.0", example="1.0.0")
    message: str = Field(default="RAG API service is operational")


class IngestRequest(BaseModel):
    """Request schema for document ingestion."""
    file_path: str | None = Field(
        default=None,
        description="Path to the Excel file to ingest (defaults to configured knowledge_base.xlsx)",
        example="documents/knowledge_base.xlsx",
    )
    reset_collection: bool = Field(
        default=False,
        description="Whether to purge existing vector collection before indexing new documents",
    )


class IngestResponse(BaseModel):
    """Response schema for document ingestion."""
    file_path: str
    raw_records_count: int
    chunks_indexed: int
    message: str


class QueryRequest(BaseModel):
    """Request schema for RAG Q&A query."""
    query: str = Field(
        ...,
        min_length=1,
        description="User question to answer using the knowledge base",
        example="What is the return policy for defective items?",
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
        description="Number of relevant chunks to retrieve from ChromaDB",
        example=4,
    )


class SourceDocument(BaseModel):
    """Schema representing retrieved source document metadata."""
    content: str
    metadata: dict[str, Any]


class QueryResponse(BaseModel):
    """Response schema for RAG Q&A query."""
    query: str
    answer: str
    sources: list[SourceDocument]
    retrieved_count: int
