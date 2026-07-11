from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "bootstrap-routing.py"


class BootstrapCommandTests(unittest.TestCase):
    def run_bootstrap(self, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repository"
            for relative_path, contents in files.items():
                path = repository / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(textwrap.dedent(contents).lstrip())
            return subprocess.run(
                [sys.executable, str(COMMAND), "--repository", str(repository)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_sparse_repository_proposes_global_first_no_local_profiles(self) -> None:
        result = self.run_bootstrap(
            {
                "package.json": '{"name": "sample", "scripts": {"test": "node test.js"}}\n',
                "docs/plan.md": "# Plan\n",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "STATUS: WARN",
                    "PRECHECK: WARN missing-repository-context AGENTS.md",
                    "EVIDENCE: docs/plan.md, package.json",
                    "ROUTING: global execution profiles first; no local profiles proposed",
                    "ATTENTION: add a concise managed routing/context block to AGENTS.md",
                    "FILES: AGENTS.md",
                    "CHECKLIST: review context pointer; approve minimal managed block; validate before write",
                    "",
                )
            ),
        )

    def test_repository_without_observable_evidence_blocks_bootstrap(self) -> None:
        result = self.run_bootstrap({})

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "STATUS: FAIL",
                    "PRECHECK: FAIL insufficient-repository-evidence",
                    "EVIDENCE: none",
                    "ROUTING: blocked",
                    "ATTENTION: provide repository instructions, plans, manifests, scripts, tests, or confirmed decisions",
                    "FILES: none",
                    "CHECKLIST: resolve evidence gap before proposing a write-capable route",
                    "",
                )
            ),
        )

    def test_existing_managed_routing_block_requires_explicit_refresh(self) -> None:
        result = self.run_bootstrap(
            {
                "AGENTS.md": "<!-- routing:start -->\nExisting contract\n<!-- routing:end -->\n",
                "CONTEXT.md": "# Repository context\n",
            }
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            "\n".join(
                (
                    "STATUS: FAIL",
                    "PRECHECK: FAIL existing-routing-contract",
                    "EVIDENCE: AGENTS.md, CONTEXT.md",
                    "ROUTING: blocked; use refresh-project-agent-routing explicitly",
                    "ATTENTION: bootstrap never infers refresh mode",
                    "FILES: none",
                    "CHECKLIST: invoke the refresh skill and preserve the existing managed block",
                    "",
                )
            ),
        )

    def test_context_ready_repository_passes_without_generating_local_profiles(self) -> None:
        result = self.run_bootstrap(
            {
                "AGENTS.md": "# Repository instructions\n",
                "CONTEXT.md": "# Repository context\n",
                "tests/example_test.py": "def test_example(): pass\n",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("STATUS: PASS", result.stdout)
        self.assertIn("PRECHECK: PASS repository-context-ready", result.stdout)
        self.assertIn("ROUTING: global execution profiles first; no local profiles proposed", result.stdout)
        self.assertIn("FILES: AGENTS.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
