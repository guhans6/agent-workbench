from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "run-whisperv-routing-experiment.py"


class WhisperVRoutingExperimentCommandTests(unittest.TestCase):
    def test_reports_global_first_bootstrap_and_bounded_apple_simulations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "WhisperV"
            repository.mkdir()
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            (repository / "AGENTS.md").write_text("# Agent Rules\n")
            (repository / "CONTEXT.md").write_text("# WhisperV\n")
            (repository / "WhisperV.xcodeproj").mkdir()
            (repository / "WhisperV.xcodeproj" / "project.pbxproj").write_text(
                textwrap.dedent(
                    """\
                    // !$*UTF8*$!
                    /* Begin PBXNativeTarget section */
                    """
                )
            )
            (repository / "WhisperV").mkdir()
            (repository / "WhisperV" / "WhisperVApp.swift").write_text("import SwiftUI\n")

            result = subprocess.run(
                [sys.executable, str(COMMAND), "--repository", str(repository), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["bootstrap"]["status"], "PASS")
        self.assertFalse(report["target_mutated"])
        self.assertEqual(report["approval_metrics"]["surface_lines"], 7)
        self.assertEqual(report["approval_metrics"]["automatic_sol_high_violations"], 0)
        expected_assignments = {
            "swift_architecture_mapping": ("swift_explorer", "gpt-5.6-terra", "medium", "read-only"),
            "approved_swift_feature": ("swift_worker", "gpt-5.6-terra", "medium", "workspace-write"),
            "xcode_build_failure": ("xcode_triager", "gpt-5.6-terra", "medium", "workspace-write"),
            "apple_api_availability": ("apple_docs_researcher", "gpt-5.6-terra", "high", "read-only"),
            "swift_concurrency_review": ("swift_reviewer", "gpt-5.6-sol", "high", "read-only"),
            "proven_hard_apple_debug": ("deep_debugger", "gpt-5.6-sol", "high", "workspace-write"),
        }
        for scenario, expected in expected_assignments.items():
            simulation = report["simulations"][scenario]
            self.assertEqual(
                (simulation["profile"], simulation["model"], simulation["reasoning"], simulation["access"]),
                expected,
            )
            self.assertTrue(simulation["specialist_value_over_global"])
            self.assertTrue(simulation["material_signals"])
        self.assertEqual(report["simulations"]["sol_high_budget_stress"]["automatic_profiles"], ["swift_reviewer"])
        self.assertEqual(report["simulations"]["sol_high_budget_stress"]["suppressed_profiles"], ["deep_debugger"])
        self.assertTrue(report["specialist_assessment"]["all_retained_profiles_have_concrete_boundaries"])
        self.assertEqual(report["specialist_assessment"]["redundant_retained_profiles"], [])


if __name__ == "__main__":
    unittest.main()
