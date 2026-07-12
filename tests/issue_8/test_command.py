from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "run-issue-8-experiment.py"


class Issue8ExperimentCommandTests(unittest.TestCase):
    def test_records_a_real_safety_stop_and_a_clean_global_first_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "ytm-tui"
            repository.mkdir()
            (repository / "AGENTS.md").write_text("# Repository instructions\n")
            (repository / "README.md").write_text("# ytm-tui\n")
            (repository / "Cargo.toml").write_text('[package]\nname = "ytm-tui"\n')
            (repository / ".codex" / "agents").mkdir(parents=True)
            (repository / ".codex" / "agents" / "local.toml").write_text('name = "local"\n')
            output = Path(temporary_directory) / "result.json"

            result = subprocess.run(
                [sys.executable, str(COMMAND), "--repository", str(repository), "--output", str(output)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            recorded = json.loads(output.read_text())
            self.assertEqual(recorded["target"]["before"], recorded["target"]["after"])
            self.assertEqual(recorded["actual_bootstrap"]["returncode"], 1)
            self.assertIn("existing-routing-contract", recorded["actual_bootstrap"]["surface"])
            self.assertEqual(recorded["projection_bootstrap"]["returncode"], 0)
            self.assertIn("no Repository-Specific Profiles proposed", recorded["projection_bootstrap"]["surface"])
            self.assertEqual(recorded["metrics"]["local_profiles_proposed"], 0)
            self.assertEqual(recorded["metrics"]["automatic_sol_high_routes"], 1)
            self.assertEqual(recorded["metrics"]["approval_surface_lines"], 7)
            self.assertEqual(recorded["metrics"]["warnings"], 2)
            self.assertIn("controlled counterfactual", recorded["rework_risk"])
            self.assertEqual(
                [simulation["profile"] for simulation in recorded["simulations"]],
                [
                    "global_scout",
                    "spark_editor_gpt56",
                    "global_worker",
                    "global_worker",
                    "global_debugger",
                ],
            )

    def test_rejects_an_output_path_inside_the_protected_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "ytm-tui"
            repository.mkdir()
            (repository / "README.md").write_text("# ytm-tui\n")
            output = repository / "result.json"

            result = subprocess.run(
                [sys.executable, str(COMMAND), "--repository", str(repository), "--output", str(output)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output must be outside the protected repository", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
