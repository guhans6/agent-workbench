# Local Agent Surfaces

This inventory summarizes what this repo currently carries.

## Agent-Neutral Catalogue

- `catalog/README.md`
- `catalog/skills.md`
- `catalog/mcps.md`
- `catalog/surfaces.yaml`

## Shared Skills

The first-level skill folders from `~/.agents/skills` are vendored under `shared/skills/`, excluding backup/runtime folders.

Shared skills count: 102 (verified 2026-10-06). The original platform/MCP snapshot is not refreshed by this limited session sync.

## Codex Platform Assets

- `platforms/codex/skills/`: Codex-home-specific local skills and existing Codex platform skill sources.
- `platforms/codex/agents/*.toml`: Codex subagent definitions.
- `platforms/codex/AGENT_ROUTING_*.{md,yaml,json}`: Codex routing catalogs.
- `platforms/codex/config.redacted.toml`: redacted Codex config snapshot.
- `platforms/codex/rules/default.rules`: Codex rule file.

## Pi and Completion Guidance

- `platforms/pi/AGENTS.md`: approved Pi global Completion block.
- `platforms/pi/README.md`: loaded-path and approval-first merge guidance.
- `platforms/codex/AGENTS.md`: existing routing preserved plus the matching Completion block.
- `shared/workflows/session-asset-sync.md`: pinned skill provenance and verification limits.

## Redaction Notes

The exported Codex config snapshot is redacted:

- API keys removed
- project trust blocks omitted
- auth/session/runtime files not copied

Plugin caches, system skills, and local runtime state are documented in the catalog but not vendored.
