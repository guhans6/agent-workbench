# Companion rich-team refresh experiment (#10)

## Scope and safety boundary

This experiment reads `/Users/guhan/Documents/Companion` only. It produces no
candidate patch for that checkout, because the target's active rich-team files
and working tree are pre-existing work that require separate repository
approval. `scripts/validate-rich-team-refresh-experiment.py` snapshots Git
status before and after every run and fails if it changes.

The target is a legacy rich-team contract rather than a v2 managed routing
overlay, so the command reports that no target patch was applied. The sterile
fixture is where the proposed v2 delta renderer is exercised.

Run:

```sh
python3 scripts/validate-rich-team-refresh-experiment.py \
  --repository /Users/guhan/Documents/Companion
```

The captured run passed with the target's existing dirty scope unchanged:

- 8 profiles: docs researcher, explorer, implementer, investigator, issue
  slicer, reviewer, scout, and visual tester.
- 6 admitted local profiles; scout and investigator are removal/merge
  recommendations. The command evaluates each profile against the policy's
  recognizable task class, distinct execution boundary, concise local
  instructions, recurring lane, and value-overhead criteria. The final
  criterion is evidenced in
  `experiments/companion-rich-team-admission.toml`: each profile's observed
  boundary is captured, and the scout/investigator entries cite their overlap
  with the committed `global_scout` bounded-inventory and `global_debugger`
  difficult-investigation lanes. The command verifies those names and triggers
  against `platforms/codex/migrations/gpt-5.6`. This is separate from
  their dirty-state provenance, which is preserved rather than used to decide
  removal.
- Model assignment is not a removal mechanism: no model migration is proposed
  by this experiment.
- The planning capability recommendation is `to-prd` to `to-spec` and
  `to-issues` to `to-tickets`; Context7 stays plugin-backed and the duplicate
  standalone MCP remains disabled.

## Delta rendering and metrics

`tests/rich_team_experiment/test_command.py` contains a sterile eight-profile
fixture. It submits one approved profile-only planning-capability replacement
to `scripts/refresh-routing.py`. The observable result is exactly one changed
row and one proposed file followed by `PRESERVED: Everything else preserved`.
It never deletes or merges profiles.

The command records every pre-existing porcelain-status entry in its approval
surface. Its seven decision lines are compared with the observed roster count
plus two framing lines: the eight-role target therefore yields ten lines and a
30% reduction. The recommended follow-up,
subject to separate Companion approval, is a six-profile configuration with
the two removal candidates handled in a distinct change from any model
migration.

## Verification

```sh
python3 tests/rich_team_experiment/test_command.py
python3 scripts/validate-rich-team-refresh-experiment.py \
  --repository /Users/guhan/Documents/Companion
```
