# Vendor Research Tool

Web app for AI-powered vendor comparison: you describe what you need, the agent researches the web and returns a markdown report with sources.

## Requirements

- **Backend:** Python 3.12
- **Frontend:** Node 18+, pnpm (or npm for root scripts)

## Quick start

### 1. Clone the repo

```bash
git clone <repo-url>
cd signalcore-assignment
```

### 2. Backend setup and run

From the repo root, create a venv in `backend/` and install dependencies (Python deps live in root `requirements.txt`):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r ../requirements.txt
```

Create `backend/.env` with:

- **LLM (at least one):** `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `OPENROUTER_API_KEY`
- **Search:** `TAVILY_API_KEY` (required for web search)
- **Optional:** `DEFAULT_LLM_PROVIDER`, `DEFAULT_LLM_MODEL`, `MAX_AGENT_STEPS`, `HTTP_TIMEOUT_SECONDS`

Run the API (from `backend/` with venv activated):

```bash
uvicorn app.main:app --reload --port 8001
```

- API: http://localhost:8001 — Docs: http://localhost:8001/docs

### 3. Frontend setup and run

In a new terminal, from the repo root:

```bash
cd frontend
pnpm install
pnpm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api` to the backend.

### 4. Install all dependencies from repo root (optional)

From the repo root (create and activate the backend venv first if you use it):

```bash
pnpm run install:all
```

This installs root dev deps (e.g. `concurrently`), backend Python deps, and frontend deps. Or run separately: `pnpm run install:backend` and `pnpm run install:frontend`.

### 5. Run both from repo root (optional)

With backend venv and deps already set up, and frontend deps installed (`pnpm run install:all` or manual steps), from the repo root:

```bash
pnpm install       # ensure root deps (e.g. concurrently) are installed
pnpm run start     # runs backend + frontend together
```

**Important:** Activate the backend venv in this terminal first so the backend uses the correct Python and dependencies. Then open http://localhost:5173.

### 6. Run backend with Docker

From the repo root, with Docker and Docker Compose installed:

1. Create `backend/.env` with at least one LLM key and `TAVILY_API_KEY`.
2. Start the backend (port 8001) with live reload:

```bash
pnpm run start:docker
# or: docker compose up
```

Run the frontend locally in another terminal: `cd frontend && pnpm run dev`, then open http://localhost:5173. The Vite dev server proxies `/api` to the backend.

### 7. Use the app

1. Enter a research prompt (e.g. “Compare observability platforms for production LLM apps: Langsmith, Langfuse, Braintrust”).
2. Click **Start research**. The form locks until the request completes.
3. You’re redirected to the results page: markdown content first, then a list of sources (URL, title) at the bottom.

## Run commands (quick reference)

| Goal | Command | Where |
|------|---------|--------|
| Backend only | `uvicorn app.main:app --reload --port 8001` | From `backend/` with venv activated |
| Backend only (root) | `pnpm run start:backend` | From repo root (venv must be activated) |
| Frontend only | `pnpm run dev` | From `frontend/` |
| Frontend only (root) | `pnpm run start:frontend` | From repo root |
| Backend + frontend | `pnpm run start` | From repo root (venv activated) |
| Backend in Docker | `pnpm run start:docker` or `docker compose up` | From repo root |
| Install all deps | `pnpm run install:all` | From repo root |

## Project layout

| Path | Description |
|------|-------------|
| `package.json` | Root scripts: `install:all`, `start` (backend + frontend), `start:backend`, `start:frontend`, `start:docker` |
| `backend/` | FastAPI app, Pydantic AI agent, tools (search, fetch_url) |
| `frontend/` | React + Vite + Tailwind UI |
| `requirements.txt` | Python dependencies (backend); install from `backend/` with `pip install -r ../requirements.txt` |
| `backend/Dockerfile` | Backend image (Python 3.12, uvicorn with --reload). Build from repo root. |
| `docker-compose.yml` | Backend service with volume mount for live reload; run from repo root. |
| `vendor-research-tool.plan.md` | Build plan and section checklists |

See `backend/README.md` and `frontend/README.md` for per-package details.
