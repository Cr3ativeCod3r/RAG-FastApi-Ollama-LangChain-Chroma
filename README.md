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
├── docker-compose.yml            # Multi-container orchestration (FastAPI, React, Ollama, ChromaDB)
├── .gitignore
├── README.md
│
├── api-service/                  # Python / FastAPI Backend Service
│   ├── .env.example
│   ├── Dockerfile
│   ├── pyproject.toml            # uv dependencies & project metadata
│   ├── uv.lock
│   ├── documents/
│   │   └── knowledge_base.xlsx   # Excel knowledge base dataset
│   ├── tests/                    # Backend unit & integration tests
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI application entry point & middleware
│       ├── api/                  # Presentation Layer (Routes, Schemas DTO)
│       ├── core/                 # Configuration, DI container, Limiter, Security
│       ├── domain/               # Domain Layer & Port interfaces
│       ├── infrastructure/       # ChromaDB, Ollama LLM, Excel Loader adapters
│       └── services/             # RagService orchestration
│
└── web-client/                   # React + TypeScript + Vite Frontend Client
    ├── .env.example
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── components/           # Modular Chat Widget, Launcher, Modal, Messages
        ├── hooks/                # useChat state & streaming hook
        ├── services/             # API client communication
        └── types/                # TypeScript interfaces
```

---

## 🛠️ Getting Started

### Option 1: Running with Docker Compose (Recommended)

1. **Start all services:**
   ```bash
   docker compose up -d --build
   ```

2. **Pull models inside Ollama container:**
   ```bash
   docker exec -it rag_ollama ollama pull llama3.2:3b
   docker exec -it rag_ollama ollama pull nomic-embed-text
   ```

3. **Access Services:**
   - **Frontend Web Client:** `http://localhost:3000`
   - **FastAPI Backend API:** `http://localhost:8000/docs`

---

### Option 2: Local Development

#### 1. Backend (`api-service`)
```bash
cd api-service
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend (`web-client`)
```bash
cd web-client
cp .env.example .env
npm install
npm run dev
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
