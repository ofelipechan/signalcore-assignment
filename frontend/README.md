# Frontend — Vendor Research Tool

React + Vite + TypeScript + Tailwind. Single flow: enter a research prompt → submit (form locks) → redirect to results page with markdown and sources.

## Requirements

- Node 18+
- pnpm

## Setup

```bash
pnpm install
```

## Run

Start the backend first (see `backend/README.md`), then:

```bash
pnpm run dev
```

Open http://localhost:5173. The dev server proxies `/api` to the backend (port 8001).

## Build

```bash
pnpm run build
```

Output is in `dist/`.

## Layout

- **Home (`/`)** — Centered textarea for the research prompt; “Start research” submits to `POST /api/research`, locks the form until done, then redirects to `/results` with the response.
- **Results (`/results`)** — Renders the markdown content, then a sources section at the bottom (url as link, title). “New research” goes back to home.
