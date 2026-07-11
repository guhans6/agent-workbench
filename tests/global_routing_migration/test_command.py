from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "validate-global-routing.py"
RENDER_COMMAND = ROOT / "scripts" / "render-global-routing-migration.py"
APPLY_COMMAND = ROOT / "scripts" / "apply-global-routing-migration.py"
APPLY_SPEC = importlib.util.spec_from_file_location("apply_global_routing_migration", APPLY_COMMAND)
assert APPLY_SPEC and APPLY_SPEC.loader
APPLY = importlib.util.module_from_spec(APPLY_SPEC)
sys.modules[APPLY_SPEC.name] = APPLY
APPLY_SPEC.loader.exec_module(APPLY)


class GlobalRoutingMigrationCommandTests(unittest.TestCase):
    def test_apply_helpers_preserve_unmanaged_guidance_and_patch_only_scalars(self) -> None:
        replaced = APPLY.replace_block(
            "Manual guidance.\n<!-- routing:start -->old<!-- routing:end -->\nKeep this.\n",
            "# Proposal\n<!-- routing:start -->new<!-- routing:end -->\n",
        )
        self.assertEqual(replaced, "Manual guidance.\n<!-- routing:start -->new<!-- routing:end -->\nKeep this.\n")
        patched = APPLY.patch_scalar('description = "keep"\nmodel = "old"\ndeveloper_instructions = "keep"\n', "model", "new")
        self.assertEqual(patched, 'description = "keep"\nmodel = "new"\ndeveloper_instructions = "keep"\n')
        with self.assertRaises(ValueError):
            APPLY.replace_block("<!-- routing:start -->one<!-- routing:end -->", "<!-- routing:start -->a<!-- routing:end --><!-- routing:start -->b<!-- routing:end -->")
    def write_tree(self, root: Path, files: dict[str, str]) -> None:
        for relative_path, contents in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(contents).lstrip())

    SHARED_POLICY = '''
        [selection]
        objective = "best-value"
        factors = ["expected-quality", "cost", "latency", "access", "coordination-overhead"]
        user_override = true
        exact_model_assignment = true
        silent_model_fallback = false
        [escalation]
        owner = "orchestrator"
        workers_may_self_promote = false
        luna_to_terra_trigger = "concrete-failure"
        terra_to_sol_triggers = ["conflicting-evidence", "architectural-ambiguity", "repeated-failure", "elevated-risk"]
        automatic_sol_high_budget = 1
    '''

    def run_validator(
        self, source_files: dict[str, str], observed: str, shared_policy: str | None = None, live_agents: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            fixture = Path(temporary_directory)
            source = fixture / "source"
            self.write_tree(source, source_files)
            observed_path = fixture / "observed.toml"
            observed_path.write_text(textwrap.dedent(observed).lstrip())
            shared_policy_path = fixture / "shared-policy.toml"
            shared_policy_path.write_text(textwrap.dedent(shared_policy or self.SHARED_POLICY).lstrip())
            live_agents_path = fixture / "live-agents"
            if live_agents is not None:
                self.write_tree(live_agents_path, live_agents)
            command = [
                    sys.executable,
                    str(COMMAND),
                    "--source",
                    str(source),
                    "--observed",
                    str(observed_path),
                    "--shared-policy",
                    str(shared_policy_path),
                ]
            if live_agents is not None:
                command.extend(("--live-agents", str(live_agents_path)))
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_validates_exact_assignments_and_shared_policy_projection(self) -> None:
        result = self.run_validator(
            {
                "AGENTS.md": "<!-- routing:start -->\nGeneral routing first.\nSelect the best-value profile by expected quality, cost, latency, access, and coordination overhead.\nExplicit user instructions override routing.\nEvery assignment is exact; an unavailable model stops routing instead of falling back.\nThe orchestrator owns classification and workers do not self-promote.\nA concrete Luna failure escalates once to Terra.\nTerra escalates to Sol only for conflicting evidence, architectural ambiguity, repeated failure, or elevated risk.\nAt most one Sol/high subagent runs automatically per user task.\nMatt workflow routing.\nUse `grill-with-docs` for an idea needing clarification and `wayfinder` when a huge effort's route remains unclear.\nApple exceptions second.\n<!-- routing:end -->\n",
                "migration.toml": '''
                    [[existing_agents]]
                    name = "explorer"
                    disposition = "replace"
                    current_model = "gpt-5.4-mini"
                    current_reasoning = "low"
                    proposed_model = "gpt-5.6-luna"
                    proposed_reasoning = "medium"
                    replacement = "global_scout"
                    install_before_remove = true

                    [[proposed_profiles]]
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    reasoning = "medium"
                    access = "read-only"
                    skills = ["implement"]
                ''',
                "agents/global_scout.toml": '''
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    model_reasoning_effort = "medium"
                    sandbox_mode = "read-only"
                ''',
            },
            '''
                models = ["gpt-5.6-luna"]
                skills = ["implement"]
            ''',
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "PASS global routing migration is structurally valid\n")

    def test_rejects_silent_fallback_and_uninstalled_replacements(self) -> None:
        result = self.run_validator(
            {
                "AGENTS.md": "<!-- routing:start -->\nGeneral routing first.\nMatt workflow routing.\nApple exceptions second.\nThe orchestrator owns classification and workers do not self-promote.\nA concrete Luna failure escalates once to Terra.\nTerra escalates to Sol only for conflicting evidence, architectural ambiguity, repeated failure, or elevated risk.\nAt most one Sol/high subagent runs automatically per user task.\n<!-- routing:end -->\n",
                "migration.toml": '''
                    [[existing_agents]]
                    name = "explorer"
                    disposition = "replace"
                    current_model = "gpt-5.4-mini"
                    current_reasoning = "low"
                    proposed_model = "gpt-5.6-luna"
                    proposed_reasoning = "medium"
                    replacement = "global_scout"
                    install_before_remove = false

                    [[proposed_profiles]]
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    reasoning = "medium"
                    access = "read-only"
                    skills = ["missing-skill"]
                ''',
            },
            'models = ["gpt-5.6-luna"]\nskills = ["implement"]\n',
            self.SHARED_POLICY.replace("silent_model_fallback = false", "silent_model_fallback = true"),
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL silent-model-fallback-enabled shared-policy.toml", result.stdout)
        self.assertIn("FAIL replacement-not-installable explorer", result.stdout)
        self.assertIn("FAIL missing-skill missing-skill", result.stdout)

    def test_rejects_duplicate_profiles_and_policy_projection_drift(self) -> None:
        result = self.run_validator(
            {
                "AGENTS.md": "<!-- routing:start -->\nGeneral routing first.\nMatt workflow routing.\nApple exceptions second.\n<!-- routing:end -->\n",
                "migration.toml": '''
                    [[proposed_profiles]]
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    reasoning = "medium"
                    access = "read-only"
                    skills = ["implement"]
                ''',
                "agents/one.toml": 'name = "global_scout"\nmodel = "gpt-5.6-luna"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\n',
                "agents/two.toml": 'name = "global_scout"\nmodel = "gpt-5.6-luna"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\n',
            },
            'models = ["gpt-5.6-luna"]\nskills = ["implement"]\n',
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL duplicate-proposed-profile global_scout", result.stdout)
        self.assertIn("FAIL invalid-routing-projection-order AGENTS.md", result.stdout)

    def test_rejects_duplicate_manifest_profiles_unmanifested_tomls_and_bad_blocks(self) -> None:
        result = self.run_validator(
            {
                "AGENTS.md": "General routing first.\n<!-- routing:end -->\n<!-- routing:start -->\nGeneral routing first.\nMatt workflow routing.\nApple exceptions second.\n<!-- routing:end -->\n",
                "migration.toml": '''
                    [[proposed_profiles]]
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    reasoning = "medium"
                    access = "read-only"
                    skills = []

                    [[proposed_profiles]]
                    name = "global_scout"
                    model = "gpt-5.6-luna"
                    reasoning = "medium"
                    access = "read-only"
                    skills = []
                ''',
                "agents/global_scout.toml": 'name = "global_scout"\nmodel = "gpt-5.6-luna"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\n',
                "agents/stray.toml": 'name = "stray"\nmodel = "gpt-5.6-luna"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\n',
            },
            'models = ["gpt-5.6-luna"]\nskills = []\n',
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL duplicate-manifest-profile global_scout", result.stdout)
        self.assertIn("FAIL unmanifested-profile-artifact stray", result.stdout)
        self.assertIn("FAIL invalid-managed-routing-block AGENTS.md", result.stdout)

    def test_rejects_live_inventory_mismatch_and_non_patch_same_name_update(self) -> None:
        result = self.run_validator(
            {
                "AGENTS.md": "<!-- routing:start -->\nGeneral routing first.\nEvery assignment is exact; an unavailable model stops routing instead of falling back.\nThe orchestrator owns classification and workers do not self-promote.\nA concrete Luna failure escalates once to Terra.\nTerra escalates to Sol only for conflicting evidence, architectural ambiguity, repeated failure, or elevated risk.\nAt most one Sol/high subagent runs automatically per user task.\nMatt workflow routing.\nApple exceptions second.\n<!-- routing:end -->\n",
                "migration.toml": '''
                    [[existing_agents]]
                    name = "apple_docs_researcher"
                    disposition = "modify"
                    current_model = "wrong"
                    current_reasoning = "medium"
                    current_access = "read-only"
                    proposed_model = "gpt-5.6-terra"
                    proposed_reasoning = "high"
                    replacement = "apple_docs_researcher"
                    install_before_remove = true

                    [[proposed_profiles]]
                    name = "apple_docs_researcher"
                    model = "gpt-5.6-terra"
                    reasoning = "high"
                    access = "read-only"
                    skills = []
                ''',
                "agents/apple_docs_researcher.toml": 'name = "apple_docs_researcher"\nmodel = "gpt-5.6-terra"\nmodel_reasoning_effort = "high"\nsandbox_mode = "read-only"\n',
            },
            'models = ["gpt-5.6-terra"]\nskills = []\n',
            live_agents={"apple_docs_researcher.toml": 'name = "apple_docs_researcher"\nmodel = "gpt-5.4-mini"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\n'},
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL non-patch-same-name-update apple_docs_researcher", result.stdout)
        self.assertIn("FAIL live-inventory-mismatch apple_docs_researcher", result.stdout)

    def test_committed_proposal_validates_every_profile_and_exact_delta(self) -> None:
        source = ROOT / "platforms" / "codex" / "migrations" / "gpt-5.6"
        result = subprocess.run(
            [
                sys.executable,
                str(COMMAND),
                "--source",
                str(source),
                "--observed",
                str(source / "observed.toml"),
                "--shared-policy",
                str(ROOT / "shared" / "routing" / "routing-policy.toml"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        rendered = subprocess.run(
            [sys.executable, str(RENDER_COMMAND), "--source", str(source)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "PASS global routing migration is structurally valid\n")
        self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
        self.assertEqual(rendered.stdout.count("AGENT DELTA: "), 9)
        self.assertEqual(rendered.stdout.count("ROUTING: "), 13)
        self.assertIn(
            "AGENT DELTA: spark_editor | merge | gpt-5.3-codex-spark / low -> gpt-5.6-luna / medium | spark_editor_gpt56",
            rendered.stdout,
        )
        self.assertIn("ROUTING: deep_debugger | difficult Apple investigation after triage | gpt-5.6-sol | high", rendered.stdout)

    def test_renders_exact_current_and_proposed_assignment_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory)
            self.write_tree(
                source,
                {
                    "migration.toml": '''
                        [[existing_agents]]
                        name = "explorer"
                        disposition = "replace"
                        current_model = "gpt-5.4-mini"
                        current_reasoning = "low"
                        proposed_model = "gpt-5.6-luna"
                        proposed_reasoning = "medium"
                        replacement = "global_scout"
                        install_before_remove = true
                    ''',
                },
            )
            result = subprocess.run(
                [sys.executable, str(RENDER_COMMAND), "--source", str(source)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            "STATUS: PROPOSED\n"
            "RECOMMENDATION: run the separate Sol/high read-only review before applying any global runtime change\n"
            "AGENT DELTA: explorer | replace | gpt-5.4-mini / low -> gpt-5.6-luna / medium | global_scout | install then validate before removal\n"
            "ATTENTION: install new global profiles before retiring legacy generic profiles; patch same-name profiles minimally; no silent fallback\n"
            "FILES: AGENTS.md; agents/*.toml\n"
            "CHECKLIST: verify live inventory; run Sol review; dry-run; back up; install or patch; validate; then separately consider removal\n"
            "GLOBAL RUNTIME: unchanged\n",
        )


if __name__ == "__main__":
    unittest.main()
