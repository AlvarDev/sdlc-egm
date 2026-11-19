# Speaker & Facilitator Guide: Deploying CI/CD Pipelines with Antigravity & the Antigravity SDK

> **Session Structure:** 20-Minute Presentation + 60-Minute Hands-On Codelab  
> **Interactive Codelab URL:** `https://alvardev.github.io/sdlc-egm/gitlab-ci/`  
> **Golden Reference Code:** [`reference-gitlab-ci/`](../reference-gitlab-ci/)

---

## 🧭 Modern GitLab UI Refresher Cheat Sheet (For Speakers Returning to GitLab)

GitLab reorganized its left sidebar navigation recently. Here is where every single menu lives today so you can navigate smoothly on screen:

| Task in Workshop | Exact Modern GitLab Click Path | Watch Out For (Common Gotcha!) |
| :--- | :--- | :--- |
| **1. Create / Import Project** | Top-right **`+`** icon $\rightarrow$ **New project/repository** $\rightarrow$ **Import project** $\rightarrow$ **Repository by URL** | If corporate firewall blocks GitHub URL imports, choose **Create blank project** (uncheck *Initialize repository with a README*), `git clone` `retropulse-starter` locally, `git remote set-url origin <GITLAB_URL>`, and `git push -u origin main`. |
| **2. Add `GEMINI_API_KEY` Secret** | Left sidebar: **Settings** $\rightarrow$ **CI/CD** $\rightarrow$ expand **Variables** $\rightarrow$ **Add variable** | **CRITICAL:** Check **Masked**, and **UNCHECK "Protect variable"**! GitLab checks "Protect variable" by default—if left checked, Merge Request branches (`feat/quick-hack`) will NOT receive `GEMINI_API_KEY` and will fail with `ERROR: Set GEMINI_API_KEY`. |
| **3. View Pipeline Runs** | Left sidebar: **Build** $\rightarrow$ **Pipelines** *(used to be called "CI/CD > Pipelines" in older GitLab)* | Click any status pill (`Passed` / `Running` / `Failed`) to see the visual stage graph (`unit-tests` $\rightarrow$ `antigravity-ai-gate`). |
| **4. Open Merge Requests** | Left sidebar: **Code** $\rightarrow$ **Merge requests** *(or click the blue **Create merge request** banner right after `git push`)* | Inside an MR, click the **Pipelines** tab right below the MR title to watch stages run live. |
| **5. View `DRIFT_REPORT.md` Artifact** | Click the `antigravity-ai-gate` job $\rightarrow$ right-hand sidebar under **Job artifacts** $\rightarrow$ click **Browse** $\rightarrow$ click `DRIFT_REPORT.md` | Because `.gitlab-ci.yml` sets `when: always` under `artifacts:`, GitLab still uploads `DRIFT_REPORT.md` and `verdict.json` even when the job exits `1` (Failed)! |
| **6. Check Runner Availability** | Left sidebar: **Settings** $\rightarrow$ **CI/CD** $\rightarrow$ expand **Runners** | Look for a green dot next to **Instance runners** or **Group runners**. (On personal `gitlab.com` free accounts, GitLab prompts for a 1-time $1 card verification if shared runners are disabled). |

---

## 🎤 Part 1: 20-Minute Presentation Outline

| Time | Topic | Key Talking Points |
| :--- | :--- | :--- |
| **0:00 – 0:03** | **Callback to Workshop 1 (`egm-drift-report`)** | In Workshop 1, we ran `/egm:egm-drift-report` locally and promised it could run in CI/CD. Today we deliver on that promise: *what happens when someone skips local EGM checks and opens a Merge Request anyway?* |
| **0:03 – 0:07** | **Why Raw Markdown Reports & Static YAML Aren't Enough** | Generating `.gitlab-ci.yml` saves 10 minutes once, and raw `egm-drift-report` only writes Markdown text without a CI exit code. Wrapping EGM inside the **Antigravity Python SDK** turns it into an automated Merge Request blocker! |
| **0:07 – 0:13** | **Meet Antigravity Python SDK + Upstream EGM** | Introduce `google-antigravity` + `google/elephant-goldfish-model`:<br>1. **Bundled runtime wheel** (`uv add --dev google-antigravity`, zero extra CLI installs in CI).<br>2. **Defense-in-depth safety** (`CapabilitiesConfig` + `policy.deny` so CI agents are strictly read-only).<br>3. **Upstream EGM Skill + Parallel Goldfish** (`InlineSkill("egm-drift-report")` + `egm_codebase_details` + `security_auditor`).<br>4. **Typed Pydantic `response_schema`** (`GateVerdict` $\rightarrow$ writes `DRIFT_REPORT.md` + deterministic `exit 0` / `exit 1`). *(Also mention the 1-line `agy -p` headless CLI option!)* |
| **0:13 – 0:17** | **Pipeline Economics & Production Security** | **Rule #1:** Run fast deterministic checks (`pytest`) *before* AI stages so broken syntax never burns tokens.<br>**Rule #2:** Workshop uses `GEMINI_API_KEY` for speed; production uses **Vertex AI (`vertex=True`) + GitLab `id_tokens` Workload Identity Federation** (zero static keys!). |
| **0:17 – 0:20** | **Workshop Overview & Q&A** | Walk through the 4-box pipeline architecture (`Antigravity App` $\rightarrow$ `pytest` $\rightarrow$ `Antigravity SDK + EGM Gate` $\rightarrow$ `Merge / Cloud Run`) and transition to Step 1 of the Codelab. |

---

## 🛠️ Part 2: 60-Minute Hands-On Facilitator Pacing & Troubleshooting

* **0:00 – 0:07 (Step 1)**: Ensure everyone imports `retropulse-starter` into GitLab, enables **Google Antigravity SDK** in Customizations, and sees `4 passed` from `uv run pytest -v`.
  * **💼 Corporate Laptop Pre-Flight (`uv` Private Mirror Bypass)**: If presenting from a managed corporate laptop that configures a private/internal PyPI mirror in a system `uv.toml`, run this in your demo terminal *before* sharing your screen so `uv add --dev google-antigravity` locks against public PyPI (preventing `uv sync --frozen` from failing on public GitLab runners):
    ```zsh
    export UV_NO_CONFIG=1
    export UV_INDEX_URL="https://pypi.org/simple"
    ```
    *(If `uv.lock` was already generated against a private mirror, reset it with `rm uv.lock && uv lock --no-config --index-url https://pypi.org/simple`.)*
* **0:07 – 0:25 (Step 2)**: Building `ci/ai_gate.py`. Point attendees to the collapsible **Checkpoint** in Step 2 if anyone's generated code misses an import, `policy.allow("*")` alongside `policy.deny(...)`, or `BuiltinTools.FINISH`. Make sure everyone sees `# Antigravity + EGM CI Gate: PASSED` locally (~1–2 min) before touching GitLab YAML!
  * **🔒 Screen-Share Tip (macOS `pbpaste`)**: To set `GEMINI_API_KEY` live on stage without showing it on screen or in `~/.zsh_history`, copy the key on your second monitor first, then **type manually** in iTerm2:
    ```zsh
    export GEMINI_API_KEY="$(pbpaste)"
    ```
    *(Type it by hand—do not copy-paste the command itself, or it will overwrite the API key in your clipboard!)*
* **0:25 – 0:35 (Step 3)**: Emphasize **unchecking "Protect variable"** when adding `GEMINI_API_KEY` in GitLab! Celebrate when attendees see their first green 2-stage pipeline under **Build > Pipelines**.
* **0:35 – 0:47 (Step 4 — The "Aha!" Moment)**: Highlight that `uv run pytest -v` passes 4/4 locally *even with* the secret-leaking `/api/debug/config` route and `USER root` in `Dockerfile`—then show `unit-tests` green ✅ + `antigravity-ai-gate` red ❌ (`DRIFT_REPORT.md`) on the GitLab Merge Request!
* **0:47 – 0:57 (Step 5)**: Guide attendees to update `docs/designs/retropulse.md` *first* when adding `/healthz`, watching the Merge Request automatically re-run and turn green ✅.
* **0:57 – 1:00 (Step 6 — Bonus)**: Walk through the keyless Workload Identity Federation `id_tokens` pattern for Cloud Run.
