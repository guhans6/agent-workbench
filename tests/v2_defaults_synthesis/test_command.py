from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "synthesize-v2-defaults.py"


class V2DefaultsSynthesisCommandTests(unittest.TestCase):
    def test_aggregates_nine_routes_without_hiding_the_partial_non_apple_result(self) -> None:
        result = subprocess.run(
            [sys.executable, str(COMMAND), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["metrics"]["representative_routes"], 9)
        self.assertEqual(report["metrics"]["recorded_user_corrections"], 0)
        self.assertEqual(report["metrics"]["automatic_sol_high_budget"], 1)
        self.assertEqual(len(report["routes"]), 9)
        self.assertEqual(report["policy_judgment"]["recommendation"], "retain-v2-defaults-with-evidence-qualifier")
        self.assertIn("controlled counterfactual", report["limitations"])
        self.assertEqual(report["policy_changes"], {"retain": 7, "revise": 0, "cut": 0})
        self.assertEqual(report["economic_comparison"]["status"], "not-measured")
        self.assertIn("no cheap-route rework", report["economic_comparison"]["reason"])
        self.assertEqual(len(report["apple_specialist_boundaries"]), 6)
        self.assertTrue(all(boundary["observed_distinct"] for boundary in report["apple_specialist_boundaries"]))
        self.assertTrue(any(route["correction"] == "none recorded" for route in report["routes"]))


if __name__ == "__main__":
    unittest.main()
