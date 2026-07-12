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
    GLOBAL_PROFILE = "terra|normal implementation|gpt-5.6-terra|medium|workspace-write"

    def run_bootstrap(
        self, files: dict[str, str], global_profiles: tuple[str, ...] = (GLOBAL_PROFILE,)
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "repository"
            for relative_path, contents in files.items():
                path = repository / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(textwrap.dedent(contents).lstrip())
            command = [sys.executable, str(COMMAND), "--repository", str(repository)]
            for profile in global_profiles:
                command.extend(("--global-profile", profile))
            return subprocess.run(
                command,
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
                    "ROUTING: terra | normal implementation | gpt-5.6-terra | medium | workspace-write; no Repository-Specific Profiles proposed",
                    "ATTENTION: add a concise Managed Routing Block to AGENTS.md",
                    "FILES: AGENTS.md",
                    "CHECKLIST: review context pointer; review global profile assignments; approve minimal Managed Routing Block; validate before write",
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
                    "ROUTING: blocked; use a dedicated refresh workflow explicitly",
                    "ATTENTION: bootstrap never infers refresh mode",
                    "FILES: none",
                    "CHECKLIST: invoke the refresh workflow and preserve the existing Managed Routing Block",
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
        self.assertIn("PRECHECK: PASS repository-context-observed", result.stdout)
        self.assertIn(
            "ROUTING: terra | normal implementation | gpt-5.6-terra | medium | workspace-write; no Repository-Specific Profiles proposed",
            result.stdout,
        )
        self.assertIn("FILES: AGENTS.md", result.stdout)

    def test_incomplete_repository_context_warns(self) -> None:
        result = self.run_bootstrap({"AGENTS.md": "# Repository instructions\n"})

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("PRECHECK: WARN missing-repository-context CONTEXT.md", result.stdout)

    def test_existing_agent_profile_requires_explicit_refresh(self) -> None:
        result = self.run_bootstrap(
            {
                "AGENTS.md": "# Repository instructions\n",
                "CONTEXT.md": "# Repository context\n",
                ".codex/agents/local.toml": 'name = "local"\n',
            }
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("PRECHECK: FAIL existing-routing-contract", result.stdout)

    def test_ignores_python_cache_files_when_collecting_evidence(self) -> None:
        result = self.run_bootstrap(
            {
                "package.json": '{"name": "sample"}\n',
                "scripts/__pycache__/generated.pyc": "cache\n",
                "scripts/verify.py": "print('verify')\n",
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("EVIDENCE: package.json, scripts/verify.py", result.stdout)
        self.assertNotIn("__pycache__", result.stdout)


if __name__ == "__main__":
    unittest.main()
