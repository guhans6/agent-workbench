from __future__ import annotations

import subprocess
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class RoutingSkillPortabilityTests(unittest.TestCase):
    def test_bootstrap_skill_bundles_runnable_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = root / "installed-skills" / "project-agent-architect"
            shutil.copytree(ROOT / "shared" / "skills" / "project-agent-architect", skill)
            command = skill / "scripts" / "bootstrap-routing.py"
            validator = skill / "scripts" / "validate-routing.py"
            repository = root / "unrelated-repository"
            repository.mkdir()
            (repository / "package.json").write_text('{"name":"portable"}\n')
            bootstrap = subprocess.run(
                [
                    sys.executable,
                    str(command),
                    "--repository",
                    str(repository),
                    "--global-profile",
                    "terra|normal implementation|gpt-5.6-terra|medium|workspace-write",
                ],
                cwd=repository,
                capture_output=True,
                text=True,
                check=False,
            )
            proposal = root / "proposal"
            proposal.mkdir()
            (proposal / "AGENTS.md").write_text("<!-- routing:start -->\nUse global profiles.\n<!-- routing:end -->\n")
            validation = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--repository",
                    str(repository),
                    "--routing",
                    str(proposal),
                    "--approved-file",
                    "AGENTS.md",
                    "--bootstrap",
                ],
                cwd=repository,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(bootstrap.returncode, 0, bootstrap.stdout + bootstrap.stderr)
        self.assertIn("STATUS: WARN", bootstrap.stdout)
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
        self.assertEqual(validation.stdout, "PASS routing configuration is structurally valid\n")

    def test_refresh_skill_bundles_runnable_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill = root / "installed-skills" / "refresh-project-agent-routing"
            shutil.copytree(ROOT / "shared" / "skills" / "refresh-project-agent-routing", skill)
            command = skill / "scripts" / "refresh-routing.py"
            repository = root / "unrelated-repository"
            candidate = root / "candidate"
            (repository / ".codex" / "agents").mkdir(parents=True)
            (candidate / ".codex" / "agents").mkdir(parents=True)
            (repository / "AGENTS.md").write_text("<!-- routing:start -->\nUse planner.\n<!-- routing:end -->\n")
            (repository / ".routing-observations.toml").write_text('models = ["gpt-5.6-terra"]\nskills = ["to-spec", "to-tickets"]\ntools = []\n')
            (repository / "routing.toml").write_text(
                'context_pointers = []\n[[routes]]\ntrigger = "planning"\nprofile = "planner"\n'
                '[[profiles]]\nname = "planner"\naccess_requirement = "workspace-write"\n'
                'responsibility = "Plan approved work."\nskills = ["to-spec", "to-tickets"]\ntools = []\n'
            )
            current_profile = (
                'name = "planner"\nmodel = "gpt-5.6-terra"\nmodel_reasoning_effort = "medium"\n'
                'sandbox_mode = "workspace-write"\ndeveloper_instructions = "Use to-prd and to-issues."\n'
            )
            (repository / ".codex" / "agents" / "planner.toml").write_text(current_profile)
            (candidate / ".codex" / "agents" / "planner.toml").write_text(
                current_profile.replace("to-prd and to-issues", "to-spec and to-tickets")
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(command),
                    "--repository",
                    str(repository),
                    "--routing",
                    str(candidate),
                    "--approved-file",
                    ".codex/agents/planner.toml",
                ],
                cwd=repository,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("STATUS: PASS", result.stdout)
        self.assertIn("CAPABILITY DELTA: to-prd -> to-spec; to-issues -> to-tickets", result.stdout)

    def test_bundled_helpers_match_the_canonical_implementations(self) -> None:
        pairs = (
            ("scripts/bootstrap-routing.py", "shared/skills/project-agent-architect/scripts/bootstrap-routing.py"),
            ("scripts/validate-routing.py", "shared/skills/project-agent-architect/scripts/validate-routing.py"),
            ("scripts/refresh-routing.py", "shared/skills/refresh-project-agent-routing/scripts/refresh-routing.py"),
            ("scripts/validate-routing.py", "shared/skills/refresh-project-agent-routing/scripts/validate-routing.py"),
        )
        for canonical, bundled in pairs:
            with self.subTest(bundled=bundled):
                self.assertEqual((ROOT / bundled).read_bytes(), (ROOT / canonical).read_bytes())


if __name__ == "__main__":
    unittest.main()
