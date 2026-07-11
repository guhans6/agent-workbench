#!/usr/bin/env python3
"""Validate a proposed, not-yet-installed global Codex routing migration."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import tomllib


DISPOSITIONS = {"retain", "modify", "merge", "replace", "remove"}
REQUIRED_PROJECTION = (
    "General routing first.",
    "Select the best-value profile by expected quality, cost, latency, access, and coordination overhead.",
    "Explicit user instructions override routing.",
    "Every assignment is exact; an unavailable model stops routing instead of falling back.",
    "The orchestrator owns classification and workers do not self-promote.",
    "A concrete Luna failure escalates once to Terra.",
    "Terra escalates to Sol only for conflicting evidence, architectural ambiguity, repeated failure, or elevated risk.",
    "At most one Sol/high subagent runs automatically per user task.",
    "Matt workflow routing.",
    "Use `grill-with-docs` for an idea needing clarification and `wayfinder` when a huge effort's route remains unclear.",
    "Apple exceptions second.",
)


@dataclass(frozen=True, order=True)
class Finding:
    severity: str
    code: str
    subject: str

    def render(self) -> str:
        return f"{self.severity} {self.code} {self.subject}"


def read_toml(path: Path, findings: list[Finding], subject: str) -> dict[str, object] | None:
    try:
        return tomllib.loads(path.read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        findings.append(Finding("FAIL", "malformed-toml", subject))
        return None


def assignment_matches(profile: dict[str, object], metadata: dict[str, object]) -> bool:
    return (
        profile.get("model") == metadata.get("model")
        and profile.get("model_reasoning_effort") == metadata.get("reasoning")
        and profile.get("sandbox_mode") == metadata.get("access")
    )


def managed_block(text: str) -> str | None:
    start = "<!-- routing:start -->"
    end = "<!-- routing:end -->"
    if text.count(start) != 1 or text.count(end) != 1:
        return None
    before, remainder = text.split(start)
    block, after = remainder.split(end)
    # Routing policy belongs only in the managed span; a title and whitespace may surround it.
    if any(item in before or item in after for item in REQUIRED_PROJECTION):
        return None
    return block


def validate(source: Path, observed: Path, shared_policy_path: Path, live_agents: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    policy = read_toml(shared_policy_path, findings, shared_policy_path.name)
    migration = read_toml(source / "migration.toml", findings, "migration.toml")
    observations = read_toml(observed, findings, observed.name)
    agents_text = (source / "AGENTS.md").read_text(errors="replace") if (source / "AGENTS.md").is_file() else ""
    has_markers = "<!-- routing:start -->" in agents_text or "<!-- routing:end -->" in agents_text
    block = managed_block(agents_text)
    if not has_markers:
        findings.append(Finding("FAIL", "missing-managed-routing-block", "AGENTS.md"))
    elif block is None:
        findings.append(Finding("FAIL", "invalid-managed-routing-block", "AGENTS.md"))
    else:
        positions = [block.find(item) for item in REQUIRED_PROJECTION]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            findings.append(Finding("FAIL", "invalid-routing-projection-order", "AGENTS.md"))
    if policy is not None:
        selection = policy.get("selection")
        escalation = policy.get("escalation")
        if not isinstance(selection, dict) or selection.get("silent_model_fallback") is not False:
            findings.append(Finding("FAIL", "silent-model-fallback-enabled", shared_policy_path.name))
        if (
            not isinstance(selection, dict)
            or selection.get("objective") != "best-value"
            or selection.get("user_override") is not True
            or selection.get("factors") != ["expected-quality", "cost", "latency", "access", "coordination-overhead"]
            or selection.get("exact_model_assignment") is not True
            or not isinstance(escalation, dict)
            or escalation.get("owner") != "orchestrator"
            or escalation.get("workers_may_self_promote") is not False
            or escalation.get("automatic_sol_high_budget") != 1
            or escalation.get("luna_to_terra_trigger") != "concrete-failure"
            or escalation.get("terra_to_sol_triggers")
            != ["conflicting-evidence", "architectural-ambiguity", "repeated-failure", "elevated-risk"]
        ):
            findings.append(Finding("FAIL", "invalid-shared-policy", shared_policy_path.name))
    if migration is None:
        return sorted(set(findings))

    available_models = set(observations.get("models", [])) if observations else set()
    available_skills = set(observations.get("skills", [])) if observations else set()
    proposed: dict[str, dict[str, object]] = {}
    for item in migration.get("proposed_profiles", []):
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            name = item["name"]
            if name in proposed:
                findings.append(Finding("FAIL", "duplicate-manifest-profile", name))
            else:
                proposed[name] = item
    profiles: dict[str, dict[str, object]] = {}
    for path in sorted((source / "agents").glob("*.toml")):
        profile = read_toml(path, findings, f"agents/{path.name}")
        if profile is not None and isinstance(profile.get("name"), str):
            if profile["name"] in profiles:
                findings.append(Finding("FAIL", "duplicate-proposed-profile", profile["name"]))
            else:
                profiles[profile["name"]] = profile

    for name in profiles:
        if name not in proposed:
            findings.append(Finding("FAIL", "unmanifested-profile-artifact", name))
    for name in proposed:
        if name not in profiles:
            findings.append(Finding("FAIL", "missing-profile-artifact", name))

    for name, metadata in proposed.items():
        profile = profiles.get(name)
        if profile is None or not assignment_matches(profile, metadata):
            findings.append(Finding("FAIL", "profile-assignment-mismatch", name))
        model = metadata.get("model")
        if isinstance(model, str) and model not in available_models:
            findings.append(Finding("FAIL", "unavailable-model", model))
        for skill in metadata.get("skills", []):
            if isinstance(skill, str) and skill not in available_skills:
                findings.append(Finding("FAIL", "missing-skill", skill))

    existing = migration.get("existing_agents", [])
    names = [item.get("name") for item in existing if isinstance(item, dict)]
    if len(names) != len(set(names)):
        findings.append(Finding("FAIL", "duplicate-existing-agent", "migration.toml"))
    for item in existing:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            findings.append(Finding("FAIL", "missing-existing-agent", "migration.toml"))
            continue
        name = item["name"]
        if live_agents is not None:
            live = read_toml(live_agents / f"{name}.toml", findings, f"live-agents/{name}.toml")
            if live is None:
                findings.append(Finding("FAIL", "missing-live-agent", name))
            elif (
                item.get("current_model") != live.get("model")
                or item.get("current_reasoning") != live.get("model_reasoning_effort")
                or item.get("current_access") != live.get("sandbox_mode")
            ):
                findings.append(Finding("FAIL", "live-inventory-mismatch", name))
        if item.get("disposition") not in DISPOSITIONS:
            findings.append(Finding("FAIL", "invalid-disposition", name))
        replacement = item.get("replacement")
        if item.get("disposition") in {"merge", "replace", "remove"}:
            if not isinstance(replacement, str) or replacement not in proposed or item.get("install_before_remove") is not True:
                findings.append(Finding("FAIL", "replacement-not-installable", name))
        if item.get("disposition") == "modify":
            if replacement != name or item.get("patch_fields") != ["model", "model_reasoning_effort", "sandbox_mode"]:
                findings.append(Finding("FAIL", "non-patch-same-name-update", name))
            if item.get("install_before_remove") is not False:
                findings.append(Finding("FAIL", "misleading-install-before-remove", name))
        if isinstance(replacement, str) and replacement in proposed:
            profile = proposed[replacement]
            if item.get("proposed_model") != profile.get("model") or item.get("proposed_reasoning") != profile.get("reasoning"):
                findings.append(Finding("FAIL", "migration-assignment-mismatch", name))
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--observed", required=True, type=Path)
    parser.add_argument("--shared-policy", required=True, type=Path)
    parser.add_argument("--live-agents", type=Path, help="Read-only current global agents directory to verify the manifest inventory.")
    arguments = parser.parse_args()
    findings = validate(arguments.source, arguments.observed, arguments.shared_policy, arguments.live_agents)
    for finding in findings:
        print(finding.render())
    if findings:
        print("FAIL global routing migration has errors")
        return 1
    print("PASS global routing migration is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
