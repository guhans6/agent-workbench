# agent-workbench

Private home for reusable agent assets across Codex and other agent setups.

This repo is a source-of-truth catalogue, not a raw dump of runtime state. It keeps reusable skills, MCP setup notes, custom agent configs, and selected non-secret global config. It excludes auth tokens, session history, caches, logs, plugin caches, and other sensitive or machine-local runtime files.

## Start Here

- `catalog/README.md` is the agent-neutral entrypoint.
- `catalog/skills.md` lists shared, Codex-specific, system, and plugin skills.
- `catalog/mcps.md` lists configured MCP servers and install/verification notes.
- `catalog/surfaces.yaml` is the structured catalogue for agents.

## Structure

- `shared/skills/`: vendored local skills intended for any compatible agent.
- `shared/rules/` and `shared/workflows/`: cross-agent notes and workflows.
- `platforms/codex/`: Codex-specific agents, routing, rules, config snapshots, and local Codex-home skills.
- `inventory/`: local inventory and export notes.

## Excluded On Purpose

- auth tokens, API keys, and secrets
- session history, logs, sqlite state, and runtime caches
- plugin caches and bundled runtime files
- generated build output

See `catalog/README.md` before installing assets on a new machine or in a different agent.
