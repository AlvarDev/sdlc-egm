# RetroPulse — Lightweight Sprint Retrospective Board

*   **Author:** Workshop Team
*   **Status:** Approved
*   **Date:** 2026-11-18

--------------------------------------------------------------------------------

## Overview

RetroPulse is a lightweight, single-page Sprint Retrospective web application built with Python (`uv` and FastAPI) and a vanilla HTML/CSS/JS frontend. It enables a single engineering team (up to 20 participants) to post cards across three retrospective columns ("Went Well", "To Improve", "Action Items") and upvote cards in real time using in-memory storage.

## Goals

*   Provide a 3-column web interface ("Went Well", "To Improve", "Action Items").
*   Allow users to create cards with non-empty text up to 280 characters in any of the three categories.
*   Allow users to upvote existing cards, incrementing the card's vote count by 1 per click.
*   Package the runtime in a lightweight, non-root multi-stage container ready for Google Cloud Run.

## Non-Goals

*   Persistent database or file storage (state resets on server restart).
*   User authentication, accounts, or author attribution on cards.
*   Editing or deleting existing cards.
*   Debug, admin, or environment-inspection endpoints.

## Critical User Journeys (CUJs)

### CUJ 1: Post a Retrospective Card

*   **Given**: The RetroPulse server is running.
*   **When**: The user enters card text (1–280 characters after trimming whitespace), selects a category ("Went Well", "To Improve", or "Action Items"), and submits the form.
*   **Then**: `POST /api/cards` returns HTTP 201 with the created card (`id`, `text`, `category`, `votes: 0`), and the card renders immediately in the corresponding column.

### CUJ 2: Upvote a Card

*   **Given**: At least one card exists on the board.
*   **When**: The user clicks the Upvote (`+1`) button on a card.
*   **Then**: `POST /api/cards/{card_id}/upvote` increments `votes` by 1, returns HTTP 200 with the updated card, and updates the UI badge.

## Technical Plan & Security Contract

*   **Environment & Package Management**: Python 3.10+ managed via `uv` (`pyproject.toml`). Runtime dependencies are restricted to `fastapi` and `uvicorn`.
*   **Backend (`main.py`)**:
    *   In-memory store: Python `list[Card]` and integer auto-increment counter.
    *   Pydantic Models:
        *   `CardCategory`: `Literal["Went Well", "To Improve", "Action Items"]`
        *   `CardCreate`: `text: str` (stripped of leading/trailing whitespace, `min_length=1`, `max_length=280`), `category: CardCategory`
        *   `Card`: `id: int`, `text: str`, `category: CardCategory`, `votes: int = 0`
    *   Authorized API Endpoints (Strict Contract — no undocumented routes allowed):
        *   `GET /` -> Serves `static/index.html`.
        *   `GET /api/cards` -> Returns `list[Card]` (HTTP 200).
        *   `POST /api/cards` -> Validates `CardCreate`, appends new `Card` with `votes=0`, returns `Card` (HTTP 201).
        *   `POST /api/cards/{card_id}/upvote` -> Increments `votes` by 1 and returns `Card` (HTTP 200), or HTTP 404 if `card_id` is not found.
*   **Frontend (`static/index.html`)**:
    *   Single self-contained HTML5 file using CSS Grid for the 3 columns and vanilla `fetch()` JavaScript (using `textContent` to prevent XSS).
*   **Container & Security Requirements (`Dockerfile`)**:
    *   Must use a multi-stage build separating `uv` build tooling from the final runtime image.
    *   Final runtime stage must use a minimal non-root image (`gcr.io/distroless/python3-debian12:nonroot`) and run strictly as `USER nonroot` (never `root`).
    *   Zero hardcoded API keys, tokens, passwords, or secrets anywhere in source code or container definitions.
    *   Never expose `os.environ` or internal runtime configuration via API endpoints.
