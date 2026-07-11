# Issue #11: v2 defaults synthesis

This artifact aggregates the committed experiments for [#8](https://github.com/guhans6/agent-workbench/issues/8), [#9](https://github.com/guhans6/agent-workbench/issues/9), and [#10](https://github.com/guhans6/agent-workbench/issues/10), alongside the completed global migration (#7). It is advisory to the orchestrator and does not close parent spec [#3](https://github.com/guhans6/agent-workbench/issues/3).

Re-render the deterministic synthesis:

```sh
python3 scripts/synthesize-v2-defaults.py --format markdown
python3 -m unittest tests/v2_defaults_synthesis/test_command.py
```

## Recommended final policy judgment

Retain the v2 defaults with an evidence qualifier. The selected nine representative routes record no user correction, and all observed automatic Sol/high selections remain inside the budget of one. No checked artifact supports revising or cutting an accepted v2 policy decision. The synthesis retains the hard-failure guard but does not claim to independently revalidate every hard-failure category; that remains the responsibility of the underlying experiment validators.

This is not a claim that every acceptance criterion is fully live-validated: #8's clean non-Apple result is a controlled projection because the actual ytm-tui target already had a routing contract. A future genuinely clean non-Apple bootstrap should replace that partial evidence.

The renderer is the complete comparison: it lists all nine routes, assignments, escalation outcomes, approval lengths, profile counts, the six separately evidenced Apple-specialist boundaries, retained/revised/cut policy decisions, and the limitation without collapsing the #8 result into a success claim. It records the economic comparison as not measured: no cheap-route rework was observed, and cost/latency telemetry remains deliberately deferred, so it makes no numerical savings claim.
