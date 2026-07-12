from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "audit-routing-skill-install.py"


class RoutingSkillInstallAuditTests(unittest.TestCase):
    def run_audit(self, mutate=None) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source"
            installed = root / "installed"
            for name in ("project-agent-architect", "refresh-project-agent-routing"):
                shutil.copytree(ROOT / "shared" / "skills" / name, source / name)
                shutil.copytree(ROOT / "shared" / "skills" / name, installed / name)
            if mutate is not None:
                mutate(source, installed)
            return subprocess.run(
                [
                    sys.executable,
                    str(COMMAND),
                    "--source-root",
                    str(source),
                    "--installed-root",
                    str(installed),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_exact_install_passes(self) -> None:
        result = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "PASS routing skill installation matches source\n")

    def test_extra_missing_and_changed_files_fail(self) -> None:
        def mutate(source: Path, installed: Path) -> None:
            (installed / "project-agent-architect" / ".DS_Store").write_text("sediment")
            (installed / "project-agent-architect" / "SKILL.md").write_text("changed")
            (installed / "refresh-project-agent-routing" / "SKILL.md").unlink()

        result = self.run_audit(mutate)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL changed-file project-agent-architect/SKILL.md", result.stdout)
        self.assertIn("FAIL extra-file project-agent-architect/.DS_Store", result.stdout)
        self.assertIn("FAIL missing-file refresh-project-agent-routing/SKILL.md", result.stdout)

    def test_missing_helpers_and_broken_or_orphaned_references_fail(self) -> None:
        def mutate(source: Path, installed: Path) -> None:
            for root in (source, installed):
                (root / "project-agent-architect" / "scripts" / "bootstrap-routing.py").unlink()
                (root / "project-agent-architect" / "references" / "orphan.md").write_text("# Orphan\n")
                skill = root / "refresh-project-agent-routing" / "SKILL.md"
                skill.write_text(skill.read_text() + "\n[missing](references/missing.md)\n")

        result = self.run_audit(mutate)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(
            "FAIL missing-source-file project-agent-architect/scripts/bootstrap-routing.py",
            result.stdout,
        )
        self.assertIn(
            "FAIL orphan-reference project-agent-architect/references/orphan.md",
            result.stdout,
        )
        self.assertIn(
            "FAIL missing-reference refresh-project-agent-routing/SKILL.md -> references/missing.md",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
