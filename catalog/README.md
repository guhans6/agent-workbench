# Agent Asset Catalog

This is the agent-neutral starting point for the user's reusable skills, MCP servers, and agent platform assets.

Use this repo as a catalogue and source checkout:

- `shared/skills/` contains vendored local skills that any compatible agent can install or inspect.
- `platforms/codex/` contains Codex-specific agents, routing, rules, config snapshots, and Codex-home-only skills.
- `catalog/skills.md` lists every skill source visible from this machine.
- `catalog/mcps.md` lists the configured MCP servers and how to recreate or verify them.
- `catalog/surfaces.yaml` is the machine-readable catalogue for agents.

## Install Patterns

For independent shared skills, copy or symlink the selected folder into the target agent's skill directory. Checkpoint consumers require the complete skills/workflows layout below; a single-folder copy leaves their shared reference unresolved. For Codex, the user-level target is usually:

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

Completion guidance is curated in `../platforms/pi/AGENTS.md` and the marked Completion section of `../platforms/codex/AGENTS.md`. Confirm each host's loaded global file (Pi agent directory; Codex `$CODEX_HOME`, normally `~/.codex`, with override precedence), preview a diff, and obtain approval before merging the block once. Preserve existing instructions rather than copying a whole global file over them. Shared skill storage is not a universal global-instruction location.

For pinned skills, explicit-only invocation, and validation limits, read `../shared/workflows/session-asset-sync.md`. The setup skill configures an approved repo reference/pointer; it does not install global guidance.

Plugin/system skills and MCP servers are not copied from runtime caches. Install them through their provider or package command, then verify with the target agent.

## Validated checkpoint bundle

The locally adapted `to-tickets`, `implement` and `setup-matt-pocock-skills` consume `shared/workflows/validated-checkpoints.md`. Install those folders and `matt-informed-engineering` under the target asset root's `skills/`, with the protocol under its sibling `workflows/`. Preview destination differences and preserve local edits before installation. See [maintenance and installation](../shared/workflows/skill-maintenance.md) for upstream merge rules and project adoption.

Run `python3 scripts/verify-checkpoint-assets.py` from this checkout for structural and temporary installation checks. To read-check an installed or staged bundle, use `python3 scripts/verify-checkpoint-assets.py --installation-root <agent-assets>`. Neither command installs assets, updates global/project instructions, nor establishes live host discovery.

The setup skill previews a checked-in project protocol and one pointer in the existing AGENTS.md/CLAUDE.md. Existing project copies change only through separately approved adoption/update; global skill refreshes do not overwrite them. [Qualification evidence and remaining boundaries](../shared/workflows/checkpoint-qualification.md).
