"""Autonomous CI/CD Quality & Security Gate powered by Antigravity SDK + EGM."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Literal

from google.antigravity import Agent, BuiltinTools, CapabilitiesConfig, LocalAgentConfig, types
from google.antigravity.hooks import policy
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parent.parent
EGM_GIT_URL = "https://github.com/google/elephant-goldfish-model.git"
_FRONTMATTER_RE = re.compile(
    r"\A---\s*\r?\n(?:.*?\r?\n)?---\s*(?:\r?\n|$)",
    re.DOTALL,
)
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


class Finding(BaseModel):
    category: Literal["SPEC_DRIFT", "SECURITY"]
    severity: Literal["HIGH", "MEDIUM", "LOW"]
    file: str = Field(description="Relative file path where the issue was found")
    description: str = Field(description="What violates the spec or security policy")
    remediation: str = Field(description="Concrete fix required to pass the gate")


class GateVerdict(BaseModel):
    approved: bool = Field(
        description="True ONLY when zero HIGH/MEDIUM spec-drift or security findings exist"
    )
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    summary: str
    findings: list[Finding] = Field(default_factory=list)


def _strip_frontmatter(markdown_text: str) -> str:
    """Strips optional YAML frontmatter from an EGM skill or Goldfish file."""
    return _FRONTMATTER_RE.sub("", markdown_text, count=1).lstrip("\r\n")


def ensure_egm_repo() -> Path:
    """Locates or shallow-clones google/elephant-goldfish-model for CI/local runs."""
    env_path = os.environ.get("EGM_REPO_PATH", "").strip()
    if env_path:
        egm_dir = Path(env_path).expanduser().resolve()
        if (egm_dir / "skills" / "egm-drift-report" / "SKILL.md").exists():
            return egm_dir

    cache_dir = Path(tempfile.gettempdir()) / "elephant-goldfish-model"
    if not (cache_dir / "skills" / "egm-drift-report" / "SKILL.md").exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet", EGM_GIT_URL, str(cache_dir)],
            check=True,
        )
    return cache_dir


def get_git_diff() -> str:
    """Returns the git diff for the current Merge Request or working tree."""
    base_sha = os.environ.get("CI_MERGE_REQUEST_DIFF_BASE_SHA", "").strip()
    target_branch = os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", "").strip()

    candidates: list[list[str]] = []
    if base_sha:
        candidates.append(["git", "diff", f"{base_sha}...HEAD"])
    if target_branch:
        candidates.append(["git", "diff", f"origin/{target_branch}...HEAD"])
        candidates.append(["git", "diff", f"{target_branch}...HEAD"])
    candidates.append(["git", "diff", "HEAD"])

    for cmd in candidates:
        res = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout[:12000]

    return "No git diff detected; audit the full repository baseline."


READ_ONLY_SUBAGENT_TOOLS = [
    BuiltinTools.VIEW_FILE,
    BuiltinTools.LIST_DIR,
    BuiltinTools.SEARCH_DIR,
    BuiltinTools.FIND_FILE,
]


def build_config() -> LocalAgentConfig:
    egm_root = ensure_egm_repo()
    drift_skill_body = _strip_frontmatter(
        (egm_root / "skills" / "egm-drift-report" / "SKILL.md").read_text(encoding="utf-8")
    )
    goldfish_body = _strip_frontmatter(
        (egm_root / "agents" / "codebase_details.md").read_text(encoding="utf-8")
    )

    egm_drift_skill = types.InlineSkill(
        name="egm-drift-report",
        description=(
            "Official EGM drift detection workflow comparing design specs in "
            "docs/designs/ against the live codebase."
        ),
        content=drift_skill_body,
    )

    egm_codebase_details = types.SubagentConfig(
        name="egm_codebase_details",
        description=(
            "Official EGM Codebase Details Goldfish auditing docs/designs/retropulse.md "
            "against main.py and static/index.html."
        ),
        system_instructions=(
            f"{goldfish_body}\n\n"
            "CI Execution Context: Run in `Mode: REVIEW` against `docs/designs/retropulse.md`, "
            "`main.py`, `static/index.html`, and call `get_git_diff`. Flag any undocumented "
            "API endpoints, altered Pydantic validation constraints, or violations of Non-Goals."
        ),
        capabilities=types.SubagentCapabilities(enabled_tools=READ_ONLY_SUBAGENT_TOOLS),
        skills_config=types.SubagentNoneSkillsConfig(),
        tools=[get_git_diff],
    )

    security_auditor = types.SubagentConfig(
        name="security_auditor",
        description="Stateless Security Goldfish auditing Dockerfile and Python code.",
        system_instructions=(
            "You are a stateless Cloud Security Goldfish running in CI. "
            "Read Dockerfile, main.py, and call get_git_diff. Flag HIGH severity "
            "issues if the runtime container runs as root instead of nonroot, skips "
            "multi-stage isolation, hardcodes secrets/tokens/keys, or exposes "
            "environment variables."
        ),
        capabilities=types.SubagentCapabilities(enabled_tools=READ_ONLY_SUBAGENT_TOOLS),
        skills_config=types.SubagentNoneSkillsConfig(),
        tools=[get_git_diff],
    )

    return LocalAgentConfig(
        model=os.environ.get("ANTIGRAVITY_MODEL") or None,
        workspaces=[str(REPO_ROOT)],
        inline_skills=[egm_drift_skill],
        system_instructions=(
            "You are the Elephant CI/CD Release Gate Coordinator. "
            "Use the analysis steps from the `egm-drift-report` skill on `docs/designs/` "
            "(do NOT attempt to call file-writing tools—CI enforces read-only policies "
            "and Python writes `DRIFT_REPORT.md` from your structured output). "
            "Invoke BOTH `egm_codebase_details` and `security_auditor` Goldfish in parallel, "
            "synthesize their findings without invention, and set approved=False if ANY "
            "HIGH or MEDIUM finding exists. IMPORTANT: Override Step 4 of `egm-drift-report`—"
            "do NOT end with plain Markdown text; you MUST invoke the `finish` tool to submit "
            "the final `GateVerdict` structured payload."
        ),
        capabilities=CapabilitiesConfig(
            enable_subagents=True,
            enabled_tools=[
                BuiltinTools.VIEW_FILE,
                BuiltinTools.LIST_DIR,
                BuiltinTools.SEARCH_DIR,
                BuiltinTools.FIND_FILE,
                BuiltinTools.INVOKE_SUBAGENT,
                BuiltinTools.FINISH,
            ],
            allowed_subagents=["egm_codebase_details", "security_auditor"],
        ),
        policies=[
            policy.deny("create_file"),
            policy.deny("edit_file"),
            policy.deny("run_command"),
            policy.allow("*"),
        ],
        subagents=[egm_codebase_details, security_auditor],
        response_schema=GateVerdict,
    )


def _extract_verdict_payload(agent: Agent, text_fallback: str) -> Any | None:
    for step in reversed(agent.conversation.history):
        if (
            step.depth == 0
            and step.type == types.StepType.FINISH
            and step.structured_output is not None
        ):
            return step.structured_output

    cleaned = text_fallback.strip()
    if not cleaned:
        return None
    if match := _JSON_FENCE_RE.search(cleaned):
        cleaned = match.group(1)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def write_reports(verdict: GateVerdict) -> None:
    status_badge = "PASSED" if verdict.approved else "BLOCKED"
    drift_findings = [f for f in verdict.findings if f.category == "SPEC_DRIFT"]
    sec_findings = [f for f in verdict.findings if f.category == "SECURITY"]

    lines = [
        f"# Antigravity + EGM CI Gate: {status_badge}",
        "",
        f"- **Approved**: `{verdict.approved}`",
        f"- **Risk Level**: `{verdict.risk_level}`",
        f"- **Summary**: {verdict.summary}",
        "",
        "## docs/designs/retropulse.md (EGM Drift Report)",
        "",
    ]
    if not drift_findings:
        lines.append("No drift detected")
    else:
        for f in drift_findings:
            lines.append(
                f"- **[{f.severity}] `{f.file}`**: {f.description} *(Fix: {f.remediation})*"
            )

    lines.extend(["", "## Security Audit", ""])
    if not sec_findings:
        lines.append("No security violations detected")
    else:
        for f in sec_findings:
            lines.append(
                f"- **[{f.severity}] `{f.file}`**: {f.description} *(Fix: {f.remediation})*"
            )

    report_md = "\n".join(lines) + "\n"
    (REPO_ROOT / "DRIFT_REPORT.md").write_text(report_md, encoding="utf-8")
    (REPO_ROOT / "verdict.json").write_text(
        verdict.model_dump_json(indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n{report_md}")


async def run_gate() -> int:
    has_api_key = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    has_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in ("true", "1")
    if not has_api_key and not has_vertex:
        print(
            "ERROR: Set GEMINI_API_KEY (workshop) or GOOGLE_GENAI_USE_VERTEXAI=true "
            "(Vertex AI / Gemini Enterprise) before running ci/ai_gate.py.",
            file=sys.stderr,
        )
        return 2

    t0 = time.monotonic()
    config = build_config()
    print(f"[{time.monotonic() - t0:5.1f}s] Starting Antigravity + EGM CI Gate...", flush=True)

    async with Agent(config) as agent:
        response = await agent.chat(
            "Run the EGM drift & security release audit on `docs/designs/` now. "
            "Delegate in parallel to `egm_codebase_details` and `security_auditor`, "
            "synthesize their findings, and invoke the `finish` tool with GateVerdict."
        )
        async for tc in response.tool_calls:
            print(f"[{time.monotonic() - t0:5.1f}s] Tool call -> {tc.name}", flush=True)

        raw = await response.structured_output()
        last_text = ""
        if raw is None:
            last_text = await response.text()
            raw = _extract_verdict_payload(agent, last_text)

        if raw is None:
            followup = await agent.chat(
                "Do not output Markdown prose. Invoke the `finish` tool now to submit "
                "the final GateVerdict structured payload."
            )
            raw = await followup.structured_output()
            if raw is None:
                last_text = await followup.text()
                raw = _extract_verdict_payload(agent, last_text)

        if raw is None:
            raise RuntimeError(
                f"Agent failed to produce GateVerdict.\nLast response text:\n{last_text}"
            )
        verdict = GateVerdict.model_validate(raw)

    write_reports(verdict)
    return 0 if verdict.approved else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_gate()))
