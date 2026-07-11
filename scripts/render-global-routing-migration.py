#!/usr/bin/env python3
"""Render the reviewable current-to-proposed global routing delta."""

from __future__ import annotations

import argparse
from pathlib import Path
import tomllib


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        migration = tomllib.loads((arguments.source / "migration.toml").read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        parser.error(f"cannot read migration.toml: {error}")
    print("STATUS: PROPOSED")
    print("RECOMMENDATION: run the separate Sol/high read-only review before applying any global runtime change")
    for agent in migration.get("existing_agents", []):
        if not isinstance(agent, dict):
            continue
        name = agent.get("name", "unknown")
        disposition = agent.get("disposition", "unknown")
        current = f"{agent.get('current_model', 'none')} / {agent.get('current_reasoning', 'none')}"
        proposed = f"{agent.get('proposed_model', 'none')} / {agent.get('proposed_reasoning', 'none')}"
        replacement = agent.get("replacement", "none")
        action = "patch only model, reasoning, and sandbox; preserve description and instructions" if disposition == "modify" else "install then validate before removal"
        print(f"AGENT DELTA: {name} | {disposition} | {current} -> {proposed} | {replacement} | {action}")
    for profile in migration.get("proposed_profiles", []):
        if not isinstance(profile, dict):
            continue
        skills = ", ".join(profile.get("skills", []))
        print(
            f"ROUTING: {profile.get('name', 'unknown')} | {profile.get('trigger', 'unspecified')} | {profile.get('model', 'none')} | "
            f"{profile.get('reasoning', 'none')} | {profile.get('access', 'none')} | {skills or 'none'}"
        )
    print("ATTENTION: install new global profiles before retiring legacy generic profiles; patch same-name profiles minimally; no silent fallback")
    print("FILES: AGENTS.md; agents/*.toml")
    print("CHECKLIST: verify live inventory; run Sol review; dry-run; back up; install or patch; validate; then separately consider removal")
    print("GLOBAL RUNTIME: unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
