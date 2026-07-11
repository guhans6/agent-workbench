---
name: refresh-project-agent-routing
description: Refresh an existing routing contract through a delta-only approval surface. Use when relevant models, capabilities, tools, or repository evidence changed; never use for first-time routing bootstrap.
---

# Refresh Project Agent Routing

Refresh only an existing Managed Routing Block. Do not infer bootstrap mode or regenerate complete files.

## Draft

1. Keep the pass read-only. Inspect the existing managed block, agent TOMLs, repository context, and only the changed model, skill, MCP, tool, or repository evidence.
2. Create a proposed-files directory containing only affected files and patch each managed section or TOML field minimally.
3. Run `scripts/refresh-routing.py --repository <repo> --routing <proposed-files> --approved-file <path>` for every proposed file. Its approval surface must show changed rows, the separate exact model-assignment delta, and `Everything else preserved`.
4. If capability identities changed, replace stale references only in affected routing or profile fields. Do not change unrelated profiles, models, or reasoning assignments.
5. Stop for approval before applying the proposed patches. `FAIL` blocks application; `WARN` findings must be fixed, accepted, or deferred explicitly.
6. After approval, apply only the reviewed minimal patches and rerun the shared validator against the final routing tree. Report the revalidation result.
