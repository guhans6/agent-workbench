#!/usr/bin/env python3
"""Render a concise, evidence-backed first-time routing-bootstrap approval surface."""

from __future__ import annotations

import argparse
from pathlib import Path


EVIDENCE_FILES = (
    "AGENTS.md",
    "CONTEXT.md",
    "README.md",
    "README",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Package.swift",
)


def observed_evidence(repository: Path) -> list[str]:
    evidence = [name for name in EVIDENCE_FILES if (repository / name).is_file()]
    for directory in ("docs", "scripts", "tests", "test"):
        root = repository / directory
        if root.is_dir():
            files = sorted(
                path
                for path in root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
            )
            if files:
                evidence.append(files[0].relative_to(repository).as_posix())
    return sorted(evidence)


def approval_surface(
    status: str, precheck: str, evidence: list[str], routing: str, attention: str, files: str, checklist: str
) -> str:
    return "\n".join(
        (
            f"STATUS: {status}",
            precheck,
            f"EVIDENCE: {', '.join(evidence) if evidence else 'none'}",
            routing,
            attention,
            f"FILES: {files}",
            checklist,
        )
    ) + "\n"


def parse_global_profiles(values: list[str]) -> list[tuple[str, str, str, str, str]]:
    profiles: list[tuple[str, str, str, str, str]] = []
    for value in values:
        fields = tuple(part.strip() for part in value.split("|"))
        if len(fields) != 5 or not all(fields):
            raise ValueError("global profiles must use name|trigger|model|reasoning|access")
        profiles.append(fields)
    return profiles


def has_routing_contract(repository: Path, agents_path: Path) -> bool:
    return (
        (agents_path.is_file() and "<!-- routing:start -->" in agents_path.read_text(errors="replace"))
        or (repository / "routing.toml").is_file()
        or any((repository / ".codex" / "agents").glob("*.toml"))
    )


def render(repository: Path, global_profiles: list[tuple[str, str, str, str, str]]) -> tuple[int, str]:
    evidence = observed_evidence(repository)
    if not evidence:
        return 1, approval_surface(
            "FAIL",
            "PRECHECK: FAIL insufficient-repository-evidence",
            evidence,
            "ROUTING: blocked",
            "ATTENTION: provide repository instructions, plans, manifests, scripts, tests, or confirmed decisions",
            "none",
            "CHECKLIST: resolve evidence gap before proposing a write-capable route",
        )

    agents_path = repository / "AGENTS.md"
    if has_routing_contract(repository, agents_path):
        return 1, approval_surface(
            "FAIL",
            "PRECHECK: FAIL existing-routing-contract",
            evidence,
            "ROUTING: blocked; use a dedicated refresh workflow explicitly",
            "ATTENTION: bootstrap never infers refresh mode",
            "none",
            "CHECKLIST: invoke the refresh workflow and preserve the existing Managed Routing Block",
        )

    context_path = repository / "CONTEXT.md"
    if agents_path.is_file() and agents_path.read_text(errors="replace").strip() and context_path.is_file() and context_path.read_text(errors="replace").strip():
        status = "PASS"
        precheck = "PRECHECK: PASS repository-context-observed"
        attention = "ATTENTION: inspect observed repository context before any minimal Managed Routing Block patch"
    elif agents_path.is_file() and agents_path.read_text(errors="replace").strip():
        status = "WARN"
        precheck = "PRECHECK: WARN missing-repository-context CONTEXT.md"
        attention = "ATTENTION: add or confirm the repository context pointer before proposing a Managed Routing Block"
    else:
        status = "WARN"
        precheck = "PRECHECK: WARN missing-repository-context AGENTS.md"
        attention = "ATTENTION: add a concise Managed Routing Block to AGENTS.md"

    if global_profiles:
        routing = "ROUTING: " + "; ".join(" | ".join(profile) for profile in global_profiles)
        routing += "; no Repository-Specific Profiles proposed"
    else:
        status = "WARN"
        routing = "ROUTING: unavailable global profile inventory; no Repository-Specific Profiles proposed"
        attention = "ATTENTION: inspect global profiles before approval; " + attention.removeprefix("ATTENTION: ")
    return 0, approval_surface(
        status,
        precheck,
        evidence,
        routing,
        attention,
        "AGENTS.md",
        "CHECKLIST: review context pointer; review global profile assignments; approve minimal Managed Routing Block; validate before write",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--global-profile", action="append", default=[], metavar="NAME|TRIGGER|MODEL|REASONING|ACCESS")
    arguments = parser.parse_args()
    try:
        global_profiles = parse_global_profiles(arguments.global_profile)
    except ValueError as error:
        parser.error(str(error))
    code, output = render(arguments.repository, global_profiles)
    print(output, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
