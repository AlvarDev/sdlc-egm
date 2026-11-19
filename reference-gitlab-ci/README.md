# RetroPulse — Reference Pipeline Solution (GitLab CI/CD + Antigravity SDK)

Golden reference checkpoint for **Workshop 2: Deploying CI/CD Pipelines with Google Antigravity & the Antigravity SDK**.

## Included Pipeline Components

* [`.gitlab-ci.yml`](./.gitlab-ci.yml) — 2-stage GitLab CI/CD pipeline (`unit-tests` -> `antigravity-ai-gate`) pulling [`google/elephant-goldfish-model`](https://github.com/google/elephant-goldfish-model), caching `uv` dependencies, and publishing `DRIFT_REPORT.md` + `verdict.json` artifacts.
* [`ci/ai_gate.py`](./ci/ai_gate.py) — Autonomous, read-only Antigravity Python SDK Elephant coordinator loading the upstream `egm-drift-report` skill and spawning two parallel Goldfish (`egm_codebase_details` and `security_auditor`) to return a Pydantic `GateVerdict`.

## Run Locally

```bash
export GEMINI_API_KEY="your-api-key"
uv sync
uv run pytest
uv run python ci/ai_gate.py
```
