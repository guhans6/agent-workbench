---
name: project-agent-architect
description: Bootstrap first-time repository routing when a repository has no routing contract and needs Repository Context or exceptional Repository-Specific Profiles. Existing contracts route to refresh-project-agent-routing.
---

# Project Agent Architect

Bootstrap a routing contract for a repository that has no existing routing contract. An existing contract routes to `refresh-project-agent-routing`.

## Bootstrap

1. Keep the target repository read-only while inspecting its instructions, context, plans, manifests, scripts, tests, and existing routing surfaces. Treat missing or conflicting boundaries as unresolved. Complete when every repository claim cites a path, every unknown is named, and no target file changed.
2. Inventory available global execution profiles and their exact model, reasoning, access, skill, and tool assignments in a temporary observations file outside the target repository. Complete when every profile referenced by the proposal has observed assignments and every unavailable capability is excluded rather than substituted.
3. Run the bundled `scripts/bootstrap-routing.py --repository <repo> --global-profile '<name>|<trigger>|<model>|<reasoning>|<access>'` relative to this skill directory, supplying every observed global profile. Complete when its PASS/WARN/FAIL result and evidence list are captured as the first approval-surface row.
4. Select global profiles first. A Repository-Specific Profile is admitted only when a recognizable task class, distinct execution boundary, concise local instruction delta, recurring evidence, and value over coordination cost are all demonstrated. When one is admitted, read [routing-contract.md](references/routing-contract.md) before drafting it. Complete when every proposed local profile cites evidence for all five conditions, or the result explicitly says `No Repository-Specific Profiles proposed`.
5. Draft the Managed Routing Block in `AGENTS.md`; when local profiles are admitted, also draft `routing.toml` and their `.codex/agents/*.toml` files. Complete when the exact proposed-file list is limited to those contract files and excludes unrelated artifacts.
6. Present status, routing table, attention-required changes, file delta, and approval checklist, with detailed evidence available on request. Complete when every proposed route, model, reasoning level, access boundary, warning, and file appears exactly once.
7. Stop before target writes and obtain approval for the exact file list. Complete when the user approves that list or the run ends without repository changes.
8. After approval, apply the minimal patch and run the bundled `scripts/validate-routing.py --bootstrap` relative to this skill directory for a no-profile proposal, or normal mode with `--observations <temporary-observations>` when local profiles exist. Complete when no FAIL remains and every WARN is fixed, accepted, or explicitly deferred.

`No Repository-Specific Profiles proposed` is a successful bootstrap outcome.
