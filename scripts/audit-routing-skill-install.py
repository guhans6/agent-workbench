#!/usr/bin/env python3
"""Verify that installed routing skill packages exactly match their sources."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


SKILLS = ("project-agent-architect", "refresh-project-agent-routing")
REQUIRED_FILES = {
    "project-agent-architect": {
        "SKILL.md",
        "agents/openai.yaml",
        "references/routing-contract.md",
        "scripts/bootstrap-routing.py",
        "scripts/validate-routing.py",
    },
    "refresh-project-agent-routing": {
        "SKILL.md",
        "agents/openai.yaml",
        "scripts/refresh-routing.py",
        "scripts/validate-routing.py",
    },
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def file_map(root: Path, skill: str) -> dict[str, bytes]:
    directory = root / skill
    if not directory.is_dir():
        return {}
    return {
        path.relative_to(directory).as_posix(): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def source_integrity(source_root: Path, skill: str) -> list[str]:
    result: list[str] = []
    directory = source_root / skill
    source = file_map(source_root, skill)
    for relative in sorted(REQUIRED_FILES[skill] - source.keys()):
        result.append(f"FAIL missing-source-file {skill}/{relative}")

    reachable: set[str] = set()
    pending = ["SKILL.md"]
    while pending:
        relative = pending.pop()
        if relative in reachable:
            continue
        reachable.add(relative)
        path = directory / relative
        if not path.is_file() or path.suffix != ".md":
            continue
        for target in MARKDOWN_LINK.findall(path.read_text(errors="replace")):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            resolved = (path.parent / target_path).resolve()
            try:
                target_relative = resolved.relative_to(directory.resolve()).as_posix()
            except ValueError:
                result.append(f"FAIL external-reference {skill}/{relative} -> {target}")
                continue
            if not resolved.is_file():
                result.append(f"FAIL missing-reference {skill}/{relative} -> {target}")
            elif resolved.suffix == ".md" and target_relative not in reachable:
                pending.append(target_relative)

    references = directory / "references"
    if references.is_dir():
        for path in sorted(references.rglob("*.md")):
            relative = path.relative_to(directory).as_posix()
            if relative not in reachable:
                result.append(f"FAIL orphan-reference {skill}/{relative}")
    return result


def findings(source_root: Path, installed_root: Path) -> list[str]:
    result: list[str] = []
    for skill in SKILLS:
        result.extend(source_integrity(source_root, skill))
        source = file_map(source_root, skill)
        installed = file_map(installed_root, skill)
        for relative in sorted(source.keys() - installed.keys()):
            result.append(f"FAIL missing-file {skill}/{relative}")
        for relative in sorted(installed.keys() - source.keys()):
            result.append(f"FAIL extra-file {skill}/{relative}")
        for relative in sorted(source.keys() & installed.keys()):
            if source[relative] != installed[relative]:
                result.append(f"FAIL changed-file {skill}/{relative}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--installed-root", required=True, type=Path)
    arguments = parser.parse_args()
    result = findings(arguments.source_root, arguments.installed_root)
    if result:
        print("\n".join(result))
        print("FAIL routing skill package audit failed")
        return 1
    print("PASS routing skill installation matches source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
