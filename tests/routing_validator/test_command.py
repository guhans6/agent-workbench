from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "validate-routing.py"


class ValidatorCommandTests(unittest.TestCase):
    OBSERVED = (
        'models = ["gpt-5.6-terra"]\n'
        'unavailable_models = ["gpt-5.6-sol"]\n'
        'skills = ["implement"]\n'
        'tools = ["git"]\n'
    )
    ROUTE = (
        'context_pointers = ["CONTEXT.md"]\n\n'
        '[[routes]]\ntrigger = "normal implementation"\nprofile = "worker"\n'
        '\n[[profiles]]\nname = "worker"\naccess_requirement = "workspace-write"\n'
        'responsibility = "Implement approved repository changes."\n'
        'skills = ["implement"]\ntools = []\n'
    )
    PROFILE = (
        'name = "worker"\ndescription = "Normal repository implementation worker."\n'
        'model = "gpt-5.6-terra"\nmodel_reasoning_effort = "medium"\n'
        'sandbox_mode = "workspace-write"\n'
        'developer_instructions = "Implement approved repository changes."\n'
    )

    def run_validator(
        self,
        repository_files: dict[str, str],
        routing_files: dict[str, str],
        approved_files: tuple[str, ...] = ("AGENTS.md", ".codex/agents/worker.toml"),
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            fixture = Path(temporary_directory)
            repository = fixture / "repository"
            routing = fixture / "routing"
            self.write_tree(repository, repository_files)
            self.write_tree(routing, routing_files)
            command = [
                sys.executable,
                str(COMMAND),
                "--repository",
                str(repository),
                "--routing",
                str(routing),
            ]
            for approved_file in approved_files:
                command.extend(("--approved-file", approved_file))
            return subprocess.run(command, capture_output=True, text=True, check=False)

    @staticmethod
    def write_tree(root: Path, files: dict[str, str]) -> None:
        for relative_path, contents in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(contents).lstrip())

    def test_valid_minimal_routing_passes(self) -> None:
        result = self.run_validator(
            repository_files={
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
            },
            routing_files={
                "routing.toml": self.ROUTE,
                ".codex/agents/worker.toml": self.PROFILE,
                "AGENTS.md": "<!-- routing:start -->\nUse worker for normal implementation.\n<!-- routing:end -->\n",
            },
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "PASS routing configuration is structurally valid\n")

    def test_missing_routing_configuration_fails(self) -> None:
        result = self.run_validator(
            repository_files={".routing-observations.toml": self.OBSERVED},
            routing_files={},
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL missing-routing-configuration routing.toml", result.stdout)
        self.assertTrue(result.stdout.rstrip().endswith("FAIL routing configuration has errors"))

    def test_structural_and_safety_defects_fail_deterministically(self) -> None:
        scenarios = {
            "malformed TOML": (
                {"routing.toml": self.ROUTE, ".codex/agents/worker.toml": "name = [\n"},
                "FAIL malformed-toml .codex/agents/worker.toml",
            ),
            "malformed frontmatter": (
                {
                    "routing.toml": self.ROUTE,
                    ".codex/agents/worker.toml": self.PROFILE,
                    "skills/local/SKILL.md": "---\nname: {\n---\n",
                },
                "FAIL malformed-frontmatter skills/local/SKILL.md",
            ),
            "duplicate agent": (
                {
                    "routing.toml": self.ROUTE,
                    ".codex/agents/worker.toml": self.PROFILE,
                    ".codex/agents/other.toml": self.PROFILE,
                },
                "FAIL duplicate-agent worker",
            ),
            "missing profile": (
                {"routing.toml": self.ROUTE.replace('profile = "worker"', 'profile = "absent"'), ".codex/agents/worker.toml": self.PROFILE},
                "FAIL missing-profile absent",
            ),
            "missing skill": (
                {"routing.toml": self.ROUTE.replace('["implement"]', '["unknown-skill"]'), ".codex/agents/worker.toml": self.PROFILE},
                "FAIL missing-skill unknown-skill",
            ),
            "missing tool": (
                {"routing.toml": self.ROUTE.replace("tools = []", 'tools = ["unknown-tool"]'), ".codex/agents/worker.toml": self.PROFILE},
                "FAIL missing-tool unknown-tool",
            ),
            "unavailable model": (
                {"routing.toml": self.ROUTE, ".codex/agents/worker.toml": self.PROFILE.replace("gpt-5.6-terra", "gpt-5.6-sol")},
                "FAIL unavailable-model gpt-5.6-sol",
            ),
            "sandbox contradiction": (
                {"routing.toml": self.ROUTE, ".codex/agents/worker.toml": self.PROFILE.replace('sandbox_mode = "workspace-write"', 'sandbox_mode = "read-only"')},
                "FAIL sandbox-contradiction worker",
            ),
            "unapproved file": (
                {"routing.toml": self.ROUTE, ".codex/agents/worker.toml": self.PROFILE, "README.md": "changed\n"},
                "FAIL unapproved-file README.md",
            ),
        }
        repository = {"CONTEXT.md": "# Repository context\n", ".routing-observations.toml": self.OBSERVED}
        for name, (routing, expected) in scenarios.items():
            with self.subTest(name=name):
                result = self.run_validator(repository, routing)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertTrue(result.stdout.rstrip().endswith("FAIL routing configuration has errors"))

    def test_noncritical_uncertainty_warns_without_failing(self) -> None:
        profile = self.PROFILE.replace("gpt-5.6-terra", "gpt-5.6-luna").replace(
            'developer_instructions = "Implement approved repository changes."',
            'developer_instructions = "Canonical build instructions shared by all workers."',
        )
        routing = self.ROUTE.replace(
            'responsibility = "Implement approved repository changes."',
            'responsibility = "Handle any task across the repository."',
        )
        result = self.run_validator(
            repository_files={
                "HANDBOOK.md": "Canonical build instructions shared by all workers.\n",
                ".routing-observations.toml": self.OBSERVED,
            },
            routing_files={"routing.toml": routing, ".codex/agents/worker.toml": profile},
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN unverifiable-model gpt-5.6-luna", result.stdout)
        self.assertIn("WARN missing-context-pointer CONTEXT.md", result.stdout)
        self.assertIn("WARN broad-profile worker", result.stdout)
        self.assertIn("WARN duplicated-instructions worker", result.stdout)
        self.assertTrue(result.stdout.rstrip().endswith("WARN routing configuration requires attention"))

    def test_untriggered_profile_warns_without_failing(self) -> None:
        result = self.run_validator(
            repository_files={
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
            },
            routing_files={
                "routing.toml": self.ROUTE,
                ".codex/agents/worker.toml": self.PROFILE,
                ".codex/agents/unused.toml": self.PROFILE.replace('name = "worker"', 'name = "unused"'),
            },
            approved_files=(".codex/agents/worker.toml", ".codex/agents/unused.toml"),
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN profile-without-trigger unused", result.stdout)
        self.assertTrue(result.stdout.rstrip().endswith("WARN routing configuration requires attention"))


if __name__ == "__main__":
    unittest.main()
