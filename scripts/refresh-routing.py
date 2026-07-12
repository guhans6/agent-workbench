#!/usr/bin/env python3
"""Render a delta-only routing-refresh approval surface without modifying a repository."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path


CONTROL_FILES = {"routing.toml"}
CAPABILITY_RENAMES = (("to-prd", "to-spec"), ("to-issues", "to-tickets"))
MANAGED_START = "<!-- routing:start -->"
MANAGED_END = "<!-- routing:end -->"


def files_in(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def managed_files(repository: Path) -> list[Path]:
    paths = [repository / "routing.toml", repository / "AGENTS.md"]
    paths.extend((repository / ".codex" / "agents").glob("*.toml"))
    paths.extend((repository / "skills").glob("*/SKILL.md"))
    return [path for path in paths if path.is_file()]


def profile_assignment(path: Path) -> tuple[str | None, str | None]:
    try:
        document = tomllib.loads(path.read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return None, None
    return document.get("model"), document.get("model_reasoning_effort")


def is_managed_path(relative: str) -> bool:
    return relative in {"routing.toml", "AGENTS.md"} or (
        relative.startswith(".codex/agents/") and relative.endswith(".toml") and relative.count("/") == 2
    )


def managed_block(text: str) -> tuple[str, str, str] | None:
    if text.count(MANAGED_START) != 1 or text.count(MANAGED_END) != 1:
        return None
    before, remainder = text.split(MANAGED_START)
    block, after = remainder.split(MANAGED_END)
    return before, block, after


def routing_rows(repository: Path, candidate: Path, changed: list[str]) -> list[str]:
    if not any(path == "routing.toml" or path.startswith(".codex/agents/") for path in changed):
        return []
    current_path = repository / "routing.toml"
    proposed_path = candidate / "routing.toml"
    try:
        current = tomllib.loads(current_path.read_text())
        proposed = tomllib.loads((proposed_path if proposed_path.is_file() else current_path).read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return []
    previous_routes = {(route.get("trigger"), route.get("profile")) for route in current.get("routes", []) if isinstance(route, dict)}
    profile_metadata = {
        profile.get("name"): profile for profile in proposed.get("profiles", []) if isinstance(profile, dict) and isinstance(profile.get("name"), str)
    }
    changed_profiles = {Path(path).stem for path in changed if path.startswith(".codex/agents/")}
    rows: list[str] = []
    for route in proposed.get("routes", []):
        if not isinstance(route, dict):
            continue
        trigger, profile_name = route.get("trigger"), route.get("profile")
        if not isinstance(trigger, str) or not isinstance(profile_name, str):
            continue
        if (trigger, profile_name) in previous_routes and profile_name not in changed_profiles:
            continue
        profile_path = candidate / ".codex" / "agents" / f"{profile_name}.toml"
        if not profile_path.is_file():
            profile_path = repository / ".codex" / "agents" / f"{profile_name}.toml"
        model, reasoning = profile_assignment(profile_path)
        metadata = profile_metadata.get(profile_name, {})
        access = metadata.get("access_requirement", "none")
        skills = metadata.get("skills", [])
        skill_list = ", ".join(skills) if isinstance(skills, list) and all(isinstance(skill, str) for skill in skills) else "none"
        rows.append(f"{profile_name} | {trigger} | {model or 'none'} | {reasoning or 'none'} | {access} | {skill_list}")
    return rows


def validate(repository: Path, candidate: Path) -> tuple[bool, list[str]]:
    with tempfile.TemporaryDirectory() as temporary_directory:
        materialized = Path(temporary_directory) / "routing"
        for source in managed_files(repository):
            copy_file(source, materialized / source.relative_to(repository))
        for source in files_in(candidate):
            copy_file(source, materialized / source.relative_to(candidate))
        command = [
            "python3",
            str(Path(__file__).with_name("validate-routing.py")),
            "--repository",
            str(repository),
            "--routing",
            str(materialized),
        ]
        for source in files_in(materialized):
            relative = source.relative_to(materialized).as_posix()
            if relative not in CONTROL_FILES:
                command.extend(("--approved-file", relative))
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    findings = [line for line in result.stdout.splitlines() if line.startswith(("FAIL ", "WARN "))]
    return result.returncode == 0 and not any(line.startswith("FAIL ") for line in findings), findings


def render(repository: Path, candidate: Path, approved_files: set[str]) -> tuple[int, str]:
    agents = repository / "AGENTS.md"
    if not agents.is_file() or MANAGED_START not in agents.read_text(errors="replace"):
        return 1, "\n".join(
            (
                "STATUS: FAIL",
                "ROUTING DELTA: blocked; missing Managed Routing Block",
                "CAPABILITY DELTA: none",
                "MODEL DELTA: No model-assignment changes proposed",
                "FILES: none",
                "PRESERVED: Everything else preserved",
                "CHECKLIST: use routing bootstrap for repositories without a routing contract",
                "",
            )
        )

    changed: list[str] = []
    capability_changes: list[str] = []
    model_changes: list[str] = []
    failures: list[str] = []
    for proposed in files_in(candidate):
        relative = proposed.relative_to(candidate).as_posix()
        current = repository / relative
        if not is_managed_path(relative):
            failures.append(f"FAIL unmanaged-refresh-file {relative}")
        if relative not in CONTROL_FILES and relative not in approved_files:
            failures.append(f"FAIL unapproved-file {relative}")
        if not current.is_file() or current.read_bytes() != proposed.read_bytes():
            changed.append(relative)
            before = current.read_text(errors="replace") if current.is_file() else ""
            after = proposed.read_text(errors="replace")
            if relative == "AGENTS.md":
                before_block = managed_block(before)
                after_block = managed_block(after)
                if before_block is None or after_block is None or before_block[::2] != after_block[::2]:
                    failures.append("FAIL unmanaged-agents-edit AGENTS.md")
            for old, new in CAPABILITY_RENAMES:
                if old in before and new in after:
                    capability_changes.append(f"{old} -> {new}")
            if relative.endswith(".toml"):
                old_model, old_reasoning = profile_assignment(current)
                new_model, new_reasoning = profile_assignment(proposed)
                if (old_model, old_reasoning) != (new_model, new_reasoning):
                    model_changes.append(
                        f"{relative}: {old_model or 'none'} / {old_reasoning or 'none'} -> "
                        f"{new_model or 'none'} / {new_reasoning or 'none'}"
                    )

    if not changed:
        failures.append("FAIL no-routing-delta")
    valid, findings = validate(repository, candidate)
    failures.extend(line for line in findings if line.startswith("FAIL "))
    warnings = [line for line in findings if line.startswith("WARN ")]
    status = "FAIL" if failures or not valid else "WARN" if warnings else "PASS"
    rows = routing_rows(repository, candidate, changed)
    routing_delta = "; ".join(rows) if rows else "none"
    capability_delta = "; ".join(capability_changes) if capability_changes else "none"
    if capability_changes:
        capability_delta += f" ({', '.join(changed)})"
    model_delta = "; ".join(model_changes) if model_changes else "No model-assignment changes proposed"
    lines = [
        f"STATUS: {status}",
        f"ROUTING DELTA: {routing_delta}",
        f"CAPABILITY DELTA: {capability_delta}",
        f"MODEL DELTA: {model_delta}",
        f"FILES: {', '.join(changed) if changed else 'none'}",
        "PRESERVED: Everything else preserved",
    ]
    lines.extend(failures)
    lines.extend(warnings)
    lines.append("CHECKLIST: review affected rows; approve minimal patches; revalidate after approved changes")
    return (1 if failures else 0), "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--routing", required=True, type=Path, help="Proposed changed files only.")
    parser.add_argument("--approved-file", action="append", default=[])
    arguments = parser.parse_args()
    code, output = render(arguments.repository, arguments.routing, set(arguments.approved_file))
    print(output, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
