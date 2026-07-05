# Agent Routing Index

This is the single starting point for another agent.

Use this file when the agent should first decide:

- which human router to read
- which machine catalog to load
- which platform-specific surface is relevant

## Start Order

If the task is to recreate or migrate this Codex setup to a new machine, start with `migration/README.md` and `migration/install-playbook.md`.

1. Read `AGENT_ROUTING_INDEX.yaml` if the consumer is machine-first.
2. Read `AGENT_ROUTING_SKILLS.md` to choose agents and skills.
3. Read `AGENT_ROUTING_MCPS.md` to choose MCP surfaces.
4. Fall through to the platform-specific source files only after the correct surface is identified.

## Human Entry Points

- `migration/README.md`: setup and migration starting point
- `migration/install-playbook.md`: new-machine recreate flow
- `AGENT_ROUTING_SKILLS.md`: fast routing for agents and skills
- `AGENT_ROUTING_MCPS.md`: fast routing for MCP selection
- `AGENTS.md`: higher-level repo guidance and routing rules

## Machine Entry Points

- `migration/surfaces.yaml`: structured migration inventory for skills, plugins, and MCPs
- `AGENT_ROUTING_INDEX.yaml`: master machine index
- `AGENT_ROUTING_SKILLS.yaml`: machine catalog for agents, skills, products, and related routing
- `AGENT_ROUTING_MCPS.yaml`: machine catalog for MCP routing

## Platform Scope

This directory is still the Codex platform surface:

- generic routing files here are written to be agent-neutral
- Codex-only products or MCP surfaces are explicitly marked in the machine catalogs
- cross-agent surfaces are marked as reusable when installed elsewhere

## Source Of Truth

- `platforms/codex/AGENTS.md`
- `platforms/codex/agents/*.toml`
- `platforms/codex/skills/*/SKILL.md`
- `platforms/codex/migration/surfaces.yaml`
- `platforms/codex/AGENT_ROUTING_SKILLS.yaml`
- `platforms/codex/AGENT_ROUTING_MCPS.yaml`

If this file disagrees with the machine catalogs, the machine catalogs win.
