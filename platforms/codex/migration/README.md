# Codex Migration Catalog

This directory is the starting point when moving the user's Codex setup to a new machine or another agent environment.

Use it differently from the routing catalogs:

- Routing files answer: "Which skill or MCP should an agent use for this task?"
- Migration files answer: "What exists on this machine, where did it come from, and how do I recreate it?"

## Start Order

1. Read `install-playbook.md` for the full migration flow.
2. Read `skills-catalog.md` for current skill groups, source locations, and install paths.
3. Read `mcps-catalog.md` for configured MCP servers and recreate commands.
4. Read `surfaces.yaml` when an agent needs structured source/install metadata.
5. Fall back to `../AGENT_ROUTING_INDEX.md` only after the machine has the same surfaces installed.

## Portability Rules

- Prefer installable upstream sources over copying machine-local folders.
- Treat `~/.agents/skills` and `~/.codex/skills` entries as local-only unless this catalog names an upstream repo or package.
- Do not copy plugin caches directly. Install plugins through Codex's plugin UI or CLI plugin browser.
- Do not copy secrets from `~/.codex/config.toml`; recreate MCPs and re-authenticate.
- Keep this repo's curated skill folders under `platforms/codex/skills/` as the portable source for personal skills that are intentionally checked in.

## Official Codex Facts Used

The Codex manual says skills can live in repo, user, admin, and system locations; plugins are the installable distribution unit for reusable skills and apps; MCP servers are configured in `config.toml` or with `codex mcp`; and plugins may bundle skills, apps, and MCP servers.

