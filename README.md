# agent-workbench

Home for reusable agent assets across Codex and other agent setups.

This repo contains usefuls skills and tools used for dev workflow.
It keeps reusable skills, custom agent configs, and selected non-secret global config.

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

See [inventory/local-agent-surfaces.md](inventory/local-agent-surfaces.md).

For a new-machine setup, start with [platforms/codex/migration/README.md](platforms/codex/migration/README.md).
