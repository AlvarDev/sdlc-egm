# RetroPulse — Lightweight Sprint Retrospective Board

*   **Author:** Workshop Attendee
*   **Status:** Approved
*   **Date:** 2026-11-12

--------------------------------------------------------------------------------

## Overview

RetroPulse is a lightweight, single-page Sprint Retrospective web application built with Python (`uv` and FastAPI) and a vanilla HTML/CSS/JS frontend. It enables a single engineering team (up to 20 participants) to post cards across three retrospective columns ("Went Well", "To Improve", "Action Items") and upvote cards in real time using in-memory storage.

## The Problem

Engineering teams running live sprint retrospectives often face friction with heavyweight project management tools that require account creation, complex board setup, or database provisioning. RetroPulse solves this by providing a zero-setup local web application with instant card creation and upvoting.

## Goals

*   Provide a 3-column web interface ("Went Well", "To Improve", "Action Items") served at `http://localhost:8000`.
*   Allow users to create cards with non-empty text up to 280 characters in any of the three categories.
*   Allow users to upvote existing cards, incrementing the card's vote count by 1 per click.
*   Maintain all state in memory inside the FastAPI process with sub-100ms response times.

## Non-Goals

*   Persistent database or file storage (state resets on server restart).
*   User authentication, accounts, or author attribution on cards.
*   Editing or deleting existing cards.
*   Multiple boards or rooms.

## Critical User Journeys (CUJs)

### CUJ 1: Post a Retrospective Card

*   **Given**: The RetroPulse server is running and the user opens `http://localhost:8000`.
*   **When**: The user enters card text (1–280 characters after trimming whitespace), selects a category ("Went Well", "To Improve", or "Action Items"), and submits the form.
*   **Then**: `POST /api/cards` returns HTTP 201 with the created card (`id`, `text`, `category`, `votes: 0`), and the card renders immediately in the corresponding column.

### CUJ 2: Upvote a Card

*   **Given**: At least one card exists on the board.
*   **When**: The user clicks the Upvote (`+1`) button on a card.
*   **Then**: `POST /api/cards/{card_id}/upvote` increments `votes` by 1, returns HTTP 200 with the updated card, and updates the UI badge.

## Technical Plan (Architecture)

*   **Environment & Package Management**: Python 3.10+ managed via `uv` (`pyproject.toml`), with dependencies restricted to `fastapi` and `uvicorn`.
*   **Backend (`main.py`)**:
    *   In-memory store: Python `list[Card]` and integer auto-increment counter.
    *   Pydantic Models:
        *   `CardCategory`: `Literal["Went Well", "To Improve", "Action Items"]`
        *   `CardCreate`: `text: str` (stripped of leading/trailing whitespace, `min_length=1`, `max_length=280`), `category: CardCategory`
        *   `Card`: `id: int`, `text: str`, `category: CardCategory`, `votes: int = 0`
    *   API Endpoints:
        *   `GET /` -> Serves `static/index.html`.
        *   `GET /api/cards` -> Returns `list[Card]` (HTTP 200).
        *   `POST /api/cards` -> Validates `CardCreate`, appends new `Card` with `votes=0`, returns `Card` (HTTP 201).
        *   `POST /api/cards/{card_id}/upvote` -> Increments `votes` by 1 and returns `Card` (HTTP 200), or HTTP 404 if `card_id` is not found.
*   **Frontend (`static/index.html`)**:
    *   Single self-contained HTML5 file using CSS Grid for the 3 columns and vanilla `fetch()` JavaScript to load, create, and upvote cards.

## Alternatives Considered

### Alternative A: Golang (`net/http`) or Node.js (`Express`) Backend

*   **Pros**: Single static binary in Go; shared JS language in Node.
*   **Cons**: Requires manual request validation boilerplate compared to FastAPI's built-in Pydantic validation.
*   **Reason for Rejection**: Rejected by author: Python with `uv` and FastAPI provides built-in schema validation (`min_length=1`, `max_length=280`, `Literal` categories) and automatic OpenAPI docs with minimal code.

### Alternative B: SQLite or PostgreSQL Persistence

*   **Pros**: Retains cards across server restarts.
*   **Cons**: Adds schema migration and file/container state complexity unnecessary for a single live retro session.
*   **Reason for Rejection**: Rejected by author: In-memory Python storage satisfies the zero-setup constraint for v1.

--------------------------------------------------------------------------------

## Detailed Implementation Plan

### Target Files to Create/Modify

#### 1. `pyproject.toml` (Create)

*   **Type / Scope**: `uv` Project Configuration
*   **Proposed Changes**: Initialize project metadata and declare `fastapi` and `uvicorn` dependencies via `uv init` and `uv add fastapi uvicorn`.

#### 2. `main.py` (Create)

*   **Type / Scope**: FastAPI Backend Service
*   **Proposed Changes**: Implement `CardCategory`, `CardCreate` (with whitespace stripping and `min_length=1`, `max_length=280`), `Card`, in-memory storage, `GET /`, `GET /api/cards`, `POST /api/cards`, and `POST /api/cards/{card_id}/upvote`.

#### 3. `static/index.html` (Create)

*   **Type / Scope**: Single-Page Web Frontend
*   **Proposed Changes**: Implement the card creation form, 3-column CSS Grid ("Went Well", "To Improve", "Action Items"), and vanilla JS functions `loadCards()`, `createCard()`, and `upvoteCard(id)`.

### Verification Plan

*   **Server Startup**: `uv run uvicorn main:app --host 0.0.0.0 --port 8000`
*   **API Smoke Check**: Verify `GET /api/cards`, `POST /api/cards` (including >280 char rejection with HTTP 422), and `POST /api/cards/1/upvote`.

--------------------------------------------------------------------------------

*Drafted with EGM*
