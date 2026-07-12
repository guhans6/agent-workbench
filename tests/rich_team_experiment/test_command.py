from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "validate-rich-team-refresh-experiment.py"
REFRESH_COMMAND = ROOT / "scripts" / "refresh-routing.py"


class RichTeamRefreshExperimentTests(unittest.TestCase):
    ROLES = (
        "docs_researcher",
        "explorer",
        "implementer",
        "investigator",
        "issue_slicer",
        "reviewer",
        "scout",
        "visual_tester",
    )

    def write_target(self, root: Path) -> None:
        (root / ".codex" / "agents").mkdir(parents=True)
        (root / "AGENTS.md").write_text(
            "Before\n<!-- routing:start -->\nUse scout for bounded discovery, explorer for analysis, and investigator for unresolved ambiguity.\n<!-- routing:end -->\nAfter\n"
        )
        (root / ".agents" / "skills" / "team").mkdir(parents=True)
        (root / ".agents" / "skills" / "team" / "SKILL.md").write_text(
            "Use ask-matt, then to-prd and to-issues. Context7 is plugin-backed; duplicate standalone MCP is disabled.\n"
            + "\n".join(f"visualcompanion_{role}" for role in self.ROLES)
            + "\n"
        )
        for role in self.ROLES:
            evidence = {
                "docs_researcher": "Context7",
                "explorer": "Svelte/React/Tauri/Rust",
                "implementer": "typed API/Tauri",
                "issue_slicer": "GitHub issue workflow",
                "reviewer": "artifact-contract",
                "visual_tester": "visual-ui-change-guard",
                "scout": "bounded file, symbol, test, dependency, configuration, and command inventories",
                "investigator": "unresolved Agent-Native parity, migration, artifact-contract, and native-boundary ambiguity",
            }[role]
            sandbox = "workspace-write" if role in {"implementer", "visual_tester"} else "read-only"
            (root / ".codex" / "agents" / f"visualcompanion_{role}.toml").write_text(
                textwrap.dedent(
                    f'''\
                    name = "visualcompanion_{role}"
                    description = "A distinct VisualCompanion {role} lane."
                    model = "gpt-5.6-terra"
                    model_reasoning_effort = "medium"
                    sandbox_mode = "{sandbox}"
                    developer_instructions = "Use VisualCompanion evidence in this {role} lane; {evidence}; use to-prd and to-issues for planning work."
                    '''
                )
            )
        (root / ".routing-observations.toml").write_text('models = ["gpt-5.6-terra"]\nskills = []\ntools = []\n')
        routing = ['context_pointers = ["AGENTS.md"]\n']
        for role in self.ROLES:
            access = "workspace-write" if role in {"implementer", "visual_tester"} else "read-only"
            name = f"visualcompanion_{role}"
            routing.extend(
                (
                    "[[routes]]\n",
                    f'trigger = "{role}"\n',
                    f'profile = "{name}"\n\n',
                    "[[profiles]]\n",
                    f'name = "{name}"\n',
                    f'access_requirement = "{access}"\n',
                    'responsibility = "A bounded local lane."\n',
                    "skills = []\ntools = []\n\n",
                )
            )
        (root / "routing.toml").write_text("".join(routing))

    def run_experiment(self, repository: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(COMMAND), "--repository", str(repository)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_rich_team_reduction_is_evidence_based_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "Companion"
            self.write_target(repository)
            dirty_file = repository / "active-work.md"
            dirty_file.write_text("do not touch\n")
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            subprocess.run(["git", "-C", str(repository), "add", "AGENTS.md", ".agents", "routing.toml", ".routing-observations.toml"], check=True)
            for role in self.ROLES:
                if role not in {"scout", "investigator"}:
                    subprocess.run(
                        ["git", "-C", str(repository), "add", f".codex/agents/visualcompanion_{role}.toml"],
                        check=True,
                    )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "-c",
                    "user.email=test@example.com",
                    "-c",
                    "user.name=Test",
                    "commit",
                    "-qm",
                    "fixture",
                ],
                check=True,
            )
            before = subprocess.check_output(["git", "-C", str(repository), "status", "--porcelain=v1"], text=True)

            result = self.run_experiment(repository)

            after = subprocess.check_output(["git", "-C", str(repository), "status", "--porcelain=v1"], text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(before, after)
            self.assertIn("STATUS: PASS", result.stdout)
            self.assertIn("TARGET CONTRACT: legacy rich team; no target patch applied", result.stdout)
            self.assertIn("DIRTY WORK PRESERVED: yes", result.stdout)
            self.assertIn("DIRTY SCOPE (3):", result.stdout)
            self.assertIn("?? active-work.md", result.stdout)
            self.assertIn("CURRENT PROFILES: 8", result.stdout)
            self.assertIn("ADMITTED LOCAL PROFILES: 6", result.stdout)
            self.assertIn("REMOVAL RECOMMENDATIONS: visualcompanion_investigator, visualcompanion_scout", result.stdout)
            self.assertIn("MODEL MIGRATIONS: none (separate from role reduction)", result.stdout)
            self.assertIn("CAPABILITY DELTA: planning aliases need to-prd -> to-spec and to-issues -> to-tickets", result.stdout)
            self.assertIn("PLUGIN DELTA: Context7 remains plugin-backed; no standalone MCP is required", result.stdout)
            self.assertRegex(result.stdout, r"APPROVAL LENGTH: delta 7 lines; full roster 10 lines; reduction 30%")

    def test_missing_rich_team_role_blocks_a_reduction_recommendation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "Companion"
            self.write_target(repository)
            (repository / ".codex" / "agents" / "visualcompanion_scout.toml").unlink()

            result = self.run_experiment(repository)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("STATUS: FAIL", result.stdout)
            self.assertIn("FAIL missing-rich-team-role visualcompanion_scout", result.stdout)

    def test_rejects_an_admitted_role_without_local_admission_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "Companion"
            self.write_target(repository)
            profile = repository / ".codex" / "agents" / "visualcompanion_reviewer.toml"
            profile.write_text(profile.read_text().replace('description = "A distinct VisualCompanion reviewer lane."\n', ""))

            result = self.run_experiment(repository)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL admission-rejected visualcompanion_reviewer: recognizable-task-class", result.stdout)

    def test_requires_observed_legacy_aliases_before_recommending_the_rename(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "Companion"
            self.write_target(repository)
            skill = repository / ".agents" / "skills" / "team" / "SKILL.md"
            skill.write_text(skill.read_text().replace("to-prd and to-issues", "to-spec and to-tickets"))

            result = self.run_experiment(repository)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FAIL missing-legacy-planning-aliases", result.stdout)

    def test_rich_team_refresh_is_delta_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "Companion"
            candidate = Path(temporary_directory) / "candidate"
            self.write_target(repository)
            source = repository / ".codex" / "agents" / "visualcompanion_issue_slicer.toml"
            destination = candidate / ".codex" / "agents" / source.name
            destination.parent.mkdir(parents=True)
            destination.write_text(source.read_text().replace("to-prd and to-issues", "to-spec and to-tickets"))

            result = subprocess.run(
                [
                    sys.executable,
                    str(REFRESH_COMMAND),
                    "--repository",
                    str(repository),
                    "--routing",
                    str(candidate),
                    "--approved-file",
                    ".codex/agents/visualcompanion_issue_slicer.toml",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("ROUTING DELTA: visualcompanion_issue_slicer | issue_slicer", result.stdout)
            self.assertIn("CAPABILITY DELTA: to-prd -> to-spec; to-issues -> to-tickets", result.stdout)
            self.assertIn("FILES: .codex/agents/visualcompanion_issue_slicer.toml", result.stdout)
            self.assertIn("PRESERVED: Everything else preserved", result.stdout)


if __name__ == "__main__":
    unittest.main()
