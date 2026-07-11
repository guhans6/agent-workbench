# WhisperV Apple specialist-routing experiment

Issue: [#9](https://github.com/guhans6/agent-workbench/issues/9)
Parent specification: [#3](https://github.com/guhans6/agent-workbench/issues/3)

## Scope and safety boundary

The experiment reads `/Users/guhan/Guhan/Projects/WhisperV` but writes only to
this agent-workbench checkout. The runner snapshots `git status --porcelain=v1
--untracked-files=all` before and after its bootstrap call and fails if that
state changes. It does not apply the bootstrap proposal.

## Reproduce

```sh
python3 scripts/run-whisperv-routing-experiment.py \
  --repository /Users/guhan/Guhan/Projects/WhisperV --format markdown
```

For a machine-readable report, use `--format json`. The focused command-level
test creates a temporary Git-backed Apple/Xcode-shaped fixture:

```sh
python3 -m unittest tests/whisperv_routing_experiment/test_command.py
```

## Observed result

The 2026-07-12 run completed with a PASS repository-context precheck, a
seven-line global-first approval surface, and no target mutation. The target
has `AGENTS.md`, `CONTEXT.md`, an Xcode project, Swift sources, and the
repository-local script surface needed to support a conservative evidence pass.

The bootstrap correctly proposes the five global profiles first and proposes
zero repository-specific profiles. That is the baseline, not an instruction to
apply a managed routing block to WhisperV. Each Apple simulation then compares
the selected Apple specialist's checked-in TOML description/instructions to its
appropriate global fallback. It requires concrete specialist-only terms (such
as `scheme`, `simulator`, `availability`, or `concurrency`) before recording
material value; a specialist without a comparison or such evidence is reported
as redundant.

| Simulated task | Selected lane | Why it is distinct |
| --- | --- | --- |
| Read-only inventory | `global_scout` | General bounded, mechanical check. |
| Swift architecture mapping | `swift_explorer` | Apple source, state-ownership, and test mapping. |
| Approved Swift feature | `swift_worker` | Apple implementation with state/concurrency constraints. |
| Build, scheme, simulator, or log failure | `xcode_triager` | Xcode evidence before a patch. |
| Apple API availability question | `apple_docs_researcher` | Current official Apple semantics and availability. |
| Swift regression or concurrency review | `swift_reviewer` | Apple behavioral, state, concurrency, and test risk. |
| Difficult failure after triage | `deep_debugger` | Escalated Apple investigation only after triage. |

The approved assignments are: Terra/medium for `swift_explorer`, `swift_worker`,
and `xcode_triager`; Terra/high for `apple_docs_researcher`; and Sol/high for
`swift_reviewer` and `deep_debugger`. Eight simulations include a two-Sol/high
candidate stress case: the runner selects `swift_reviewer` and suppresses
`deep_debugger`, so every automatic task remains within the central budget of
one. `gatekeeper` is not an automatic route; it remains a manual-only exhaustive
review lane.

No retained Apple profile is persona-only: each cites a concrete tool,
platform, or verification boundary. None of the retained Apple profiles was
redundant in these scenarios. The general layer remains sufficient for the
inventory baseline; the Apple layer takes over only at the distinct boundaries
listed above.
