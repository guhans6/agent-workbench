# GPT-5.6 Global Routing Migration Proposal

This directory is the ticket-owned, reviewable source for issue #7. It does not alter `~/.codex/AGENTS.md` or `~/.codex/agents/`.

`shared/routing/routing-policy.toml` is the already committed central-policy source introduced by issue #4; this proposal validates its managed-block projection against that file rather than copying policy into this migration.

Run the source checks:

```sh
python3 scripts/validate-global-routing.py \
  --source platforms/codex/migrations/gpt-5.6 \
  --observed platforms/codex/migrations/gpt-5.6/observed.toml \
  --shared-policy shared/routing/routing-policy.toml
python3 scripts/render-global-routing-migration.py \
  --source platforms/codex/migrations/gpt-5.6
```

Before any runtime migration, start one separate `gpt-5.6-sol` high, read-only review. Give it this directory, the live `~/.codex/AGENTS.md`, and live `~/.codex/agents/*.toml`; ask it to verify the inventory, model availability, installed skill references, policy projection, Apple exceptions, and safe install order. It must not write global files.

Only after that review is accepted, copy the managed routing block and proposed TOMLs into the global runtime. Install `global_*` replacements and `spark_editor_gpt56` first, validate the live runtime using a refreshed read-only observation snapshot, and retain `explorer` and `spark_editor` until their replacements have been installed and validated. Do not silently substitute unavailable models. Apply Apple profile updates only after the same validation. Keep `gatekeeper` manual-only.
