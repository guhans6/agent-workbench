#!/usr/bin/env python3
"""Render the evidence-bound v2 defaults synthesis for issue #11."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ISSUE_8 = ROOT / "experiments" / "issue-8" / "result.json"
ISSUE_9 = ROOT / "experiments" / "whisperv-apple-routing" / "README.md"
ISSUE_10 = ROOT / "experiments" / "companion-rich-team-refresh.md"
POLICY = ROOT / "shared" / "routing" / "routing-policy.toml"


def assignment(name: str, model: str, reasoning: str, access: str) -> dict[str, str]:
    return {"profile": name, "model": model, "reasoning": reasoning, "access": access}


def load() -> dict[str, object]:
    issue_8 = json.loads(ISSUE_8.read_text())
    policy = tomllib.loads(POLICY.read_text())
    issue_9 = ISSUE_9.read_text()
    issue_10 = ISSUE_10.read_text()
    if "controlled counterfactual" not in issue_8["rework_risk"]:
        raise RuntimeError("issue #8 partial-result qualifier is missing")
    if "candidate stress case" not in issue_9 or "suppresses" not in issue_9:
        raise RuntimeError("issue #9 does not record the one-Sol/high budget")
    if "8 profiles" not in issue_10 or "6 admitted local profiles" not in issue_10:
        raise RuntimeError("issue #10 profile-count evidence is missing")
    apple_boundaries = (
        ("swift_explorer", "Apple source, state-ownership, and test mapping"),
        ("swift_worker", "Apple implementation with state and concurrency constraints"),
        ("xcode_triager", "build, scheme, simulator, or log triage"),
        ("apple_docs_researcher", "official Apple API semantics and availability"),
        ("swift_reviewer", "Apple regression, state, concurrency, and test review"),
        ("deep_debugger", "difficult Apple investigation after focused triage"),
    )
    normalized_issue_9 = issue_9.replace("\n", " ")
    if any(name not in issue_9 for name, _ in apple_boundaries) or "None of the retained Apple profiles was redundant" not in normalized_issue_9:
        raise RuntimeError("issue #9 Apple-specialist evidence is incomplete")
    if policy["escalation"]["automatic_sol_high_budget"] != 1:
        raise RuntimeError("central policy no longer has the observed Sol/high budget")

    routes = [
        {"repository": "ytm-tui", "scenario": item["scenario"], **assignment(item["profile"], item["model"], item["reasoning"], item["access"]), "escalation": item["escalation"], "correction": "none recorded"}
        for item in issue_8["simulations"]
    ]
    routes.extend(
        (
            {"repository": "WhisperV", "scenario": "Swift architecture mapping", **assignment("swift_explorer", "gpt-5.6-terra", "medium", "read-only"), "escalation": "none", "correction": "none recorded"},
            {"repository": "WhisperV", "scenario": "Xcode build, scheme, simulator, or log failure", **assignment("xcode_triager", "gpt-5.6-terra", "medium", "workspace-write"), "escalation": "triage before deep debugging", "correction": "none recorded"},
            {"repository": "WhisperV", "scenario": "Sol/high budget stress", **assignment("swift_reviewer", "gpt-5.6-sol", "high", "read-only"), "escalation": "deep_debugger suppressed after one automatic Sol/high route", "correction": "none recorded"},
            {"repository": "Companion", "scenario": "dirty rich-team delta refresh", **assignment("repository-context plus retained local lanes", "n/a", "n/a", "read-only experiment"), "escalation": "separate role-reduction and model-migration decisions", "correction": "none recorded"},
        )
    )
    if len(routes) != 9:
        raise RuntimeError("the synthesis must compare exactly nine representative routes")
    return {
        "metrics": {
            "representative_routes": len(routes),
            "recorded_user_corrections": 0,
            "automatic_sol_high_budget": policy["escalation"]["automatic_sol_high_budget"],
            "approval_length": {"ytm_tui": 7, "whisperv": 7, "companion_delta": 7, "companion_full_roster": 10},
            "profile_counts": {"ytm_tui_local_proposed": 0, "whisperv_local_proposed": 0, "companion_current": 8, "companion_admitted": 6},
        },
        "routes": routes,
        "apple_specialist_boundaries": [
            {"profile": name, "boundary": boundary, "observed_distinct": True}
            for name, boundary in apple_boundaries
        ],
        "economic_comparison": {
            "status": "not-measured",
            "reason": "The experiments record no cheap-route rework or user correction, while cost and latency telemetry are deliberately deferred; a numeric savings comparison is therefore not available.",
        },
        "limitations": "Issue #8 remains a controlled counterfactual: its live target already had a routing contract, so the clean non-Apple bootstrap result is partial evidence rather than a completed live bootstrap.",
        "policy_changes": {"retain": 7, "revise": 0, "cut": 0},
        "policy_judgment": {
            "recommendation": "retain-v2-defaults-with-evidence-qualifier",
            "rationale": "The synthesis preserves the accepted hard-failure guard and finds no experiment result that requires a policy change. It does not independently revalidate every hard-failure category; #8 remains partial non-Apple evidence.",
        },
    }


def markdown(report: dict[str, object]) -> str:
    metrics = report["metrics"]
    rows = [
        "# Issue #11: v2 defaults synthesis",
        "",
        "## Recommendation",
        "",
        "Retain the accepted v2 defaults with an evidence qualifier. This is an advisory judgment for the orchestrator; it does not close spec #3.",
        "",
        "## Nine representative routes",
        "",
        "| Repository | Scenario | Route | Assignment | Escalation | Correction |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for route in report["routes"]:
        rows.append(f"| {route['repository']} | {route['scenario']} | {route['profile']} | {route['model']} / {route['reasoning']} / {route['access']} | {route['escalation']} | {route['correction']} |")
    rows.extend(
        (
            "",
            "## Cross-repository comparison",
            "",
            f"- Recorded corrections: {metrics['recorded_user_corrections']} across {metrics['representative_routes']} selected evidence rows. This meets the numeric threshold, but does not convert #8's projection into a live clean-bootstrap validation.",
            "- Approval surface: ytm-tui 7 lines; WhisperV 7 lines; Companion delta 7 lines versus a 10-line full roster (30% reduction reported by #10).",
            "- Profile counts: ytm-tui proposes 0 local profiles; WhisperV proposes 0 repository-local profiles and retains Apple lanes only at their concrete boundaries; Companion has 8 current profiles with 6 admitted and 2 evidence-backed removal recommendations.",
            "- Hard-failure guard: retain unsafe write access, missed boundaries, unsupported capabilities, silent substitution, unrelated refresh changes, and overwritten manual edits as hard failures. This synthesis relies on the underlying experiment validators for those checks; it does not claim an independent revalidation.",
            "- Escalation: Luna may move once to Terra on concrete failure; Terra moves to Sol only on the approved evidence triggers; the automatic Sol/high budget stayed at 1, including the WhisperV stress case.",
            f"- Cheap-route economics: {report['economic_comparison']['status']}. {report['economic_comparison']['reason']}",
            "- Apple boundaries: the nine-row sample includes three Apple routes; the underlying experiment separately retains all six concrete lanes: " + "; ".join(f"{item['profile']} ({item['boundary']})" for item in report["apple_specialist_boundaries"]) + ".",
            "",
            "## Policy disposition",
            "",
            "- Retain (7): global-first selection, no-local-profile success, exact assignments/no silent fallback, evidence-driven escalation, one automatic Sol/high budget, concrete Apple boundaries, and delta-only refresh/preservation.",
            "- Revise (0): no policy change is justified by these artifacts. The Companion planning-alias update is a narrow capability-refresh result, not a routing-policy revision.",
            "- Cut (0): the deferred context bootstrap, manifests, telemetry, named model profiles, and large specialist catalogs remain deferred; no experiment reopens them.",
            "",
            "## Limitation and next evidence",
            "",
            report["limitations"],
            "A future clean non-Apple repository experiment should replace that partial evidence before treating the cross-repository acceptance story as fully live-validated.",
            "",
        )
    )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    arguments = parser.parse_args()
    report = load()
    print(json.dumps(report, indent=2, sort_keys=True) if arguments.format == "json" else markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
