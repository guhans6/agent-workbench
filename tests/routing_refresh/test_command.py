from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "refresh-routing.py"


class RefreshCommandTests(unittest.TestCase):
    OBSERVED = (
        'models = ["gpt-5.6-terra"]\n'
        'skills = ["implement", "to-spec", "to-tickets"]\n'
        'tools = ["git"]\n'
    )
    ROUTING = (
        'context_pointers = ["CONTEXT.md"]\n\n'
        '[[routes]]\ntrigger = "planning"\nprofile = "planner"\n\n'
        '[[profiles]]\nname = "planner"\naccess_requirement = "workspace-write"\n'
        'responsibility = "Plan approved repository work."\n'
        'skills = ["to-spec", "to-tickets"]\ntools = []\n'
    )
    LEGACY_PROFILE = (
        'name = "planner"\ndescription = "Repository planning worker."\n'
        'model = "gpt-5.6-terra"\nmodel_reasoning_effort = "medium"\n'
        'sandbox_mode = "workspace-write"\n'
        'developer_instructions = "Use to-prd and to-issues for approved planning work."\n'
    )
    REFRESHED_PROFILE = LEGACY_PROFILE.replace("to-prd and to-issues", "to-spec and to-tickets")

    def run_refresh(
        self, repository_files: dict[str, str], routing_files: dict[str, str]
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            fixture = Path(temporary_directory)
            repository = fixture / "repository"
            routing = fixture / "routing"
            self.write_tree(repository, repository_files)
            self.write_tree(routing, routing_files)
            return subprocess.run(
                [
                    sys.executable,
                    str(COMMAND),
                    "--repository",
                    str(repository),
                    "--routing",
                    str(routing),
                    "--approved-file",
                    ".codex/agents/planner.toml",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    @staticmethod
    def write_tree(root: Path, files: dict[str, str]) -> None:
        for relative_path, contents in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(contents).lstrip())

    def test_capability_rename_is_a_delta_and_preserves_model_assignments(self) -> None:
        result = self.run_refresh(
            {
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
                "routing.toml": self.ROUTING,
                ".codex/agents/planner.toml": self.LEGACY_PROFILE,
                "AGENTS.md": "<!-- routing:start -->\nUse planner for planning.\n<!-- routing:end -->\n",
                "README.md": "Manual repository notes.\n",
            },
            {".codex/agents/planner.toml": self.REFRESHED_PROFILE},
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "STATUS: PASS",
                    "ROUTING DELTA: planner | planning | gpt-5.6-terra | medium | workspace-write | to-spec, to-tickets",
                    "CAPABILITY DELTA: to-prd -> to-spec; to-issues -> to-tickets (.codex/agents/planner.toml)",
                    "MODEL DELTA: No model-assignment changes proposed",
                    "FILES: .codex/agents/planner.toml",
                    "PRESERVED: Everything else preserved",
                    "CHECKLIST: review affected rows; approve minimal patches; revalidate after approved changes",
                    "",
                )
            ),
        )

    def test_model_assignment_changes_are_reported_separately(self) -> None:
        result = self.run_refresh(
            {
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
                "routing.toml": self.ROUTING,
                ".codex/agents/planner.toml": self.LEGACY_PROFILE,
                "AGENTS.md": "<!-- routing:start -->\nUse planner for planning.\n<!-- routing:end -->\n",
            },
            {".codex/agents/planner.toml": self.LEGACY_PROFILE.replace('model_reasoning_effort = "medium"', 'model_reasoning_effort = "high"')},
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "MODEL DELTA: .codex/agents/planner.toml: gpt-5.6-terra / medium -> gpt-5.6-terra / high",
            result.stdout,
        )
        self.assertIn("PRESERVED: Everything else preserved", result.stdout)

    def test_validation_failures_block_an_unapproved_refresh(self) -> None:
        result = self.run_refresh(
            {
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
                "routing.toml": self.ROUTING,
                ".codex/agents/planner.toml": self.LEGACY_PROFILE,
                "AGENTS.md": "<!-- routing:start -->\nUse planner for planning.\n<!-- routing:end -->\n",
            },
            {"routing.toml": self.ROUTING.replace('"to-spec", "to-tickets"', '"missing-skill"')},
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("STATUS: FAIL", result.stdout)
        self.assertIn("FAIL missing-skill missing-skill", result.stdout)

    def test_unmanaged_file_and_manual_agents_edits_are_rejected(self) -> None:
        result = self.run_refresh(
            {
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
                "routing.toml": self.ROUTING,
                ".codex/agents/planner.toml": self.LEGACY_PROFILE,
                "AGENTS.md": "Before\n<!-- routing:start -->\nUse planner.\n<!-- routing:end -->\nAfter\n",
            },
            {
                "README.md": "Unrelated change.\n",
                "AGENTS.md": "Changed manual text\n<!-- routing:start -->\nUse planner.\n<!-- routing:end -->\nAfter\n",
            },
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL unmanaged-refresh-file README.md", result.stdout)
        self.assertIn("FAIL unmanaged-agents-edit AGENTS.md", result.stdout)

    def test_changed_routing_row_is_rendered(self) -> None:
        result = self.run_refresh(
            {
                "CONTEXT.md": "# Repository context\n",
                ".routing-observations.toml": self.OBSERVED,
                "routing.toml": self.ROUTING,
                ".codex/agents/planner.toml": self.LEGACY_PROFILE,
                "AGENTS.md": "<!-- routing:start -->\nUse planner.\n<!-- routing:end -->\n",
            },
            {"routing.toml": self.ROUTING.replace('trigger = "planning"', 'trigger = "architecture planning"')},
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "ROUTING DELTA: planner | architecture planning | gpt-5.6-terra | medium | workspace-write | to-spec, to-tickets",
            result.stdout,
        )

if __name__ == "__main__":
    unittest.main()
