# Agent Asset Catalog

This is the agent-neutral starting point for the user's reusable skills, MCP servers, and agent platform assets.

Use this repo as a catalogue and source checkout:

- `shared/skills/` contains vendored local skills that any compatible agent can install or inspect.
- `platforms/codex/` contains Codex-specific agents, routing, rules, config snapshots, and Codex-home-only skills.
- `catalog/skills.md` lists every skill source visible from this machine.
- `catalog/mcps.md` lists the configured MCP servers and how to recreate or verify them.
- `catalog/surfaces.yaml` is the machine-readable catalogue for agents.

## Install Patterns

For shared skills, copy or symlink the selected folder into the target agent's skill directory. For Codex, the user-level target is usually:

```bash
mkdir -p ~/.agents/skills
cp -R shared/skills/<skill-name> ~/.agents/skills/
```

For Codex-specific assets, install from `platforms/codex/` and keep secrets out of the repo:

- skills: `platforms/codex/skills/`
- subagents: `platforms/codex/agents/`
- routing docs and catalogs: `platforms/codex/AGENT_ROUTING_*.{md,yaml,json}`
- rules: `platforms/codex/rules/`
- config example: `platforms/codex/config.redacted.toml`

Plugin/system skills and MCP servers are not copied from runtime caches. Install them through their provider or package command, then verify with the target agent.
