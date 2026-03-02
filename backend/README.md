# Backend — Vendor Research Tool

Python FastAPI backend: research agent (LLM + tools) and `/api/research` endpoint.

## Requirements

- python 3.12

## Setup

From this directory (`backend/`). Python deps are in the repo root `requirements.txt`:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r ../requirements.txt
```

Set env (e.g. in `.env` in `backend/`):

- **LLM (at least one):** `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `OPENROUTER_API_KEY` — required for the agent depending on provider.
- **Search:** `TAVILY_API_KEY` — required for web search (Tavily API).
- **Default model (optional):** `DEFAULT_LLM_PROVIDER` (e.g. `openrouter`, `openai`, `anthropic`) and `DEFAULT_LLM_MODEL` (e.g. `openai/gpt-4o`, `gpt-4o`, `claude-3-5-sonnet`). If unset, the agent will use a fallback when implemented. For OpenRouter, use the full model id (e.g. `openai/gpt-4o`).

Provider and model are set via env only (no per-request override).

Optional: `HTTP_TIMEOUT_SECONDS`, `MAX_AGENT_STEPS`.

## API

- **`POST /api/research`** — Run the research agent.
  - **Body:** `{ "prompt": "..." }` (prompt required).
  - **Response:** `{ "markdown": "...", "sources": [ { "url", "title?", "source_type?", "date?" } ] }`. `sources` is always present; each source has at least `url`; `date` is set or `"unknown"` so the UI can show provenance and recency.
- Streaming (e.g. SSE) is not implemented; the response is returned when the agent run completes.

## CORS

CORS is enabled for local frontend development. Allowed origins include `http://localhost:5173` and `http://127.0.0.1:5173` (typical Vite dev server). If you serve the frontend from another origin, add it to `allow_origins` in `app/main.py`.

## Run

**Local:** from `backend/`:

```bash
uvicorn app.main:app --reload --port 8001
```

**Docker (with live reload):** from repo root, with `backend/.env` set:

```bash
docker compose up --build backend
```

The compose file mounts `./backend` into the container so code changes trigger uvicorn reload. API: http://localhost:8001 — Docs: http://localhost:8001/docs

## Layout

- `app/main.py` — FastAPI app, CORS, router
- `app/config.py` — pydantic-settings
- `app/api/routes.py` — `POST /api/research`
- `app/agent/` — research agent (LLM + tools loop); `app/agent/prompts/` — system prompt file(s)
- `app/tools/` — fetch_url, search
- `app/models/schemas.py` — ResearchRequest, ResearchResponse
