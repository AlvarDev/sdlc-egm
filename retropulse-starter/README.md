# RetroPulse — CI/CD Workshop Starter

Starter repository for the **Deploying CI/CD Pipelines with Google Antigravity & the Antigravity SDK** hands-on workshop.

## Quick Start (Local)

```bash
uv sync
uv run pytest
uv run uvicorn main:app --reload --port 8000
```

## Project Layout

* `main.py` — FastAPI backend (`GET /`, `GET /api/cards`, `POST /api/cards`, `POST /api/cards/{card_id}/upvote`)
* `test_main.py` — Deterministic unit tests (`pytest`)
* `static/index.html` — 3-column Sprint Retrospective board UI
* `Dockerfile` — Multi-stage non-root Google Distroless container
* `docs/designs/retropulse.md` — Approved architecture & security specification (Single Source of Truth)
