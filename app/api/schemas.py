from typing import Any
from pydantic import BaseModel, Field, field_validator

from app.core.security import sanitize_user_input


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(default="ok", examples=["ok"])
    version: str = Field(default="1.0.0", examples=["1.0.0"])
    message: str = Field(default="RAG API service is operational")


class IngestRequest(BaseModel):
    """Request schema for document ingestion."""
    file_path: str | None = Field(
        default=None,
        max_length=500,
        description="Path to the Excel file to ingest (defaults to configured knowledge_base.xlsx)",
        examples=["documents/knowledge_base.xlsx"],
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
        max_length=2000,
        description="User question to answer using the knowledge base (max 2000 chars)",
        examples=["What is the return policy for defective items?"],
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
        description="Number of relevant chunks to retrieve from ChromaDB",
        examples=[4],
    )

    @field_validator("query")
    @classmethod
    def validate_and_sanitize_query(cls, value: str) -> str:
        sanitized = sanitize_user_input(value)
        if not sanitized:
            raise ValueError("Query cannot be empty or contain only invalid characters.")
        return sanitized


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
