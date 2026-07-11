# Issue #8: ytm-tui global-first routing experiment

## Result

The requested target remained unchanged. This is a **partial validation**, not acceptance of all of issue #8: its live checkout is a clean non-Apple Rust repository, but it is **not** a first-time-bootstrap candidate because it already contains `.codex/agents/` and a repository-specific team. The actual bootstrap therefore stopped with `FAIL existing-routing-contract`, as required, rather than overwriting or inferring a refresh.

To test the issue's clean-bootstrap case without altering the target, the runner copied only `AGENTS.md`, `README.md`, and `Cargo.toml` into a temporary evidence-only projection. That projection rendered the global-first approval surface and proposed no local profiles. It returned `WARN missing-repository-context CONTEXT.md`; that warning is intentional and requires approval before any future target patch.

`result.json` is the captured run. Re-run it from this repository:

```sh
python3 scripts/run-issue-8-experiment.py \
  --repository /Users/guhan/Documents/ytm-tui \
  --output experiments/issue-8/result.json
```

The runner snapshots the target Git `HEAD` and full porcelain status before and after its reads. A mismatch fails the run. It rejects an output path inside the target, then writes only the supplied external artifact path and its temporary projection.

## Evidence and boundary

- Target: `/Users/guhan/Documents/ytm-tui` at `b3dc3bab6e5fcf20f4045e2dffe3deef7e5a3bfa`, clean before and after.
- Observed target context: `AGENTS.md`, `README.md`, `Cargo.toml`, `docs/agents/domain.md`, `docs/agents/roadmap.md`, `.agents/skills/ytm-tui-project-team/SKILL.md`, and `.codex/agents/`.
- The target identifies a Rust terminal YouTube/YouTube Music audio player; its normal checks are `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, and `cargo test`.
- The experiment references those boundary documents. It does not copy target instructions, commands, or local-profile prompts into new agents.

## Approval surface

The projected surface has seven decision-first lines: status, precheck, evidence, routing, attention, files, and checklist. It exposes every profile's exact model, reasoning, and access assignment, then explicitly says `no Repository-Specific Profiles proposed`.

The real target run has the same seven-line shape and a `FILES: none` safety result. That is the correct outcome for an already-routed checkout; a separate refresh workflow and repository approval would be required for any local change.

## Routing simulations

| Scenario | Route | Exact assignment | Escalation |
| --- | --- | --- | --- |
| bounded source and test inventory | `global_scout` | `gpt-5.6-luna`, medium, read-only | none |
| one confirmed README wording correction | `spark_editor_gpt56` | `gpt-5.6-luna`, medium, workspace-write | none |
| approved Rust behavior change with focused test | `global_worker` | `gpt-5.6-terra`, medium, workspace-write | none |
| concrete Luna inventory failure | `global_worker` | `gpt-5.6-terra`, medium, workspace-write | Luna to Terra once |
| repeated Terra failure with conflicting runtime evidence | `global_debugger` | `gpt-5.6-sol`, high, workspace-write | one Sol/high route |

The orchestrator owns all selections. The simulations use the global migration manifest; they do not authorize a worker to self-promote.

## Metrics

| Metric | Result |
| --- | ---: |
| Global profiles considered | 6 |
| Local profiles proposed | 0 |
| Routing corrections | 0 |
| Automatic Sol/high routes | 1 |
| Approval-surface lines | 7 |
| Warnings/safety stops | 2 |

The two recorded attention items are the actual target's existing routing contract and the projection's missing `CONTEXT.md`. No local profile is proposed, which is a valid result under the admission policy. Rework risk is medium: ytm-tui is a useful non-Apple evidence source, but its existing rich team means the clean projection is a controlled counterfactual, not proof that the live target should be bootstrapped. A genuinely clean non-Apple repository, or a separately approved removal of the target's existing contract, is still needed to close issue #8.
