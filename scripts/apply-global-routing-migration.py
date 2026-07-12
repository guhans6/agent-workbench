#!/usr/bin/env python3
"""Safely apply a reviewed migration to an explicitly selected global Codex root."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path


START, END = "<!-- routing:start -->", "<!-- routing:end -->"
PATCH_FIELDS = ("model", "model_reasoning_effort", "sandbox_mode")


def replace_block(current: str, proposed: str) -> str:
    """Replace exactly one managed span, retaining every unrelated instruction byte."""
    if current.count(START) > 1 or current.count(END) > 1 or proposed.count(START) != 1 or proposed.count(END) != 1:
        raise ValueError("managed routing block must be unique")
    block = proposed.split(START, 1)[1].split(END, 1)[0]
    if current.count(START) == 0 and current.count(END) == 0:
        separator = "" if not current or current.endswith("\n") else "\n"
        return f"{current}{separator}\n{START}{block}{END}\n"
    if current.count(START) != 1 or current.count(END) != 1 or current.index(START) > current.index(END):
        raise ValueError("live AGENTS.md has an invalid managed routing block")
    before, rest = current.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}{block}{END}{after}"


def patch_scalar(text: str, key: str, value: str) -> str:
    import re
    pattern = rf"(?m)^{re.escape(key)}\s*=\s*.*$"
    replacement = f'{key} = "{value}"'
    if not re.search(pattern, text):
        raise ValueError(f"live profile is missing {key}")
    return re.sub(pattern, replacement, text, count=1)


def validate(source: Path, observed: Path, policy: Path, agents: Path) -> None:
    command = ["python3", str(Path(__file__).with_name("validate-global-routing.py")), "--source", str(source), "--observed", str(observed), "--shared-policy", str(policy), "--live-agents", str(agents)]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(result.stdout.strip())


def validate_installed(source: Path, global_root: Path, profiles: dict[str, dict[str, object]]) -> None:
    if managed_block_text(global_root / "AGENTS.md") != managed_block_text(source / "AGENTS.md"):
        raise ValueError("installed managed routing block mismatch")
    for name, metadata in profiles.items():
        target = global_root / "agents" / f"{name}.toml"
        if not target.is_file():
            raise ValueError(f"missing installed profile {name}")
        installed = tomllib.loads(target.read_text())
        if (installed.get("model"), installed.get("model_reasoning_effort"), installed.get("sandbox_mode")) != (metadata["model"], metadata["reasoning"], metadata["access"]):
            raise ValueError(f"installed assignment mismatch {name}")


def managed_block_text(path: Path) -> str:
    text = path.read_text()
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("managed routing block must be unique")
    return text.split(START, 1)[1].split(END, 1)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--observed", required=True, type=Path)
    parser.add_argument("--shared-policy", required=True, type=Path)
    parser.add_argument("--global-root", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="Perform writes; without this flag prints the validated plan only.")
    args = parser.parse_args()
    agents = args.global_root / "agents"
    validate(args.source, args.observed, args.shared_policy, agents)
    migration = tomllib.loads((args.source / "migration.toml").read_text())
    backup = args.global_root / ".routing-backups" / dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"VALIDATED: {args.global_root}")
    print(f"BACKUP: {backup}")
    print("PLAN: replace only the managed AGENTS.md block; install replacements; patch same-name model/reasoning/sandbox fields; validate; then remove no legacy files automatically.")
    if not args.apply:
        return 0
    backup.mkdir(parents=True)
    shutil.copy2(args.global_root / "AGENTS.md", backup / "AGENTS.md")
    shutil.copytree(agents, backup / "agents")
    try:
        proposed_agents = (args.source / "AGENTS.md").read_text()
        live_agents = args.global_root / "AGENTS.md"
        live_agents.write_text(replace_block(live_agents.read_text(), proposed_agents))
        profiles = {item["name"]: item for item in migration["proposed_profiles"]}
        for item in migration["existing_agents"]:
            name, disposition = item["name"], item["disposition"]
            target = agents / f"{name}.toml"
            if disposition == "modify":
                text = target.read_text()
                metadata = profiles[name]
                for key, metadata_key in zip(PATCH_FIELDS, ("model", "reasoning", "access"), strict=True):
                    text = patch_scalar(text, key, metadata[metadata_key])
                target.write_text(text)
        patch_names = {item["name"] for item in migration["existing_agents"] if item["disposition"] == "modify"}
        for name in profiles:
            if name in patch_names:
                continue
            shutil.copy2(args.source / "agents" / f"{name}.toml", agents / f"{name}.toml")
        validate_installed(args.source, args.global_root, profiles)
    except Exception:
        shutil.copy2(backup / "AGENTS.md", args.global_root / "AGENTS.md")
        shutil.rmtree(agents)
        shutil.copytree(backup / "agents", agents)
        raise
    print("APPLIED: validation passed; legacy removal remains a separate explicit operation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
