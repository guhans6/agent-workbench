# agent-workbench

Private home for reusable agent assets across Codex and other agent setups.

This repo is source-of-truth oriented, not a raw dump of runtime state.
It keeps reusable skills, custom agent configs, and selected non-secret global config.
It excludes auth tokens, session history, caches, logs, plugin caches, and other sensitive or machine-local runtime files.

## Structure

- `platforms/codex/migration/`
  - migration playbook, skill catalog, MCP catalog, and install metadata for recreating this setup on a new machine
- `platforms/codex/skills/`
  - custom Codex skill sources
- `platforms/codex/agents/`
  - custom Codex subagent definitions
- `platforms/codex/AGENTS.md`
  - global Codex routing guidance
- `platforms/codex/config.redacted.toml`
  - redacted Codex global config snapshot
- `platforms/codex/rules/`
  - Codex rule files worth keeping
- `shared/rules/`
  - non-Codex agent rules
- `shared/workflows/`
  - shared workflow notes
- `inventory/`
  - local inventory and export notes

## Included Now

- `publish-workflow`
- `apple-ci-bootstrap`
- `ios-macos-repo-workflow`
- Codex migration catalog for skills, plugins, and MCPs
- Codex global `AGENTS.md`
- Codex agent TOMLs
- Codex `default.rules`
- redacted Codex `config.toml`
- shared Graphify rule and workflow notes

## Excluded On Purpose

- `auth.json`
- API keys and secrets
- session history
- logs and sqlite state
- plugin caches
- system or bundled skills
- runtime-only temp files

See [inventory/local-agent-surfaces.md](inventory/local-agent-surfaces.md).

For a new-machine setup, start with [platforms/codex/migration/README.md](platforms/codex/migration/README.md).
