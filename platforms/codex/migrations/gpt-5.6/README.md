# GPT-5.6 Global Routing Migration Proposal

This directory is the ticket-owned, reviewable source for issue #7. It does not alter `~/.codex/AGENTS.md` or `~/.codex/agents/`.

`shared/routing/routing-policy.toml` is the already committed central-policy source introduced by issue #4; this proposal validates its managed-block projection against that file rather than copying policy into this migration.

Run the source checks:

```sh
python3 scripts/validate-global-routing.py \
  --source platforms/codex/migrations/gpt-5.6 \
  --observed platforms/codex/migrations/gpt-5.6/observed.toml \
  --shared-policy shared/routing/routing-policy.toml \
  --live-agents ~/.codex/agents
python3 scripts/render-global-routing-migration.py \
  --source platforms/codex/migrations/gpt-5.6
```

Before any runtime migration, start one separate `gpt-5.6-sol` high, read-only review. Give it this directory, the live `~/.codex/AGENTS.md`, and live `~/.codex/agents/*.toml`; ask it to verify the inventory, model availability, installed skill references, policy projection, Apple exceptions, and safe install order. It must not write global files.

Only after that review is accepted, refresh the read-only observation snapshot and run the dry-run application command below. It validates the live inventory before writing, makes a timestamped backup under `~/.codex/.routing-backups/`, replaces exactly one managed block while preserving all unrelated global guidance, installs new profiles, and patches only `model`, `model_reasoning_effort`, and `sandbox_mode` for same-name Apple profiles. If a write or post-write assignment validation fails, it restores the backup. It never removes legacy profiles: removal is a separate explicit operation after the installed replacements validate.

```sh
python3 scripts/apply-global-routing-migration.py \
  --source platforms/codex/migrations/gpt-5.6 \
  --observed platforms/codex/migrations/gpt-5.6/observed.toml \
  --shared-policy shared/routing/routing-policy.toml \
  --global-root ~/.codex

# Only after reviewing the output and explicitly approving global writes:
python3 scripts/apply-global-routing-migration.py \
  --source platforms/codex/migrations/gpt-5.6 \
  --observed platforms/codex/migrations/gpt-5.6/observed.toml \
  --shared-policy shared/routing/routing-policy.toml \
  --global-root ~/.codex --apply
```
