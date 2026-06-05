# Agent Platform Assets

This directory contains reusable agent-facing assets for the Codex platform:

- custom skills
- custom subagent configs
- global routing guidance
- non-secret config snapshots
- rule files

`config.redacted.toml` is a curated snapshot, not a raw runtime export.
It intentionally omits secrets and local trust-state noise.

## Start Here

If another agent needs to decide which agent, skill, or MCP surface to use for a task, read:

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
