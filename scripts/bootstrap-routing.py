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
            files = sorted(path for path in root.rglob("*") if path.is_file())
            if files:
                evidence.append(files[0].relative_to(repository).as_posix())
    return sorted(evidence)


def render(repository: Path) -> tuple[int, str]:
    evidence = observed_evidence(repository)
    if not evidence:
        lines = (
            "STATUS: FAIL",
            "PRECHECK: FAIL insufficient-repository-evidence",
            "EVIDENCE: none",
            "ROUTING: blocked",
            "ATTENTION: provide repository instructions, plans, manifests, scripts, tests, or confirmed decisions",
            "FILES: none",
            "CHECKLIST: resolve evidence gap before proposing a write-capable route",
        )
        return 1, "\n".join(lines) + "\n"

    agents_path = repository / "AGENTS.md"
    if agents_path.is_file() and "<!-- routing:start -->" in agents_path.read_text(errors="replace"):
        lines = (
            "STATUS: FAIL",
            "PRECHECK: FAIL existing-routing-contract",
            f"EVIDENCE: {', '.join(evidence)}",
            "ROUTING: blocked; use refresh-project-agent-routing explicitly",
            "ATTENTION: bootstrap never infers refresh mode",
            "FILES: none",
            "CHECKLIST: invoke the refresh skill and preserve the existing managed block",
        )
        return 1, "\n".join(lines) + "\n"

    if agents_path.is_file():
        status = "PASS"
        precheck = "PRECHECK: PASS repository-context-ready"
        attention = "ATTENTION: inspect existing repository context before any minimal managed-block patch"
    else:
        status = "WARN"
        precheck = "PRECHECK: WARN missing-repository-context AGENTS.md"
        attention = "ATTENTION: add a concise managed routing/context block to AGENTS.md"

    lines = (
        f"STATUS: {status}",
        precheck,
        f"EVIDENCE: {', '.join(evidence)}",
        "ROUTING: global execution profiles first; no local profiles proposed",
        attention,
        "FILES: AGENTS.md",
        "CHECKLIST: review context pointer; approve minimal managed block; validate before write",
    )
    return 0, "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    arguments = parser.parse_args()
    code, output = render(arguments.repository)
    print(output, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
