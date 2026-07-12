#!/usr/bin/env python3
"""Run the read-only global-first routing experiment for issue #8."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "bootstrap-routing.py"
MIGRATION = ROOT / "platforms" / "codex" / "migrations" / "gpt-5.6" / "migration.toml"
PROFILE_NAMES = (
    "global_scout",
    "spark_editor_gpt56",
    "global_worker",
    "global_docs_researcher",
    "global_debugger",
    "global_reviewer",
)


def git_snapshot(repository: Path) -> dict[str, str]:
    result = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        head = subprocess.run(
            ["git", "-C", str(repository), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        return {"kind": "git", "head": head.stdout.strip(), "status": result.stdout}

    digest = hashlib.sha256()
    for path in sorted(path for path in repository.rglob("*") if path.is_file()):
        digest.update(path.relative_to(repository).as_posix().encode())
        digest.update(path.read_bytes())
    return {"kind": "tree", "sha256": digest.hexdigest()}


def profiles() -> dict[str, dict[str, str | list[str]]]:
    with MIGRATION.open("rb") as source:
        migration = tomllib.load(source)
    return {
        profile["name"]: profile
        for profile in migration["proposed_profiles"]
        if profile["name"] in PROFILE_NAMES
    }


def bootstrap(repository: Path, global_profiles: dict[str, dict[str, str | list[str]]]) -> dict[str, int | str]:
    command = [sys.executable, str(BOOTSTRAP), "--repository", str(repository)]
    for name in PROFILE_NAMES:
        profile = global_profiles[name]
        command.extend(
            (
                "--global-profile",
                "|".join(
                    (
                        name,
                        str(profile["trigger"]),
                        str(profile["model"]),
                        str(profile["reasoning"]),
                        str(profile["access"]),
                    )
                ),
            )
        )
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return {"returncode": result.returncode, "surface": result.stdout}


def clean_projection(repository: Path) -> tempfile.TemporaryDirectory[str]:
    projection = tempfile.TemporaryDirectory(prefix="issue-8-routing-projection-")
    root = Path(projection.name)
    for relative_path in ("AGENTS.md", "README.md", "Cargo.toml"):
        source = repository / relative_path
        if source.is_file():
            destination = root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    return projection


def simulation(name: str, route: str, profiles_by_name: dict[str, dict[str, str | list[str]]], escalation: str) -> dict[str, str]:
    profile = profiles_by_name[route]
    return {
        "scenario": name,
        "profile": route,
        "model": str(profile["model"]),
        "reasoning": str(profile["reasoning"]),
        "access": str(profile["access"]),
        "escalation": escalation,
    }


def run(repository: Path) -> dict[str, object]:
    before = git_snapshot(repository)
    global_profiles = profiles()
    actual = bootstrap(repository, global_profiles)
    with clean_projection(repository) as projection:
        projected = bootstrap(Path(projection), global_profiles)
    after = git_snapshot(repository)
    if before != after:
        raise RuntimeError("target repository changed during the read-only experiment")

    simulations = [
        simulation("bounded source and test inventory", "global_scout", global_profiles, "none"),
        simulation("one confirmed README wording correction", "spark_editor_gpt56", global_profiles, "none"),
        simulation("approved Rust behavior change with focused test", "global_worker", global_profiles, "none"),
        simulation("concrete Luna inventory failure", "global_worker", global_profiles, "Luna to Terra once"),
        simulation("repeated Terra failure with conflicting runtime evidence", "global_debugger", global_profiles, "Terra to one Sol/high route"),
    ]
    actual_surface = str(actual["surface"])
    projected_surface = str(projected["surface"])
    approval_surface_lines = len(projected_surface.rstrip().splitlines())
    warnings = sum(
        not surface.startswith("STATUS: PASS") for surface in (actual_surface, projected_surface)
    )
    local_profiles_proposed = 0 if "no Repository-Specific Profiles proposed" in projected_surface else None
    return {
        "target": {"path": str(repository), "before": before, "after": after},
        "actual_bootstrap": actual,
        "projection_bootstrap": projected,
        "simulations": simulations,
        "metrics": {
            "global_profiles_considered": len(PROFILE_NAMES),
            "local_profiles_proposed": local_profiles_proposed,
            "routing_corrections": sum(item["profile"] != expected for item, expected in zip(simulations, ("global_scout", "spark_editor_gpt56", "global_worker", "global_worker", "global_debugger"))),
            "automatic_sol_high_routes": sum(item["model"] == "gpt-5.6-sol" for item in simulations),
            "approval_surface_lines": approval_surface_lines,
            "warnings": warnings,
        },
        "rework_risk": "medium: the live target has an existing local routing contract, so the clean projection is a controlled counterfactual",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    if not arguments.repository.is_dir():
        parser.error("repository must be an existing directory")
    if arguments.output.resolve().is_relative_to(arguments.repository.resolve()):
        parser.error("output must be outside the protected repository")
    result = run(arguments.repository)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"wrote {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
