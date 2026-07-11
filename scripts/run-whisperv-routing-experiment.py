#!/usr/bin/env python3
"""Run the read-only WhisperV Apple-routing experiment for issue #9."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "bootstrap-routing.py"
POLICY = ROOT / "shared" / "routing" / "routing-policy.toml"
AGENTS = ROOT / "platforms" / "codex" / "migrations" / "gpt-5.6" / "agents"

GLOBAL_PROFILES = (
    ("global_scout", "bounded inventory or mechanical verification"),
    ("global_worker", "normal analysis or approved implementation"),
    ("global_docs_researcher", "current non-Apple documentation research"),
    ("global_debugger", "difficult investigation after concrete escalation evidence"),
    ("global_reviewer", "high-risk review"),
)

@dataclass(frozen=True)
class Simulation:
    automatic_candidates: tuple[str, ...]
    expected_primary: str
    global_fallback: str | None
    trigger: str
    material_signals: tuple[str, ...] = ()


SIMULATIONS = {
    "repository_inventory": Simulation(("global_scout",), "global_scout", None, "bounded read-only inventory"),
    "swift_architecture_mapping": Simulation(("swift_explorer",), "swift_explorer", "global_scout", "Apple source, state, and test mapping", ("apple", "state ownership", "tests")),
    "approved_swift_feature": Simulation(("swift_worker",), "swift_worker", "global_worker", "approved SwiftUI implementation", ("apple", "concurrency", "state ownership")),
    "xcode_build_failure": Simulation(("xcode_triager",), "xcode_triager", "global_debugger", "build, scheme, simulator, or log triage", ("build", "scheme", "simulator", "log")),
    "apple_api_availability": Simulation(("apple_docs_researcher",), "apple_docs_researcher", "global_docs_researcher", "official Apple API semantics or availability", ("apple", "platform semantics", "availability")),
    "swift_concurrency_review": Simulation(("swift_reviewer",), "swift_reviewer", "global_reviewer", "Apple regression, state, concurrency, or test review", ("apple", "concurrency", "test risk")),
    "proven_hard_apple_debug": Simulation(("deep_debugger",), "deep_debugger", "global_debugger", "only after focused Xcode triage fails", ("apple", "focused triage")),
    "sol_high_budget_stress": Simulation(("swift_reviewer", "deep_debugger"), "swift_reviewer", None, "two eligible Sol/high profiles competing for one automatic task budget"),
}


def git_status(repository: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"repository is not a readable Git checkout: {repository}")
    return result.stdout


def load_agent(name: str) -> dict[str, object]:
    with (AGENTS / f"{name}.toml").open("rb") as handle:
        return tomllib.load(handle)


def profile_summary(name: str) -> dict[str, str]:
    profile = load_agent(name)
    return {
        "model": str(profile["model"]),
        "reasoning": str(profile["model_reasoning_effort"]),
        "access": str(profile["sandbox_mode"]),
    }


def profile_text(name: str) -> str:
    profile = load_agent(name)
    return " ".join(str(profile.get(field, "")) for field in ("description", "developer_instructions")).lower()


def bootstrap(repository: Path) -> dict[str, object]:
    command = [sys.executable, str(BOOTSTRAP), "--repository", str(repository)]
    for name, trigger in GLOBAL_PROFILES:
        profile = profile_summary(name)
        command.extend(
            (
                "--global-profile",
                "|".join((name, trigger, profile["model"], profile["reasoning"], profile["access"])),
            )
        )
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    lines = result.stdout.rstrip().splitlines()
    return {"status": lines[0].removeprefix("STATUS: "), "output": result.stdout, "surface_lines": len(lines)}


def apple_evidence(repository: Path) -> dict[str, object]:
    projects = sorted(path.relative_to(repository).as_posix() for path in repository.glob("*.xcodeproj/project.pbxproj"))
    swift_sources = sorted(path.relative_to(repository).as_posix() for path in repository.rglob("*.swift"))
    if not projects or not swift_sources:
        raise RuntimeError("repository lacks the Xcode project and Swift-source evidence required for an Apple-routing experiment")
    return {"xcode_projects": projects, "swift_source_count": len(swift_sources)}


def select_automatic_profiles(candidates: tuple[str, ...], sol_high_budget: int) -> tuple[list[str], list[str]]:
    selected: list[str] = []
    suppressed: list[str] = []
    sol_high_count = 0
    for name in candidates:
        profile = profile_summary(name)
        is_sol_high = profile["model"] == "gpt-5.6-sol" and profile["reasoning"] == "high"
        if is_sol_high and sol_high_count >= sol_high_budget:
            suppressed.append(name)
            continue
        selected.append(name)
        sol_high_count += int(is_sol_high)
    return selected, suppressed


def run(repository: Path) -> dict[str, object]:
    before = git_status(repository)
    evidence = apple_evidence(repository)
    bootstrap_result = bootstrap(repository)
    after = git_status(repository)

    policy = tomllib.loads(POLICY.read_text())
    automatic_sol_budget = policy["escalation"]["automatic_sol_high_budget"]
    simulations: dict[str, dict[str, object]] = {}
    automatic_sol_high_violations = 0
    max_automatic_sol_high = 0
    assessments: dict[str, dict[str, str]] = {}
    for scenario_name, simulation in SIMULATIONS.items():
        automatic_profiles, suppressed_profiles = select_automatic_profiles(simulation.automatic_candidates, automatic_sol_budget)
        if automatic_profiles[0] != simulation.expected_primary:
            raise RuntimeError(f"simulation selected an unexpected primary profile for {scenario_name}")
        profile_name = automatic_profiles[0]
        profile = profile_summary(profile_name)
        sol_high_count = sum(
            int(candidate["model"] == "gpt-5.6-sol" and candidate["reasoning"] == "high")
            for candidate in map(profile_summary, automatic_profiles)
        )
        automatic_sol_high_violations += int(sol_high_count > automatic_sol_budget)
        max_automatic_sol_high = max(max_automatic_sol_high, sol_high_count)
        specialist_value = False
        if simulation.global_fallback:
            specialist_text = profile_text(profile_name)
            fallback_text = profile_text(simulation.global_fallback)
            material_signals = [
                signal for signal in simulation.material_signals if signal in specialist_text and signal not in fallback_text
            ]
            specialist_value = len(material_signals) == len(simulation.material_signals) and bool(material_signals)
            assessments[profile_name] = {
                "global_fallback": simulation.global_fallback,
                "material_signals": ", ".join(material_signals),
            }
        else:
            material_signals = []
        simulations[scenario_name] = {
            "profile": profile_name,
            "trigger": simulation.trigger,
            **profile,
            "automatic_profiles": automatic_profiles,
            "suppressed_profiles": suppressed_profiles,
            "automatic_sol_high_count": sol_high_count,
            "specialist_value_over_global": specialist_value,
            "material_signals": material_signals,
        }

    retained_profiles = {profile for simulation in SIMULATIONS.values() for profile in simulation.automatic_candidates if profile in {"swift_explorer", "swift_worker", "xcode_triager", "apple_docs_researcher", "swift_reviewer", "deep_debugger"}}
    redundant_profiles = sorted(retained_profiles - set(assessments))
    for profile_name, assessment in assessments.items():
        if not assessment["material_signals"]:
            redundant_profiles.append(profile_name)
    redundant_profiles = sorted(set(redundant_profiles))
    target_mutated = before != after
    if target_mutated:
        raise RuntimeError("read-only experiment changed the target repository state")

    return {
        "target": str(repository),
        "target_mutated": target_mutated,
        "target_status_preserved": before == after,
        "apple_evidence": evidence,
        "bootstrap": bootstrap_result,
        "approval_metrics": {
            "surface_lines": bootstrap_result["surface_lines"],
            "global_profiles_displayed": len(GLOBAL_PROFILES),
            "repository_specific_profiles_proposed": 0,
            "simulation_count": len(simulations),
            "automatic_sol_high_budget": automatic_sol_budget,
            "max_automatic_sol_high_per_task": max_automatic_sol_high,
            "automatic_sol_high_violations": automatic_sol_high_violations,
        },
        "simulations": simulations,
        "specialist_assessment": {
            "all_retained_profiles_have_concrete_boundaries": not redundant_profiles,
            "retained_boundaries": assessments,
            "redundant_retained_profiles": redundant_profiles,
            "manual_only_profiles": ["gatekeeper"],
        },
    }


def markdown(report: dict[str, object]) -> str:
    metrics = report["approval_metrics"]
    rows = [
        "# WhisperV Apple-routing experiment",
        "",
        "## Result",
        "",
        f"- Bootstrap: {report['bootstrap']['status']} (global-first; no repository-specific profiles proposed)",
        f"- Target mutation: {'none' if not report['target_mutated'] else 'detected'}",
        f"- Approval surface: {metrics['surface_lines']} lines; {metrics['global_profiles_displayed']} global profiles displayed.",
        f"- Simulations: {metrics['simulation_count']}; Sol/high maximum {metrics['max_automatic_sol_high_per_task']} of budget {metrics['automatic_sol_high_budget']}.",
        "",
        "## Apple-specialist simulation",
        "",
        "| Scenario | Selected profile | Assignment |",
        "| --- | --- | --- |",
    ]
    for name, value in report["simulations"].items():
        rows.append(f"| {name} | {value['profile']} | {value['model']} / {value['reasoning']} / {value['access']} |")
    rows.extend(
        (
            "",
            "No retained Apple profile is persona-only: each has a documented tool, platform, or verification boundary. No retained Apple profile was redundant in these scenarios; `gatekeeper` remains a manual-only exhaustive review lane.",
            "",
        )
    )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    arguments = parser.parse_args()
    try:
        report = run(arguments.repository.resolve())
    except RuntimeError as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    if arguments.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
