# Codex Platform Assets

This directory contains reusable assets for the Codex platform:

- Codex-specific skills
- custom subagent configs
- routing guidance
- non-secret config snapshots
- rule files

For the agent-neutral catalogue, start at `../../catalog/README.md`.

`config.redacted.toml` is a curated snapshot, not a raw runtime export. It intentionally omits secrets and local trust-state noise.

## Start Here

If another agent needs to decide which Codex agent, skill, or MCP surface to use for a task, read:

- `AGENT_ROUTING_INDEX.md` for the single human starting point
- `AGENT_ROUTING_INDEX.yaml` for the single machine-readable starting point
- `AGENT_ROUTING_INDEX.json` for the JSON export of the master index
- `AGENT_ROUTING_SKILLS.md` for the task-to-surface routing guide
- `AGENT_ROUTING_SKILLS.yaml` for the machine-readable inventory of agents, skills, products, and MCP surfaces
- `AGENT_ROUTING_SKILLS.json` for the JSON export of the skills catalog
- `AGENT_ROUTING_MCPS.md` for the MCP routing guide
- `AGENT_ROUTING_MCPS.yaml` for the machine-readable MCP inventory
- `AGENT_ROUTING_MCPS.json` for the JSON export of the MCP catalog
- `AGENTS.md` for the higher-level routing rules

Detailed source files live under:

- `agents/*.toml`
- `skills/*/SKILL.md`
