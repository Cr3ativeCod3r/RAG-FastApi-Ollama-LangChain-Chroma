# Excel RAG Application (FastAPI + LangChain + Ollama + ChromaDB + React)

A containerized, production-ready Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **LangChain**, **Ollama**, and **ChromaDB**, managed with **uv**, featuring a **React** web client.

<img width="1470" height="655" alt="Web Interface" src="https://github.com/user-attachments/assets/07201c21-4b89-40e3-8840-fa837285f2d3" />
<img width="367" height="539" alt="Chat Widget" src="https://github.com/user-attachments/assets/0767cfd6-ac0f-42ad-a28b-bb13afd11104" />

The application indexes documents from an Excel spreadsheet (`.xlsx`) into **ChromaDB** vector storage and uses a local **Ollama LLM** (`llama3.2:3b` with `nomic-embed-text`) to provide accurate, grounded answers with source attribution.

---

## 🏗️ Backend Architecture (`api-service`)

The backend is built following **Layered Clean Architecture** and **SOLID** principles:

- **Presentation Layer (`app/api/`):** FastAPI route controllers, streaming endpoints, and Pydantic DTO request/response schemas with strict validation.
- **Service Layer (`app/services/`):** `RagService` orchestrating document ingestion, chunking, vector indexing, and RAG retrieval pipelines.
- **Domain Layer (`app/domain/`):** Abstract ports and interfaces (`IDocumentLoader`, `IVectorStore`, `ILLMService`) ensuring complete Dependency Inversion (DIP).
- **Infrastructure Layer (`app/infrastructure/`):** Concrete adapters for spreadsheet processing (`pandas`/`openpyxl`), vector search (`ChromaDB`), and LLM generation (`Ollama` via LangChain).
- **Core Layer (`app/core/`):** Application settings (`pydantic-settings`), Dependency Injection providers, SlowAPI rate limiter, and security sanitizers.

### Backend Directory Structure

```text
api-service/
├── .env.example              # Environment variable template
├── Dockerfile                # Multi-stage container build with uv
├── pyproject.toml            # Project metadata and dependencies (uv)
├── uv.lock                   # Deterministic dependency lockfile
├── documents/
│   └── knowledge_base.xlsx   # Knowledge base Excel spreadsheet
├── tests/
│   └── test_security_and_limits.py  # Unit & integration test suite
└── app/
    ├── __init__.py
    ├── main.py               # FastAPI application factory & middleware
    ├── api/                  # Presentation Layer
    │   ├── __init__.py
    │   ├── routes.py         # Endpoints: /health, /ingest, /ask, /ask/stream
    │   └── schemas.py        # Pydantic DTOs with validation & sanitization
    ├── core/                 # Core Layer
    │   ├── __init__.py
    │   ├── config.py         # App configuration & settings
    │   ├── dependencies.py   # FastAPI Dependency Injection wiring
    │   ├── limiter.py        # SlowAPI rate limiter instance
    │   └── security.py       # Input sanitization & prompt guard utilities
    ├── domain/               # Domain Layer
    │   ├── __init__.py
    │   └── ports.py          # Abstract interfaces (ports)
    ├── infrastructure/       # Infrastructure Layer
    │   ├── __init__.py
    │   ├── chroma_db.py      # ChromaDB vector store adapter
    │   ├── excel_loader.py   # Excel data loader & parser
    │   └── ollama_llm.py     # Ollama LLM & embeddings adapter
    └── services/             # Application Service Layer
        ├── __init__.py
        └── rag_service.py    # RAG orchestration service
```

* **Frontend (`web-client/`):** Built with **React** (TypeScript).

---

## 🛡️ Security & Threat Mitigation

To protect against abuse, resource starvation, and prompt manipulation, the backend implements the most critical security defenses:

* **Rate Limiting (DoS / Abuse Protection):** IP-based rate limiting via `slowapi` (`20 req/min` for `/ask` and `/ask/stream`, `5 req/min` for `/ingest`), returning `HTTP 429 Too Many Requests`.
* **Payload & Message Size Limits (Buffer Overflow / OOM Defense):** Enforces a `max_length=2000` character limit on queries and a global HTTP middleware rejecting requests over **1 MB** with `HTTP 413 Content Too Large`.
* **Execution Timeouts (Hanging Connection Protection):** Configurable client-side timeouts (60s) and route-level `asyncio.wait_for` (90s) returning `HTTP 504 Gateway Timeout` if model inference stalls.
* **Prompt Injection Defense:** Input sanitization removing null bytes/control characters and neutralizing boundary delimiters (`</user_question>`, `<system>`, `[INST]`), paired with strict XML tag separation (`<context>`, `<user_question>`) and hardened system prompt guardrails.

> [!NOTE]
> **Threat Landscape Notice:** LLM applications face a wide range of emerging attack vectors (e.g., advanced indirect injection from untrusted files, side-channel data exfiltration, adversarial jailbreak suffixes). The mechanisms above cover the most critical, immediate, and common attack surfaces.

---

## 🛠️ Getting Started

### Option 1: Running with Docker Compose (Recommended)

1. **Start all services:**
   ```bash
   docker compose up -d --build
   ```

2. **Pull models inside the Ollama container:**
   ```bash
   docker exec -it rag_ollama ollama pull llama3.2:3b
   docker exec -it rag_ollama ollama pull nomic-embed-text
   ```

3. **Access the application:**
   - **Web Client (React):** `http://localhost:3000`
   - **FastAPI Swagger Docs:** `http://localhost:8000/docs`

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

## 🧪 Running Backend Tests

```bash
cd api-service
uv run pytest
```

---

## 📡 API Endpoints

Interactive Swagger documentation is available at: `http://localhost:8000/docs`

| Method | Endpoint | Rate Limit | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | - | Service health status check |
| `POST` | `/api/v1/ingest` | 5/min | Ingest Excel file and index embeddings into ChromaDB |
| `POST` | `/api/v1/ask` | 20/min | Query knowledge base and receive grounded LLM response |
| `POST` | `/api/v1/ask/stream` | 20/min | Stream LLM answer tokens in real-time |
