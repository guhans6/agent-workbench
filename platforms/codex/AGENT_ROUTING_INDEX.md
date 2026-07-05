# Agent Routing Index

This is the single starting point when an agent needs to choose a Codex-specific agent, skill, or MCP surface.

For the repo-wide agent asset catalogue and install guidance, start at `../../catalog/README.md`.

## Start Order

1. Read `AGENT_ROUTING_INDEX.yaml` if the consumer is machine-first.
2. Read `AGENT_ROUTING_SKILLS.md` to choose agents and skills.
3. Read `AGENT_ROUTING_MCPS.md` to choose MCP surfaces.
4. Fall through to the platform-specific source files only after the correct surface is identified.

## Human Entry Points

- `../../catalog/README.md`: repo-wide agent asset catalogue
- `AGENT_ROUTING_SKILLS.md`: fast routing for agents and skills
- `AGENT_ROUTING_MCPS.md`: fast routing for MCP selection
- `AGENTS.md`: higher-level repo guidance and routing rules

## Machine Entry Points

- `../../catalog/surfaces.yaml`: repo-wide catalogue for skills, plugins, and MCPs
- `AGENT_ROUTING_INDEX.yaml`: master machine index
- `AGENT_ROUTING_SKILLS.yaml`: machine catalog for agents, skills, products, and related routing
- `AGENT_ROUTING_MCPS.yaml`: machine catalog for MCP routing

## Platform Scope

This directory is the Codex platform surface:

- generic routing files here are written to be agent-neutral where possible
- Codex-only products or MCP surfaces are explicitly marked in the machine catalogs
- cross-agent skills live under `shared/skills/`

## Source Of Truth

- `catalog/surfaces.yaml`
- `shared/skills/*/SKILL.md`
- `platforms/codex/AGENTS.md`
- `platforms/codex/agents/*.toml`
- `platforms/codex/skills/*/SKILL.md`
- `platforms/codex/AGENT_ROUTING_SKILLS.yaml`
- `platforms/codex/AGENT_ROUTING_MCPS.yaml`

If this file disagrees with the machine catalogs, the machine catalogs win.
