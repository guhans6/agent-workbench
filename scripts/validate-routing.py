#!/usr/bin/env python3
"""Validate a proposed repository routing overlay through a stable CLI seam."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import tomllib


CONTROL_FILES = {"routing.toml"}


@dataclass(frozen=True, order=True)
class Finding:
    severity: str
    code: str
    subject: str

    def render(self) -> str:
        return f"{self.severity} {self.code} {self.subject}"


def load_toml(path: Path, findings: list[Finding], relative_path: str) -> dict[str, object] | None:
    try:
        return tomllib.loads(path.read_text())
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        findings.append(Finding("FAIL", "malformed-toml", relative_path))
        return None


def valid_frontmatter(path: Path) -> bool:
    try:
        lines = path.read_text().splitlines()
    except (OSError, UnicodeError):
        return False
    if len(lines) < 3 or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    try:
        result = subprocess.run(
            [
                "ruby",
                "-e",
                'require "yaml"; document = YAML.safe_load(STDIN.read, aliases: false); exit(document.is_a?(Hash) ? 0 : 1)',
            ],
            input="\n".join(lines[: end + 1]),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return result.returncode == 0


def text_corpus(root: Path) -> str:
    parts: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            parts.append(path.read_text())
        except (OSError, UnicodeError):
            pass
    return "\n".join(parts)


def validate(repository: Path, routing: Path, approved_files: set[str], bootstrap: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    routing_path = routing / "routing.toml"
    if routing_path.is_file():
        configuration = load_toml(routing_path, findings, "routing.toml")
    elif bootstrap:
        configuration = {}
    else:
        findings.append(Finding("FAIL", "missing-routing-configuration", "routing.toml"))
        configuration = None
    observation_path = repository / ".routing-observations.toml"
    observations = load_toml(observation_path, findings, ".routing-observations.toml") if observation_path.is_file() else {}

    for path in sorted(routing.glob("skills/*/SKILL.md")):
        if not valid_frontmatter(path):
            findings.append(Finding("FAIL", "malformed-frontmatter", path.relative_to(routing).as_posix()))

    profiles: dict[str, dict[str, object]] = {}
    for path in sorted(routing.glob(".codex/agents/*.toml")):
        relative_path = path.relative_to(routing).as_posix()
        profile = load_toml(path, findings, relative_path)
        if profile is None:
            continue
        name = profile.get("name")
        if not isinstance(name, str) or not name:
            findings.append(Finding("FAIL", "missing-agent-name", relative_path))
            continue
        if name in profiles:
            findings.append(Finding("FAIL", "duplicate-agent", name))
        else:
            profiles[name] = profile

    profile_metadata: dict[str, dict[str, object]] = {}
    routed_profiles: set[str] = set()

    if configuration is not None:
        for metadata in configuration.get("profiles", []):
            if isinstance(metadata, dict) and isinstance(metadata.get("name"), str):
                profile_metadata[metadata["name"]] = metadata
        for route in configuration.get("routes", []):
            if isinstance(route, dict):
                profile_name = route.get("profile")
                if isinstance(profile_name, str):
                    routed_profiles.add(profile_name)
                    if profile_name not in profiles:
                        findings.append(Finding("FAIL", "missing-profile", profile_name))
        for pointer in configuration.get("context_pointers", []):
            if isinstance(pointer, str) and not (repository / pointer).exists():
                findings.append(Finding("WARN", "missing-context-pointer", pointer))

    available_models = set(observations.get("models", [])) if observations else set()
    unavailable_models = set(observations.get("unavailable_models", [])) if observations else set()
    available_skills = set(observations.get("skills", [])) if observations else set()
    available_tools = set(observations.get("tools", [])) if observations else set()
    repository_text = text_corpus(repository)

    for name, profile in profiles.items():
        if name not in routed_profiles:
            findings.append(Finding("WARN", "profile-without-trigger", name))
        model = profile.get("model")
        if isinstance(model, str):
            if model in unavailable_models:
                findings.append(Finding("FAIL", "unavailable-model", model))
            elif model not in available_models:
                findings.append(Finding("WARN", "unverifiable-model", model))
        metadata = profile_metadata.get(name, {})
        for required_field in ("model", "model_reasoning_effort", "sandbox_mode"):
            if not isinstance(profile.get(required_field), str) or not profile[required_field]:
                findings.append(Finding("FAIL", "missing-exact-assignment", f"{name}.{required_field}"))
        for skill in metadata.get("skills", []):
            if isinstance(skill, str) and skill not in available_skills and not (routing / "skills" / skill / "SKILL.md").exists():
                findings.append(Finding("FAIL", "missing-skill", skill))
        for tool in metadata.get("tools", []):
            if isinstance(tool, str) and tool not in available_tools:
                findings.append(Finding("FAIL", "missing-tool", tool))
        sandbox = profile.get("sandbox_mode")
        required_access = metadata.get("access_requirement")
        if isinstance(sandbox, str) and isinstance(required_access, str) and sandbox != required_access:
            findings.append(Finding("FAIL", "sandbox-contradiction", name))
        responsibility = metadata.get("responsibility")
        if isinstance(responsibility, str) and re.search(r"\b(any task|all tasks|everything)\b", responsibility, re.IGNORECASE):
            findings.append(Finding("WARN", "broad-profile", name))
        instructions = profile.get("developer_instructions")
        if isinstance(instructions, str) and len(instructions) >= 40 and instructions in repository_text:
            findings.append(Finding("WARN", "duplicated-instructions", name))

    for path in routing.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(routing).as_posix()
        if relative_path not in CONTROL_FILES and relative_path not in approved_files:
            findings.append(Finding("FAIL", "unapproved-file", relative_path))

    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--routing", required=True, type=Path)
    parser.add_argument("--approved-file", action="append", default=[])
    parser.add_argument("--bootstrap", action="store_true", help="Allow a managed block with no Repository-Specific Profiles.")
    arguments = parser.parse_args()
    findings = validate(arguments.repository, arguments.routing, set(arguments.approved_file), arguments.bootstrap)
    for finding in findings:
        print(finding.render())
    if any(finding.severity == "FAIL" for finding in findings):
        print("FAIL routing configuration has errors")
        return 1
    if findings:
        print("WARN routing configuration requires attention")
        return 0
    print("PASS routing configuration is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
