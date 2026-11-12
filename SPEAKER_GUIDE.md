# Speaker & Facilitator Guide: SDD with Antigravity & EGM

This guide covers both parts of your 90-minute session:
* **Part 1 (30 Minutes)**: Presentation — *Spec-Driven Development (SDD) in Antigravity, the Elephant-Goldfish Model (EGM), and How They Connect to CI/CD*.
* **Part 2 (60 Minutes)**: Hands-on Workshop — *Building "RetroPulse" from Scratch with Antigravity & EGM (`codelab.md` / `WORKSHOP_GUIDE.md`)*.
* **Appendix**: Golden Reference Artifacts (`docs/designs/retropulse.md`, `main.py`, `static/index.html`, and `Dockerfile`) in case you need a live backup during the session.

---

## Part 1: 30-Minute Presentation Outline & Talking Points

### Slide-by-Slide Arc (30 Minutes Total)

#### Section 1: The Trap of "Vibe Coding" in the Era of AI CI/CD (00:00 – 05:00)
* **Core Message**: AI agents can generate 1,000 lines of code in 30 seconds, which shifts the engineering bottleneck from *writing code* to *verifying intent and architecture*.
* **The 4 Failure Modes of Unstructured Prompting**:
  1. **Context Collapse & Hallucination Cascades**: Long chat threads accumulate outdated assumptions.
  2. **"Weeds Syndrome" (Premature Implementation)**: Agents start editing files immediately before evaluating simplicity (YAGNI) or architecture.
  3. **Chat Dump Fatigue**: Reviewing 300-line plans inside a scrolling chat box is unmanageable.
  4. **CI/CD Overload**: If you feed unstructured "vibe-coded" PRs into a CI/CD pipeline, you just ship bugs and tech debt faster.

#### Section 2: Spec-Driven Development (SDD) with Antigravity (05:00 – 12:00)
* **Core Message**: Shift from `Prompt → Code` to `Requirement → Spec → Plan → Verified Code`.
* **What Changes in SDD**:
  * The **Specification (`docs/designs/<feature>.md`)** is a checked-in, version-controlled artifact in Git—not ephemeral chat history.
  * When your spec contains the problem statement, non-goals, architecture, and exact file boundaries, a brand-new coding agent session can implement the entire feature from a one-sentence prompt: `"Implement docs/designs/<feature>.md"`.

#### Section 3: Bonus Power-Up — The Elephant-Goldfish Model (EGM) (12:00 – 22:00)
* **References**:
  * [Introducing the Elephant-Goldfish Model Plugin (Google Open Source Blog)](https://opensource.googleblog.com/2026/10/introducing-elephant-goldfish-model-plugin.html)
  * [Elephants, Goldfish, and the New Golden Age of Software Engineering (Dave Rensin)](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874)
  * [EGM GitHub Repository (`google/elephant-goldfish-model`)](https://github.com/google/elephant-goldfish-model)
* **Why Vanilla SDD Isn't Enough**:
  * If the **same agent session** interviews you, writes the spec, and reviews its own spec, it suffers from **confirmation bias**—it validates its own blind spots.
* **The Three Roles in EGM**:
  1. **The Elephant (`/egm:egm-brainstorm`, `/egm:egm-draft`)**: Holds deep, long-horizon context. Interviews the human, records architectural decisions into `concepts_brief.md`, and drafts `docs/designs/<feature>.md` section by section. **Writes zero production code.**
  2. **The Goldfish (`/egm:egm-review`)**: Stateless adversarial subagents spawned with **zero conversation history**. They only read the spec on disk and attack it across 5 stages (*Zoom Out/YAGNI*, *Naive Reader Comprehension*, *Hostile Design Critic*, *Intermediate Zoom Out*, and *Implementation Readiness*).
  3. **The Human (Architect)**: Makes every architectural choice (such as choosing Python + `uv` + FastAPI over Golang) and owns the outcome.

#### Section 4: How SDD + EGM Connect to CI/CD (22:00 – 30:00)
* **Note for Speaker**: Even though we won't build a CI/CD pipeline during today's 1-hour workshop, show attendees how SDD + EGM plugs into the broader **CI/CD with AI** lifecycle:
  1. **Shift-Left CI (Spec PRs Before Code PRs)**: Just as traditional CI runs unit tests and linters on code, `/egm:egm-review` acts as an automated **pre-implementation quality gate** on design PRs.
  2. **File-Boundary Enforcement in CI**: Stage 9 of `/egm:egm-review` locks down the exact `Target Files to Create/Modify` list in the spec. A CI check can verify that an implementation PR only touches files authorized by the spec.
  3. **Continuous Spec Drift Detection (`/egm:egm-drift-report`)**: In traditional teams, design docs rot the week after launch. Running `/egm:egm-drift-report` (locally or in CI) compares `docs/designs/*.md` against the codebase and fails if someone "vibe-codes" an undocumented endpoint or changes a validation rule without updating the spec.

---

## Part 2: 60-Minute Workshop Facilitation Runbook

### Timing & Pacing Table

| Time | Workshop Step | Facilitator Tips & What to Watch For |
| :--- | :--- | :--- |
| **00–05m** | **Step 1: Empty Folder & Install EGM** | Ensure attendees open a completely empty `retropulse` folder in the **Antigravity App**. Remind them: no terminal commands needed! |
| **05–15m** | **Step 2: `/egm:egm-brainstorm`** | Point out how **Prompt 2** answers the Elephant's clarifying questions *and* declares `uv` + `FastAPI` over Golang. Open `concepts_brief.md` on screen once generated to show attendees that their stack choice is now saved on disk under `## Key Decisions` and `## Alternatives Weighed`. |
| **15–25m** | **Step 3: `/egm:egm-draft`** | Walk attendees through clicking **`Approve [Section Name] and proceed to next section`** across the 4 gates (`Overview & Goals` $\rightarrow$ `Technical Plan` $\rightarrow$ `Alternatives Considered` $\rightarrow$ `Detailed Implementation`). Emphasize that the Elephant is forbidden from writing `.py` or `.html` files during this phase. |
| **25–35m** | **Step 4: `/egm:egm-review`** | Have attendees select **`Implementation plan only`** at the preset menu so the review finishes in ~2 minutes. Explain that in production they can run the full 5-stage `Interactive` or `Consolidated` review. |
| **35–45m** | **Step 5: Implement from Spec** | Highlight the magic of **Prompt 7**: `"Implement docs/designs/retropulse.md and start the local server on port 8000."` Because everything is in `docs/designs/retropulse.md`, we don't repeat `uv`, `FastAPI`, or `index.html` in the prompt! |
| **45–55m** | **Step 6: `/egm:egm-drift-report`** | **The "Aha!" Moment**:<br>1) Run `/egm:egm-drift-report docs/designs/` $\rightarrow$ `No drift detected.`<br>2) Have attendees manually edit `280` $\rightarrow$ `50` in `main.py`.<br>3) Have attendees open a **`+ New Conversation`** and paste **Prompt 9** to vibe-code the `author` field and `DELETE /api/cards` button.<br>4) Run `/egm:egm-drift-report docs/designs/` and show how EGM catches *both* the `50`-char manual tweak and the undocumented feature! |
| **55–60m** | **Step 7: Optional Cloud Run Bonus** | Demo or walk through **Prompt 12** showing the multi-stage Distroless `Dockerfile` and least-privilege Service Account deployment to `southamerica-east1`. |

---

## Appendix: Golden Reference Checkpoints

If an attendee falls behind or hits a network/quota issue during the live workshop, you can share any of these reference files so they can jump straight to Step 5 or Step 6.

### 1. Reference Specification (`docs/designs/retropulse.md`)

```markdown
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

*   **Server Startup**: `uv run uvicorn main.py:app --host 0.0.0.0 --port 8000`
*   **API Smoke Check**: Verify `GET /api/cards`, `POST /api/cards` (including >280 char rejection with HTTP 422), and `POST /api/cards/1/upvote`.

--------------------------------------------------------------------------------

*Drafted with EGM*
```

---

### 2. Reference Backend (`main.py` — v1 Spec-Compliant)

```python
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="RetroPulse")

CardCategory = Literal["Went Well", "To Improve", "Action Items"]


class CardCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=280)
    category: CardCategory

    @field_validator("text", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v


class Card(BaseModel):
    id: int
    text: str
    category: CardCategory
    votes: int = 0


cards_db: list[Card] = []
next_id: int = 1


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/cards", response_model=list[Card])
def list_cards() -> list[Card]:
    return cards_db


@app.post("/api/cards", response_model=Card, status_code=201)
def create_card(payload: CardCreate) -> Card:
    global next_id
    card = Card(
        id=next_id,
        text=payload.text,
        category=payload.category,
        votes=0,
    )
    next_id += 1
    cards_db.append(card)
    return card


@app.post("/api/cards/{card_id}/upvote", response_model=Card)
def upvote_card(card_id: int) -> Card:
    for card in cards_db:
        if card.id == card_id:
            card.votes += 1
            return card
    raise HTTPException(status_code=404, detail="Card not found")
```

---

### 3. Reference Frontend (`static/index.html` — v1 Spec-Compliant)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RetroPulse — Sprint Retro Board</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --border: #e2e8f0;
      --primary: #2563eb;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    header { margin-bottom: 1.5rem; }
    h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
    p.subtitle { color: var(--muted); }
    form {
      display: flex;
      gap: 0.75rem;
      background: var(--card-bg);
      padding: 1rem;
      border-radius: 0.5rem;
      border: 1px solid var(--border);
      margin-bottom: 2rem;
    }
    input[type="text"] {
      flex: 1;
      padding: 0.6rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 0.375rem;
      font-size: 0.95rem;
    }
    select, button {
      padding: 0.6rem 1rem;
      border-radius: 0.375rem;
      border: 1px solid var(--border);
      font-size: 0.95rem;
      cursor: pointer;
    }
    button.primary {
      background: var(--primary);
      color: white;
      border: none;
      font-weight: 600;
    }
    .board {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.25rem;
    }
    .column {
      background: #f1f5f9;
      padding: 1rem;
      border-radius: 0.5rem;
      min-height: 400px;
    }
    .column h2 {
      font-size: 1.1rem;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--border);
    }
    .card {
      background: var(--card-bg);
      padding: 0.85rem;
      border-radius: 0.375rem;
      border: 1px solid var(--border);
      margin-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
    }
    .upvote-btn {
      background: #eff6ff;
      color: var(--primary);
      border: 1px solid #bfdbfe;
      padding: 0.35rem 0.65rem;
      border-radius: 999px;
      font-weight: 600;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <header>
    <h1>RetroPulse</h1>
    <p class="subtitle">Lightweight Sprint Retrospective Board</p>
  </header>

  <form id="card-form">
    <input
      type="text"
      id="card-text"
      placeholder="Share a thought (max 280 chars)..."
      maxlength="280"
      required
    />
    <select id="card-category">
      <option value="Went Well">Went Well</option>
      <option value="To Improve">To Improve</option>
      <option value="Action Items">Action Items</option>
    </select>
    <button type="submit" class="primary">Add Card</button>
  </form>

  <section class="board">
    <div class="column">
      <h2>Went Well</h2>
      <div id="col-Went Well"></div>
    </div>
    <div class="column">
      <h2>To Improve</h2>
      <div id="col-To Improve"></div>
    </div>
    <div class="column">
      <h2>Action Items</h2>
      <div id="col-Action Items"></div>
    </div>
  </section>

  <script>
    const categories = ["Went Well", "To Improve", "Action Items"];

    async function loadCards() {
      const res = await fetch("/api/cards");
      const cards = await res.json();
      categories.forEach((cat) => {
        document.getElementById(`col-${cat}`).innerHTML = "";
      });
      cards.forEach((card) => {
        const col = document.getElementById(`col-${card.category}`);
        if (!col) return;
        const el = document.createElement("div");
        el.className = "card";
        const span = document.createElement("span");
        span.textContent = card.text;
        const btn = document.createElement("button");
        btn.className = "upvote-btn";
        btn.textContent = `▲ ${card.votes}`;
        btn.onclick = () => upvoteCard(card.id);
        el.appendChild(span);
        el.appendChild(btn);
        col.appendChild(el);
      });
    }

    async function upvoteCard(id) {
      await fetch(`/api/cards/${id}/upvote`, { method: "POST" });
      await loadCards();
    }

    document.getElementById("card-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = document.getElementById("card-text");
      const category = document.getElementById("card-category").value;
      const res = await fetch("/api/cards", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input.value, category }),
      });
      if (res.ok) {
        input.value = "";
        await loadCards();
      }
    });

    loadCards();
  </script>
</body>
</html>
```

---

### 4. Reference Multi-Stage Distroless `Dockerfile` & Cloud Run Commands (Step 7 Bonus)

```dockerfile
# Stage 1: Build dependencies using uv
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project --no-dev --no-config --index-url https://pypi.org/simple

COPY main.py ./
COPY static ./static

# Stage 2: Minimal non-root Google Distroless runtime
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /app/.venv/lib/python3.12/site-packages /app/site-packages
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/static /app/static

ENV PYTHONPATH="/app/site-packages" \
    PORT=8080

EXPOSE 8080
USER nonroot

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Cloud Run Deployment Commands (`southamerica-east1` with Dedicated Service Account)

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="southamerica-east1"
export SERVICE_NAME="retropulse"
export SA_NAME="retropulse-sa"

# 1. Create a dedicated least-privilege Service Account
gcloud iam service-accounts create "${SA_NAME}" \
  --display-name="RetroPulse Cloud Run Service Account" \
  --project="${PROJECT_ID}"

# 2. Deploy from source to Cloud Run in southamerica-east1
gcloud run deploy "${SERVICE_NAME}" \
  --source=. \
  --region="${REGION}" \
  --service-account="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --allow-unauthenticated \
  --project="${PROJECT_ID}"
```
