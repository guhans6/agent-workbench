---
name: project-agent-architect
description: Bootstrap first-time repository routing from observed evidence. Use when the user asks to set up project routing, repo-local agent context, or exceptional local agent profiles for a repository that has no existing routing contract. Produce a concise approval surface before any write; do not use for routing refreshes or ordinary feature implementation.
---

# Project Agent Architect

Bootstrap a routing contract for a repository that has no existing routing contract. Do not infer refresh mode; use `refresh-project-agent-routing` when a routing contract already exists.

## Draft

1. Keep the pass read-only. Do not read secrets or install dependencies.
2. Inspect repository instructions, context, plans, manifests, scripts, tests, and existing routing surfaces. Treat missing or conflicting boundaries as unresolved; never invent architecture.
3. Inspect available global execution profiles and exact model, reasoning, access, skill, and tool assignments. Reject unavailable profiles or capabilities; never silently substitute one.
4. Run `scripts/bootstrap-routing.py --repository <repo>` for the compact preflight. Use its PASS/WARN/FAIL result as the first approval-surface row.
5. Select global profiles first. Propose a repository-specific profile only when the task class, distinct execution boundary, concise local instruction delta, recurring evidence, and value over coordination cost are all demonstrated.
6. Propose only a managed routing/context block in `AGENTS.md` and justified `.codex/agents/*.toml` files. Do not propose a project-team skill, evidence ledger, architecture profile, or roster by default.
7. Present only status, routing table, attention-required changes, file delta, and approval checklist. Keep detailed evidence available on request.
8. Stop for approval before writing. After approval, make a minimal patch, run `scripts/validate-routing.py` against the proposal, fix all FAIL findings, and report accepted/deferred WARN findings.

`No local profiles proposed` is a successful bootstrap outcome.
