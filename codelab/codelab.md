summary: Getting Started with Spec-Driven Development & the Elephant-Goldfish Model (EGM) in Antigravity
id: sdd-egm-antigravity
categories: AI, Web, Cloud
tags: antigravity, sdd, egm, fastapi, cloud-run
status: Published
authors: AlvarDev

# Spec-Driven Development with Antigravity & the Elephant-Goldfish Model (EGM)

## Overview
Duration: 0:05:00

Welcome to the hands-on workshop on **Spec-Driven Development (SDD)** with **Google Antigravity** and the **Elephant-Goldfish Model (EGM)**.

Instead of unstructured "vibe coding" (prompting an AI to write code directly and hoping for the best), Spec-Driven Development treats your **technical specification** as the single source of truth. In this workshop, you will take SDD a step further using the open-source [Elephant-Goldfish Model (EGM) plugin](https://github.com/google/elephant-goldfish-model):

* **The Elephant (Long-Horizon Context)**: Collaborates with you to brainstorm requirements, weigh architectural trade-offs, and draft a formal specification (`docs/designs/retropulse.md`)—without writing production code.
* **The Goldfish (Stateless Adversarial Reviewers)**: Isolated subagents spawned with **zero conversation history** that review your specification with fresh eyes to catch hidden assumptions, missing edge cases, and ambiguities before a single line of code is written.
* **You (The Architect)**: Make the architectural decisions, approve the specification, and govern alignment between your design and codebase using automated **drift detection**.

### What You Will Build
You will build **RetroPulse**, a lightweight Sprint Retrospective Board web application from a completely empty folder:
* **Backend**: Python managed with `uv` and **FastAPI** (`main.py`) with in-memory state.
* **Frontend**: A responsive 3-column single-page interface (`static/index.html`) built with vanilla HTML, CSS, and JavaScript (*Went Well*, *To Improve*, *Action Items*) with card creation and upvoting.
* **No Google Cloud Project Required**: Steps 1 through 6 run **100% locally** on your machine. Step 7 is an optional bonus for deploying your containerized app to **Google Cloud Run**.

### What You Will Learn
* How to turn a raw product idea into an anchored `concepts_brief.md` using `/egm:egm-brainstorm`.
* How to declare your tech stack (`uv` + FastAPI) and document rejected alternatives in `docs/designs/retropulse.md` using `/egm:egm-draft`.
* How to run stateless adversarial reviews on your specification using `/egm:egm-review`.
* How to generate a complete working application from a single-line prompt referencing your approved specification.
* How to detect both silent manual code edits and "vibe-coded" features using `/egm:egm-drift-report`.

### Prerequisites
* [Google Antigravity App](https://antigravity.google) installed on your machine.
* Python 3.10+ and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed locally.
* *(Optional for Step 7)* A Google Cloud Project with billing enabled and the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) installed.

---

## Step 1: Set Up Your Workspace & Install EGM
Duration: 0:05:00

You will start completely from scratch in an empty folder—no starter repository, no pre-written code, and no manual terminal setup required.

### 1. Create and Open an Empty Folder
1. Create a new empty folder on your computer named `retropulse`.
2. Open the **Antigravity App** and select **Open Folder...** to open `retropulse`.

### 2. Install the EGM Plugin
In the Antigravity App agent chat panel, install the open-source Elephant-Goldfish Model plugin by copying and pasting the following prompt (or using `/plugin`):

```text
Install https://github.com/google/elephant-goldfish-model
```

> aside positive
> **Tip:** If you also have the Antigravity CLI (`agy`) installed, you can install the plugin from any terminal with:
> `agy plugin install https://github.com/google/elephant-goldfish-model`

Once installed, start a fresh session or reload the window so the `/egm:*` skills (`egm-brainstorm`, `egm-draft`, `egm-review`, `egm-resolve`, and `egm-drift-report`) and Goldfish reviewer subagents are active.

---

## Step 2: Brainstorm with the Elephant (`/egm:egm-brainstorm`)
Duration: 0:10:00

In EGM, you never ask the agent to write code right away. Instead, you start an upstream ideation session with **the Elephant** using `/egm:egm-brainstorm`.

### 1. Start the Brainstorm Session
Copy and paste **Prompt 1** into the Antigravity chat:

```text
/egm:egm-brainstorm Build a Sprint Retro Board web application ("RetroPulse") where team members can post cards into three columns ("Went Well", "To Improve", "Action Items") and upvote cards.
```

### 2. Answer the Elephant's Clarifying Questions & Declare Your Tech Stack
Because the `retropulse` folder is completely empty, the Elephant does not yet know your target users, constraints, or which tech stack you want to use (`uv` + FastAPI vs. Golang or Node.js).

The Elephant will interview you in chat about your problem statement, users, constraints, non-goals, success metrics, and author name.

> aside positive
> **Where is your tech stack recorded?**
> When you answer the Elephant's questions in chat, your choices are **not** left in chat history. At the end of this step, the Elephant writes your answers directly into a file on disk called `concepts_brief.md` under `## Key Decisions & Staging for Next Steps` and `## Alternatives Weighed`.

Copy and paste **Prompt 2** to answer all of the Elephant's clarifying questions and declare your architecture in one turn:

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

### 3. Trigger the Goldfish Brainstorm Swarm
After reading your constraints, the Elephant summarizes the anchored hypothesis and presents a single-select confirmation gate in chat:

1. Select **`Review with Goldfishes`**.
2. Behind the scenes, the Elephant spawns **7 stateless Goldfish subagents in parallel** (*Contrarian/YAGNI*, *Cost & Quota*, *UX & Ergonomics*, *Migration*, *Observability*, *Tech Debt*, and *Inventive Catalyst*) to challenge your concept.
3. The Elephant synthesizes their findings and writes **`concepts_brief.md`** to your workspace.

### 4. Finalize the Brief and Hand Off to Drafting
The Elephant will highlight 2–3 edge cases raised by the Goldfish reviewers (such as handling invalid category names, concurrent upvote requests, or whitespace-only card text).

Copy and paste **Prompt 3** to align on those edge cases and finalize the brief:

```text
Keep the scope strictly minimal for v1: enforce category validation ("Went Well", "To Improve", "Action Items") and strip whitespace in the FastAPI Pydantic model so empty strings are rejected with HTTP 422. I am aligned with `concepts_brief.md`—let's finalize the brief.
```

When the handoff menu appears, select:
* **`Proceed to egm-draft (Initialize formal design document)`**

---

## Step 3: Draft the Specification (`/egm:egm-draft`)
Duration: 0:10:00

Now that `concepts_brief.md` is saved on disk, you will use `/egm:egm-draft` to turn the brief into a formal engineering specification (`docs/designs/retropulse.md`).

### 1. Start the Drafting Workflow
Copy and paste **Prompt 4** into the Antigravity chat:

```text
/egm:egm-draft
```

The Elephant automatically detects and reads `concepts_brief.md` from disk and asks for confirmation to start drafting. If prompted in chat to confirm, reply:

```text
Yes, proceed with drafting from concepts_brief.md.
```

### 2. Review and Approve the 4 Specification Sections
Instead of dumping a massive document into chat, `/egm:egm-draft` writes **`design_draft.md`** section by section, pausing after each section with a 2-option approval button so you remain in control:

1. **Checkpoint 1 — `Overview & Goals`**:
   * Writes `## Overview`, `## The Problem`, `## Goals`, `## Non-Goals`, and `## Critical User Journeys (CUJs)`.
   * Open `design_draft.md` in the side panel, verify that card deletion and card authors are listed under `Non-Goals`, and click:
     **`Approve Overview & Goals and proceed to next section`**
2. **Checkpoint 2 — `Technical Plan`**:
   * Appends `## Technical Plan (Architecture)`, documenting the FastAPI endpoints (`GET /api/cards`, `POST /api/cards`, `POST /api/cards/{id}/upvote`), the Pydantic model (`max_length=280`), in-memory storage, and `static/index.html`.
   * Review the architecture and click:
     **`Approve Technical Plan and proceed to next section`**
3. **Checkpoint 3 — `Alternatives Considered`**:
   * Appends `## Alternatives Considered`, permanently documenting why **Golang / Node.js** and **SQLite / external databases** were rejected in favor of Python (`uv` + FastAPI) and in-memory state.
   * Review and click:
     **`Approve Alternatives Considered and proceed to next section`**
4. **Checkpoint 4 — `Detailed Implementation`**:
   * Appends `## Detailed Implementation Plan`, listing **every exact file to create** (`pyproject.toml`, `main.py`, `static/index.html`, and tests) along with the `### Verification Plan` (`uv` commands).
   * Notice that **no production code is written yet**—only the blueprint. Click:
     **`Approve Detailed Implementation and proceed to next section`**

### 3. Save the Specification to `docs/designs/`
After the fourth checkpoint, the Elephant reconciles `design_draft.md` against `concepts_brief.md` and asks where to save the finalized specification.

Select:
* **`Save to detected directory: docs/designs/`**

Your specification is now saved on disk at `docs/designs/retropulse.md` (typically `docs/designs/retropulse.md`).

---

## Step 4: Stateless Review with Goldfish (`/egm:egm-review`)
Duration: 0:10:00

Why shouldn't the Elephant just review its own specification? Because the Elephant carries the entire conversation history and hidden biases from Steps 2 and 3.

Now you will invoke `/egm:egm-review` to spawn **stateless Goldfish subagents** with **zero conversation history**. They only see `docs/designs/retropulse.md`.

### 1. Launch `/egm:egm-review`
Copy and paste **Prompt 5** (adjusting the filename if your spec was saved under a slightly different name inside `docs/designs/`):

```text
/egm:egm-review docs/designs/retropulse.md
```

### 2. Provide Goldfish Context
Because this is a brand-new project with no existing source code files yet, when the agent asks if you want to provide additional `GoldfishContext` files, copy and paste **Prompt 6**:

```text
Proceed with no additional context files.
```

### 3. Choose the Review Execution Mode
EGM presents a 4-option preset menu:
* *Interactive review with all review rubrics* (runs all 5 stages with pauses)
* *Consolidated report with all review rubrics* (runs all 5 stages uninterrupted)
* *Feature spec only* (runs Stages 5–8 on architecture)
* *Implementation plan only* (runs Stage 9 on implementation readiness)

For this 1-hour workshop, select:
* **`Implementation plan only (evaluate design for implementation readiness)`**

> aside positive
> **What happens during Stage 9?**
> EGM spawns isolated subagents (`egm-implementation-readiness`, `egm-codebase-details`, and `egm-style`) in fresh contexts to verify that your `## Detailed Implementation Plan` in `docs/designs/retropulse.md` is unambiguous and complete enough for a zero-context coding agent to build without guessing.

### 4. Resolve Findings and Finalize the Spec
When the Goldfish review completes, it writes `implementation_readiness_report.md` and presents a checkpoint menu:
* If the report found any missing details you want fixed, select **`Resolve findings with agent (evaluate findings, propose fixes, and apply approved edits)`** (which runs `/egm:egm-resolve`) and approve the proposed fixes.
* Otherwise, select **`Conclude review and finalize document`**.

---

## Step 5: Build the App from the Approved Spec
Duration: 0:10:00

Look at your workspace: you now have a verified, self-contained specification in `docs/designs/retropulse.md` that defines `uv`, `fastapi`, `uvicorn`, `main.py`, `static/index.html`, the API routes, and the data validation rules (`max_length=280`).

Because everything is documented in `docs/designs/retropulse.md`, **you do not need to repeat your tech stack or requirements in the implementation prompt.**

### 1. Implement the Spec with a Single Sentence
Copy and paste **Prompt 7** into the Antigravity chat:

```text
Implement docs/designs/retropulse.md and start the local server on port 8000.
```

Watch what Antigravity does autonomously from that single line:
1. Reads `docs/designs/retropulse.md`.
2. Initializes the Python project with `uv` (`pyproject.toml`) and installs `fastapi` and `uvicorn`.
3. Creates `main.py` with the in-memory store, Pydantic validation (`max_length=280`), and REST endpoints.
4. Creates `static/index.html` with the 3-column layout (*Went Well*, *To Improve*, *Action Items*).
5. Starts the server with `uv run uvicorn main:app --host 0.0.0.0 --port 8000`.

### 2. Test RetroPulse in Your Browser
1. Open [http://localhost:8000](http://localhost:8000) in your browser.
2. Add a card to **Went Well**, **To Improve**, and **Action Items**.
3. Click the **Upvote (`+1`)** button on a card and verify the counter increments immediately.

---

## Step 6: Catch Spec-to-Code Drift (`/egm:egm-drift-report`)
Duration: 0:10:00

In real-world engineering, specifications often rot the moment someone makes a quick manual edit in the code or "vibe-codes" an urgent feature in a new chat session without updating the design doc.

EGM solves this with **`/egm:egm-drift-report`**, which audits your checked-in specifications (`docs/designs/`) against your actual source code.

### 1. Verify Zero Baseline Drift
First, verify that your v1 implementation matches `docs/designs/retropulse.md`. Copy and paste **Prompt 8**:

```text
/egm:egm-drift-report docs/designs/
```

Open the generated `{YYYY-MM-DD}_DRIFT_REPORT.md` file. Because the app was built strictly from `docs/designs/retropulse.md`, it reports:
* **`No drift detected.`**

### 2. Create Drift #1: A Silent 1-Line Manual Code Change
Let's simulate a developer silently changing a validation rule in the code:
1. Open `main.py` in the Antigravity App file editor.
2. Find the card text maximum character limit (`280`) in the Pydantic model or validation logic.
3. Manually change `280` to **`50`** and save `main.py`.

### 3. Create Drift #2: "Vibe Coding" a New Feature in a New Conversation
Now let's simulate an urgent feature request where a developer skips SDD and prompts the AI directly in a new chat:
1. Click **`+ New Conversation`** (or open a new chat thread) in the Antigravity App.
2. Copy and paste **Prompt 9** into the new conversation:

```text
In main.py and static/index.html, add an optional "author" field (defaulting to "Anonymous") to every card and display it on the card UI, and add a "Clear Board" button in the UI backed by a DELETE /api/cards endpoint.
```

3. Refresh [http://localhost:8000](http://localhost:8000) in your browser—you will see the new **Author** field and the **Clear Board** button working in the UI.

### 4. Run `/egm:egm-drift-report` to Catch Both Drifts!
Now run the drift detector by copying and pasting **Prompt 10**:

```text
/egm:egm-drift-report docs/designs/
```

Open `{YYYY-MM-DD}_DRIFT_REPORT.md`! EGM compares `docs/designs/retropulse.md` against `main.py` and `static/index.html` and catches **both** divergences red-handed:
1. **Logic / Validation Drift**: `main.py` enforces a `50`-character limit on card text instead of the `280`-character limit specified in `docs/designs/retropulse.md`.
2. **Undocumented Feature & Model Drift**: `main.py` and `static/index.html` include an undocumented `author` field and a `DELETE /api/cards` ("Clear Board") endpoint that contradicts the v1 specification's `Non-Goals`.

### 5. Reconcile the Specification and Code
In EGM, when drift is detected, the human architect decides whether to revert the code or update the spec. Here, we want to **fix the accidental `50`-character bug** back to `280`, while **officially adopting the new `author` and `Clear Board` features** in the specification.

Copy and paste **Prompt 11**:

```text
Reconcile the drift between docs/designs/retropulse.md and the codebase:
1. In main.py (and static/index.html if applicable), restore the maximum card text length back to 280 characters to match the specification.
2. Update docs/designs/retropulse.md to officially document the optional "author" field (default "Anonymous") and the DELETE /api/cards "Clear Board" feature.
3. Re-run /egm:egm-drift-report docs/designs/ to verify that zero drift remains.
```

Inspect `{YYYY-MM-DD}_DRIFT_REPORT.md`—your specification and codebase are once again 100% synchronized (`No drift detected.`)!

---

## Step 7: (Optional Bonus) Containerize & Deploy to Cloud Run
Duration: 0:05:00

> aside negative
> **Optional Step:** This final step requires a **Google Cloud Project** with billing enabled and the `gcloud` CLI authenticated on your machine. If you do not have a Google Cloud Project, you can still generate and inspect the production `Dockerfile` locally!

To deploy RetroPulse following [Google Cloud Run security best practices](https://cloud.google.com/run/docs/securing/service-identity), we will:
* Package the app using a lightweight **multi-stage Dockerfile** with a non-root [Google Distroless Python runtime image](https://cloud.google.com/containers/docs/securing-containers).
* Deploy to the `southamerica-east1` region using a **dedicated, least-privilege Service Account** (never the default Compute Engine service account).

### 1. Generate the Multi-Stage Dockerfile & Deploy
Copy and paste **Prompt 12** into Antigravity (replacing `YOUR_GCP_PROJECT_ID` if you are deploying to Google Cloud):

```text
Update docs/designs/retropulse.md and the project to include a production multi-stage Dockerfile optimized for size (using python:3.12-slim with uv as the builder stage and gcr.io/distroless/python3-debian12:nonroot as the final runtime stage, listening on PORT=8080).

If I provide a Google Cloud Project ID (YOUR_GCP_PROJECT_ID), give me the exact gcloud commands to:
1. Create a dedicated least-privilege service account `retropulse-sa`.
2. Build and deploy the container to Cloud Run in `southamerica-east1` using `--service-account=retropulse-sa@YOUR_GCP_PROJECT_ID.iam.gserviceaccount.com`.
```

### Congratulations!
You have built a complete web application from scratch using **Spec-Driven Development (SDD)** in **Antigravity** and the **Elephant-Goldfish Model (EGM)**—brainstorming with the Elephant, reviewing with stateless Goldfish subagents, building from a single source-of-truth specification, and catching code drift automatically with `/egm:egm-drift-report`.
