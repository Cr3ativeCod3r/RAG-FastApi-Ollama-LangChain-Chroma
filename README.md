# Excel RAG API (FastAPI + LangChain + Ollama + ChromaDB + UV)

A containerized, production-ready Retrieval-Augmented Generation (RAG) backend built with Python, **FastAPI**, **LangChain**, **Ollama**, and **ChromaDB**, managed with the ultra-fast package manager **uv**.

This application reads knowledge base documents from an Excel spreadsheet (`.xlsx`), vectorizes the data into ChromaDB, and uses a local Ollama LLM to answer user queries with high accuracy and source attribution.

---

## 🏗️ Architecture

Built following a **Layered Clean Architecture** and **SOLID** principles:
- **Presentation Layer (`app/api/`):** FastAPI endpoints, routing, and Pydantic DTO schemas.
- **Service Layer (`app/services/`):** `RagService` orchestrating document ingestion and semantic query retrieval.
- **Infrastructure Layer (`app/infrastructure/`):** Concrete implementations for Excel parsing (`pandas`/`openpyxl`), vector storage (`ChromaDB`), and LLM prompting (`Ollama`).
- **Domain Layer (`app/domain/`):** Abstract interfaces (`ports.py`) ensuring Dependency Inversion (DIP).
- **Core Layer (`app/core/`):** Pydantic Settings and FastAPI Dependency Injection providers.

---

## 🚀 Tech Stack & Tools

- **Package Manager:** [Astral uv](https://github.com/astral-sh/uv) (fast Python package installer and resolver)
- **Web Framework:** FastAPI + Uvicorn
- **AI / LLM:** Ollama (e.g. `llama3`, `mistral`)
- **Embeddings:** Ollama Embeddings (e.g. `nomic-embed-text`)
- **Vector Database:** ChromaDB
- **Orchestration:** LangChain
- **Spreadsheet Processing:** pandas + openpyxl
- **Containerization:** Docker & Docker Compose

---

## 📂 Project Directory Structure

```text
.
├── .gitignore
├── .env.example
├── README.md
├── pyproject.toml
├── uv.lock
├── docker-compose.yml
├── backend.Dockerfile
├── documents/
│   └── knowledge_base.xlsx       # Excel file with Q&A / knowledge base data
└── app/
    ├── __init__.py
    ├── main.py                   # FastAPI application entry point
    ├── api/                      # Presentation Layer
    │   ├── __init__.py
    │   ├── routes.py             # API Endpoints (/health, /ingest, /ask, /ask/stream)
    │   └── schemas.py            # Pydantic models (DTOs)
    ├── core/                     # Configuration and DI setup
    │   ├── __init__.py
    │   ├── config.py             # Environment variables (pydantic-settings)
    │   └── dependencies.py       # Dependency Injection container
    ├── domain/                   # Domain Layer (Business Rules & Interfaces)
    │   ├── __init__.py
    │   └── ports.py              # Abstract Base Classes (IDocumentLoader, IVectorStore, ILLMService)
    ├── infrastructure/           # Infrastructure Layer (Concrete Implementations)
    │   ├── __init__.py
    │   ├── chroma_db.py          # ChromaDB implementation
    │   ├── ollama_llm.py         # Ollama / LangChain implementation
    │   └── excel_loader.py       # Excel loader using pandas & openpyxl
    └── services/                 # Application / Service Layer
        ├── __init__.py
        └── rag_service.py        # Core RAG orchestration logic
```

---

## 🛠️ Getting Started

### Option 1: Running with UV (Local Development)

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Sync dependencies (if needed):**
   ```bash
   uv sync
   ```

3. **Start local Ollama & ChromaDB:**
   Make sure Ollama is running on your machine:
   ```bash
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text
   ```

4. **Start the FastAPI server:**
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```

---

### Option 2: Running with Docker Compose

1. **Start all services:**
   ```bash
   docker compose up -d --build
   ```

2. **Pull models inside Ollama container:**
   ```bash
   docker exec -it rag_ollama ollama pull llama3.2:3b
   docker exec -it rag_ollama ollama pull nomic-embed-text
   ```

---

## 📡 API Endpoints

Interactive Swagger documentation is available at: `http://localhost:8000/docs`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status check |
| `POST` | `/api/v1/ingest` | Ingest Excel file and store embeddings in ChromaDB |
| `POST` | `/api/v1/ask` | Query the knowledge base with Ollama LLM response |
| `POST` | `/api/v1/ask/stream` | Stream LLM answer tokens in real-time |

### Example Queries

#### 1. Ingest Knowledge Base
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
     -H "Content-Type: application/json" \
     -d '{"reset_collection": true}'
```

#### 2. Ask a Question
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the return policy for damaged items?"}'
```

#### 3. Ask with Streaming
```bash
curl -N -X POST "http://localhost:8000/api/v1/ask/stream" \
     -H "Content-Type: application/json" \
     -d '{"query": "How much is the remote work equipment stipend?"}'
```
