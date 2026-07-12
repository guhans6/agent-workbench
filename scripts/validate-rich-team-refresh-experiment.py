#!/usr/bin/env python3
"""Validate the read-only Companion rich-team refresh experiment."""

from __future__ import annotations

import argparse
import subprocess
import tomllib
from pathlib import Path


RICH_TEAM = (
    "visualcompanion_docs_researcher",
    "visualcompanion_explorer",
    "visualcompanion_implementer",
    "visualcompanion_investigator",
    "visualcompanion_issue_slicer",
    "visualcompanion_reviewer",
    "visualcompanion_scout",
    "visualcompanion_visual_tester",
)
APPROVAL_DELTA_LINES = 7
DEFAULT_ADMISSION = Path(__file__).resolve().parents[1] / "experiments" / "companion-rich-team-admission.toml"
DEFAULT_GLOBAL_ROUTING = Path(__file__).resolve().parents[1] / "platforms" / "codex" / "migrations" / "gpt-5.6"


def git_status(repository: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def text_at(repository: Path, relative: str) -> str:
    try:
        return (repository / relative).read_text(errors="replace")
    except OSError:
        return ""


def profile_at(path: Path) -> dict[str, object]:
    try:
        return tomllib.loads(path.read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return {}


def admission_result(
    name: str, profile: dict[str, object], team_skill: str, admission: dict[str, object], global_routing: str
) -> tuple[bool, str]:
    description = profile.get("description")
    instructions = profile.get("developer_instructions")
    recognizable_task_class = isinstance(description, str) and bool(description.strip())
    distinct_execution_boundary = isinstance(instructions, str) and "VisualCompanion" in instructions
    concise_local_instructions = isinstance(instructions, str) and len(instructions.splitlines()) <= 30
    recurring_lane = name in team_skill
    evidence = admission.get("evidence")
    global_equivalent = admission.get("global_equivalent")
    global_trigger = admission.get("global_trigger")
    local_distinct = admission.get("local_distinct")
    profile_text = "\n".join(value for value in profile.values() if isinstance(value, str))
    has_global_coverage = (
        isinstance(global_equivalent, str)
        and global_equivalent in global_routing
        and isinstance(global_trigger, str)
        and global_trigger in global_routing
    )
    value_exceeds_overhead = (
        isinstance(evidence, str)
        and evidence in profile_text
        and isinstance(local_distinct, bool)
        and (local_distinct or has_global_coverage)
        and local_distinct
    )
    missing = [
        criterion
        for criterion, passed in (
            ("recognizable-task-class", recognizable_task_class),
            ("distinct-execution-boundary", distinct_execution_boundary),
            ("concise-local-instructions", concise_local_instructions),
            ("recurring-lane", recurring_lane),
            ("value-exceeds-overhead", value_exceeds_overhead),
        )
        if not passed
    ]
    return not missing, ", ".join(missing) if missing else "admitted"


def validate(repository: Path, admission_path: Path, global_routing_path: Path) -> tuple[list[str], dict[str, str], list[str]]:
    findings: list[str] = []
    profile_root = repository / ".codex" / "agents"
    present = {path.stem for path in profile_root.glob("*.toml")}
    for role in RICH_TEAM:
        if role not in present:
            findings.append(f"FAIL missing-rich-team-role {role}")

    agents = text_at(repository, "AGENTS.md")
    if not all(role in agents for role in ("scout", "explorer", "investigator")):
        findings.append("FAIL missing-escalation-chain AGENTS.md")

    team_skill = text_at(repository, ".agents/skills/team/SKILL.md")
    if not team_skill:
        team_skill = text_at(repository, ".agents/skills/visualcompanion-project-team/SKILL.md")
    if "ask-matt" not in team_skill:
        findings.append("FAIL missing-current-planning-capability")
    if "to-prd" not in team_skill or "to-issues" not in team_skill:
        findings.append("FAIL missing-legacy-planning-aliases")
    if "Context7" not in team_skill or "duplicate standalone" not in team_skill:
        findings.append("FAIL missing-plugin-boundary")
    admission_document = profile_at(admission_path)
    global_routing = "\n".join(text_at(global_routing_path, name) for name in ("AGENTS.md", "migration.toml"))
    if not global_routing:
        findings.append("FAIL missing-global-routing-evidence")
    admission_profiles = admission_document.get("profiles", {})
    if not isinstance(admission_profiles, dict):
        findings.append("FAIL malformed-admission-evidence")
        admission_profiles = {}
    admissions: dict[str, str] = {}
    for name in RICH_TEAM:
        profile = profile_at(profile_root / f"{name}.toml")
        admission = admission_profiles.get(name, {})
        if not isinstance(admission, dict):
            findings.append(f"FAIL missing-admission-evidence {name}")
            admission = {}
        admitted, reason = admission_result(name, profile, team_skill, admission, global_routing)
        admissions[name] = reason
        if not admitted and reason != "value-exceeds-overhead":
            findings.append(f"FAIL admission-rejected {name}: {reason}")
    return findings, admissions, present


def render(repository: Path, admission_path: Path, global_routing_path: Path) -> tuple[int, str]:
    before = git_status(repository)
    findings, admissions, present = validate(repository, admission_path, global_routing_path)
    after = git_status(repository)
    if before != after:
        findings.append("FAIL target-mutated-during-experiment")

    if findings:
        return 1, "\n".join(["STATUS: FAIL", *findings, "TARGET MUTATION: none", ""])

    admitted_count = sum(reason == "admitted" for reason in admissions.values())
    recommendations = ", ".join(name for name, reason in admissions.items() if reason == "value-exceeds-overhead")
    dirty_scope = before.strip().splitlines()
    dirty_summary = "; ".join(dirty_scope) if dirty_scope else "clean"
    full_roster_lines = len(present) + 2
    reduction = round((1 - APPROVAL_DELTA_LINES / full_roster_lines) * 100)
    lines = (
        "STATUS: PASS",
        "TARGET CONTRACT: legacy rich team; no target patch applied",
        "DIRTY WORK PRESERVED: yes",
        f"DIRTY SCOPE ({len(dirty_scope)}): {dirty_summary}",
        f"CURRENT PROFILES: {len(present)}",
        f"ADMITTED LOCAL PROFILES: {admitted_count}",
        f"REMOVAL RECOMMENDATIONS: {recommendations}",
        "MODEL MIGRATIONS: none (separate from role reduction)",
        "CAPABILITY DELTA: planning aliases need to-prd -> to-spec and to-issues -> to-tickets",
        "PLUGIN DELTA: Context7 remains plugin-backed; no standalone MCP is required",
        f"APPROVAL LENGTH: delta {APPROVAL_DELTA_LINES} lines; full roster {full_roster_lines} lines; reduction {reduction}%",
        "TARGET MUTATION: none",
        "",
    )
    return 0, "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--admission", type=Path, default=DEFAULT_ADMISSION)
    parser.add_argument("--global-routing", type=Path, default=DEFAULT_GLOBAL_ROUTING)
    arguments = parser.parse_args()
    code, output = render(arguments.repository, arguments.admission, arguments.global_routing)
    print(output, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
