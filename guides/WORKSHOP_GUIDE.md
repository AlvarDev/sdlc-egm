# Hands-On Workshop Guide: Spec-Driven Development with Antigravity & EGM

> **Duration:** 60 Minutes  
> **App Built:** **RetroPulse** — A 3-Column Sprint Retrospective Board (`uv` + FastAPI + Vanilla HTML/CSS/JS)  
> **Cloud Requirement:** None for Steps 1–6 (100% local). Step 7 is an optional bonus for Google Cloud Run.

---

## Architecture & Workflow Overview

```mermaid
sequenceDiagram
    autonumber
    actor Dev as You (Architect)
    participant Elephant as Elephant (Brainstorm & Draft)
    participant Docs as Markdown Artifacts (On Disk)
    participant Goldfish as Goldfish Subagents (Zero Context)
    participant Coder as Antigravity Implementation Agent

    Dev->>Elephant: /egm:egm-brainstorm (Idea + Tech Stack Constraints)
    Elephant->>Goldfish: Spawn 7-Lens Brainstorm Swarm
    Elephant->>Docs: Save concepts_brief.md
    Dev->>Elephant: /egm:egm-draft (4 Section Checkpoints)
    Elephant->>Docs: Save docs/designs/retropulse.md
    Dev->>Goldfish: /egm:egm-review docs/designs/retropulse.md
    Goldfish->>Docs: Save implementation_readiness_report.md
    Dev->>Coder: "Implement docs/designs/retropulse.md"
    Coder->>Docs: Generate main.py + static/index.html
    Dev->>Elephant: /egm:egm-drift-report docs/designs/
```

---

## Step 1: Set Up Your Workspace & Install EGM (5 min)

1. Create a brand-new, empty folder on your machine named `retropulse`.
2. Open the **Antigravity App** and open the empty `retropulse` folder (**File > Open Folder...**).
3. In the Antigravity chat panel, install the [Elephant-Goldfish Model (EGM) plugin](https://github.com/google/elephant-goldfish-model) by copying and pasting:

```text
Install https://github.com/google/elephant-goldfish-model
```

*(Alternatively, run `/plugin` in the Antigravity App or `agy plugin install https://github.com/google/elephant-goldfish-model` in the CLI).*

4. Start a new chat or reload the window so the `/egm:*` commands are available.

---

## Step 2: Brainstorm with the Elephant (`/egm:egm-brainstorm`) (10 min)

### 2.1 Pitch the Product Concept
Copy and paste **Prompt 1** into the Antigravity chat:

```text
/egm:egm-brainstorm Build a Sprint Retro Board web application ("RetroPulse") where team members can post cards into three columns ("Went Well", "To Improve", "Action Items") and upvote cards.
```

### 2.2 Answer Clarifying Questions & Declare Your Tech Stack
The Elephant will interview you in chat about your target users, constraints, non-goals, success metrics, and author name.

> [!IMPORTANT]
> **Why declare `uv` and `FastAPI` here?**  
> Because your folder is empty, you must tell the Elephant which language and framework to use (e.g., Python with `uv` + FastAPI instead of Golang or Node.js). The Elephant writes your answers directly to disk inside **`concepts_brief.md`** (`## Key Decisions & Staging for Next Steps` and `## Alternatives Weighed`), so your choices become a permanent project record rather than getting lost in chat history.

Copy and paste **Prompt 2**:

```text
Here are our answers and architectural constraints:
- Author: Workshop Attendee
- Problem & Users: A single engineering team (up to 20 people) needs a fast, zero-setup board during live sprint retrospectives without logging into heavy project management tools.
- Tech Stack Choice: Python managed with `uv`, using `fastapi` and `uvicorn` (chosen over Golang or Node.js for rapid Pydantic schema validation), serving a single-page frontend in `static/index.html` built with vanilla HTML, CSS, and JavaScript.
- Storage Constraint: Strictly in-memory Python list/dict in `main.py` (no SQLite, Postgres, or external databases; resetting on server restart is expected).
- Functional Rules: Each card has `id`, `text` (non-empty, max 280 characters), `category` ("Went Well", "To Improve", or "Action Items"), and `votes` (integer starting at 0, incrementing by +1 per upvote).
- Out of Scope (Non-Goals for v1): No user authentication, no card deletion, no card editing, no author field on cards.
- Success Metric: Users can open `http://localhost:8000`, create cards in any of the 3 columns, and upvote cards with sub-100ms response time.
```

### 2.3 Run the Goldfish Brainstorm Swarm
1. When the Readiness Gate appears, select **`Review with Goldfishes`**.
2. Wait as the Elephant spawns 7 stateless Goldfish subagents in parallel and writes **`concepts_brief.md`** to your workspace.
3. When the Elephant highlights 2–3 edge-case objections in chat, copy and paste **Prompt 3**:

```text
Keep the scope strictly minimal for v1: enforce category validation ("Went Well", "To Improve", "Action Items") and strip whitespace in the FastAPI Pydantic model so empty strings are rejected with HTTP 422. I am aligned with `concepts_brief.md`—let's finalize the brief.
```

4. At the handoff gate, select **`Proceed to egm-draft (Initialize formal design document)`**.

---

## Step 3: Draft the Specification (`/egm:egm-draft`) (10 min)

### 3.1 Start Drafting
Copy and paste **Prompt 4**:

```text
/egm:egm-draft
```

*(If asked in chat to confirm starting from `concepts_brief.md`, reply: `Yes, proceed with drafting from concepts_brief.md.`)*

### 3.2 Approve the 4 Interactive Checkpoints
The Elephant builds `design_draft.md` across 4 sequential checkpoints. Review `design_draft.md` in the side panel at each step and click the approval option:

| Checkpoint | Section Added to `design_draft.md` | Action to Select |
| :--- | :--- | :--- |
| **1. Overview & Goals** | `Overview`, `The Problem`, `Goals`, `Non-Goals`, `Critical User Journeys (CUJs)` | `Approve Overview & Goals and proceed to next section` |
| **2. Technical Plan** | `Technical Plan (Architecture)`: `uv` + FastAPI routes (`GET /api/cards`, `POST /api/cards`, `POST /api/cards/{id}/upvote`), Pydantic model (`max_length=280`), `static/index.html` | `Approve Technical Plan and proceed to next section` |
| **3. Alternatives** | `Alternatives Considered`: Documents why Golang, Node.js, and external DBs were rejected | `Approve Alternatives Considered and proceed to next section` |
| **4. Implementation** | `Detailed Implementation Plan`: Lists exact files (`pyproject.toml`, `main.py`, `static/index.html`) and `Verification Plan` (`uv` commands) | `Approve Detailed Implementation and proceed to next section` |

### 3.3 Save the Specification
When prompted where to save the finalized specification, select:
* **`Save to detected directory: docs/designs/`**

This saves your specification to **`docs/designs/retropulse.md`**.

---

## Step 4: Stateless Review with Goldfish (`/egm:egm-review`) (10 min)

1. Copy and paste **Prompt 5** to start the stateless subagent review:

```text
/egm:egm-review docs/designs/retropulse.md
```

2. When asked if you want to provide additional `GoldfishContext` files, copy and paste **Prompt 6**:

```text
Proceed with no additional context files.
```

3. At the **Review Execution Mode** selector, choose:
   * **`Implementation plan only (evaluate design for implementation readiness)`**
4. Once `implementation_readiness_report.md` is generated:
   * Choose **`Resolve findings with agent`** if you want the Elephant to patch any flagged gaps in `docs/designs/retropulse.md`, or
   * Choose **`Conclude review and finalize document`**.

---

## Step 5: Build the App from the Approved Spec (10 min)

Because `docs/designs/retropulse.md` already documents `uv`, `fastapi`, `uvicorn`, `main.py`, `static/index.html`, and the validation rules, your implementation prompt is a single sentence!

### 5.1 Implement the Specification
Copy and paste **Prompt 7**:

```text
Implement docs/designs/retropulse.md and start the local server on port 8000.
```

### 5.2 Test the App Locally
1. Open [http://localhost:8000](http://localhost:8000) in your browser.
2. Create cards in **Went Well**, **To Improve**, and **Action Items**.
3. Click the **Upvote** button on several cards to confirm votes increment properly.

---

## Step 6: Experience `/egm:egm-drift-report` (10 min)

Now you will test EGM's drift detection against **two types of real-world drift**:
1. A **silent 1-line manual edit** in `main.py`.
2. An **undocumented "vibe-coded" feature** added in a new chat conversation.

### 6.1 Verify Zero Baseline Drift
Copy and paste **Prompt 8**:

```text
/egm:egm-drift-report docs/designs/
```

Open `{YYYY-MM-DD}_DRIFT_REPORT.md` and verify that it says:
* **`No drift detected.`**

### 6.2 Drift #1 — Make a Manual 1-Line Edit in `main.py`
1. Open `main.py` in the Antigravity editor.
2. Locate the maximum character length for card text (`280`).
3. Manually change `280` to **`50`** and save `main.py`.

### 6.3 Drift #2 — "Vibe Code" a Feature in a New Conversation
1. Click **`+ New Conversation`** in the Antigravity App (simulating a developer jumping in to code an urgent request without consulting `docs/designs/retropulse.md`).
2. Copy and paste **Prompt 9** into the new conversation:

```text
In main.py and static/index.html, add an optional "author" field (defaulting to "Anonymous") to every card and display it on the card UI, and add a "Clear Board" button in the UI backed by a DELETE /api/cards endpoint.
```

3. Refresh [http://localhost:8000](http://localhost:8000) in your browser and verify the new **Author** input and **Clear Board** button work.

### 6.4 Catch Both Drifts with `/egm:egm-drift-report`
Copy and paste **Prompt 10**:

```text
/egm:egm-drift-report docs/designs/
```

Open `{YYYY-MM-DD}_DRIFT_REPORT.md`! Notice that EGM caught **both** divergences:
1. **Manual Code Drift**: `main.py` restricts card text to `50` characters instead of the `280` characters required by `docs/designs/retropulse.md`.
2. **Vibe-Coded Feature Drift**: `main.py` and `static/index.html` contain an undocumented `author` field and a `DELETE /api/cards` endpoint that violates the v1 `Non-Goals`.

### 6.5 Reconcile Spec & Code
Copy and paste **Prompt 11** to fix the `50`-character bug in code and officially adopt the `author` and `Clear Board` features in `docs/designs/retropulse.md`:

```text
Reconcile the drift between docs/designs/retropulse.md and the codebase:
1. In main.py (and static/index.html if applicable), restore the maximum card text length back to 280 characters to match the specification.
2. Update docs/designs/retropulse.md to officially document the optional "author" field (default "Anonymous") and the DELETE /api/cards "Clear Board" feature.
3. Re-run /egm:egm-drift-report docs/designs/ to verify that zero drift remains.
```

---

## Step 7 (Optional Bonus): Deploy to Cloud Run (5 min)

> [!NOTE]
> Requires a Google Cloud Project with billing enabled and `gcloud` installed. Even without a GCP project, you can run this prompt to generate and inspect the multi-stage Distroless `Dockerfile` locally.

Copy and paste **Prompt 12** (replace `YOUR_GCP_PROJECT_ID` if deploying):

```text
Update docs/designs/retropulse.md and the project to include a production multi-stage Dockerfile optimized for size (using python:3.12-slim with uv as the builder stage and gcr.io/distroless/python3-debian12:nonroot as the final runtime stage, listening on PORT=8080).

If I provide a Google Cloud Project ID (YOUR_GCP_PROJECT_ID), give me the exact gcloud commands to:
1. Create a dedicated least-privilege service account `retropulse-sa`.
2. Build and deploy the container to Cloud Run in `southamerica-east1` using `--service-account=retropulse-sa@YOUR_GCP_PROJECT_ID.iam.gserviceaccount.com`.
```
