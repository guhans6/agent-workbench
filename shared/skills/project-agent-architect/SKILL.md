---
name: project-agent-architect
description: Analyze a repository evidence-first and draft repo-local agent context, a project-team skill, Codex custom agents, and skill/MCP assignments. Use when the user asks to create project agents, a repo skill, local project context, subagent team, project profile, or Codex team configuration. Do not use for ordinary feature implementation.
---

# Project Agent Architect

Create a repo-local agent operating model from evidence. Do not implement product features. First produce a draft for approval; write files only after the user approves.

Read `references/role-model-policy.md` before drafting roles, model assignments, skill/MCP assignments, or research rules.

## Non-Negotiable Rules

1. Keep the first pass read-only.
2. Do not create or modify project files before approval.
3. Do not guess. Mark missing facts as `unknown`.
4. Cite evidence for every claim about stack, commands, architecture, tests, deploy, conventions, tools, skills, and MCPs.
5. Do not read, print, or copy secrets, `.env` values, tokens, private keys, credential files, or auth stores.
6. Do not install dependencies, run migrations, change infrastructure, or run destructive commands during analysis.
7. Use repo evidence first, then targeted official-doc research only when needed.
8. Preserve existing repo instructions and config. Propose minimal patches instead of overwrites.

## Phase 1: Evidence Inventory

Start from the current working directory. Find the git root with `git rev-parse --show-toplevel` when available.

Collect evidence from:

- `git status --short`
- top-level tree, excluding `.git`, `node_modules`, `.next`, `dist`, `build`, `target`, `.venv`, `venv`, `coverage`, `.turbo`, `.cache`
- manifests and lockfiles: `package.json`, lockfiles, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `Package.swift`, Xcode projects/workspaces, `Podfile`, `Gemfile`, `Dockerfile`, compose files, `Makefile`, `justfile`, `Taskfile.yml`
- CI files: `.github/workflows/*`, `.gitlab-ci.yml`, `circle.yml`, `azure-pipelines.yml`, `Jenkinsfile`
- docs: `README*`, `docs/**`, `CONTRIBUTING*`, `ARCHITECTURE*`, `SECURITY*`
- tests: `test/**`, `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*`, and framework-specific test folders
- agent surfaces: `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `.agents/**`, `.codex/**`, `.cursor/rules/**`, `.github/copilot-instructions.md`, `.mcp.json`, `mcp.json`

Record facts as:

| Claim | Evidence | Confidence |
|---|---|---|

## Phase 2: Skill, MCP, and Agent Inventory

Inventory only observable surfaces. Do not invent unavailable tools.

Check repo-local paths first:

- `.agents/skills/**/SKILL.md`
- `.codex/agents/*.toml`
- `.codex/config.toml`
- `.mcp.json` or `mcp.json`

Check user-level paths only if accessible and safe:

- `~/.agents/skills/**/SKILL.md`
- `~/.codex/skills/**/SKILL.md`
- `~/.codex/agents/*.toml`
- `~/.codex/config.toml`

Use live platform listings when available, such as `/skills`, `/mcp`, `/mcp verbose`, or `codex mcp list`.

Record surfaces as:

| Surface | Name | Source | Purpose | Safe to assign? | Notes |
|---|---|---|---|---|---|

## Phase 3: Draft the Project Team

Use the policy in `references/role-model-policy.md`.

The main role must be domain-specific, not generic. Derive it from evidence, for example:

- Apple repo: senior Apple platform engineer plus product-minded technical lead
- Web repo: senior product engineer specializing in the detected frontend/backend stack
- ML repo: ML systems engineer specializing in pipelines, evals, data contracts, and runtime constraints
- CLI/tooling repo: senior tooling engineer specializing in command UX, integration tests, packaging, and release flow

Use subagents selectively, not by default. The smallest useful team wins.

## Phase 4: Required Draft Output

The first run must output a chat draft and stop for approval.

Include:

1. Repo identity
2. Evidence ledger
3. Detected stack and architecture
4. Existing agent, skill, MCP, and instruction inventory
5. Main role proposal
6. Subagent roster proposal
7. Skill/MCP assignment proposal
8. Model and reasoning proposal
9. Research gate and when web/docs lookup is required
10. Files proposed for creation/modification
11. Risks and unknowns
12. Approval checklist

For each proposed role, include:

| Agent | Persona | Specialty | Thinking Style | Trigger | Model | Reasoning | Sandbox | Always-Use Skills | Conditional Skills | MCPs/Tools | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Phase 5: Proposed Files

Only propose files that are justified by repo evidence and user goals.

Common files:

```text
AGENTS.md
.agents/skills/<repo-slug>-project-team/SKILL.md
.agents/project-profile/evidence.md
.agents/project-profile/architecture.md
.agents/project-profile/agent-roster.md
.codex/config.toml
.codex/agents/<repo-slug>-explorer.toml
.codex/agents/<repo-slug>-implementer.toml
.codex/agents/<repo-slug>-reviewer.toml
.codex/agents/<repo-slug>-tester.toml
.codex/agents/<repo-slug>-docs-researcher.toml
```

If `AGENTS.md` exists, propose a minimal patch or appendix. Do not overwrite it. If `.codex/config.toml` exists, propose a minimal additive patch.

## Approval Message

End the first-run draft with:

```markdown
## Approval needed

I have not written files yet.

Approve one:

1. Approve as-is.
2. Approve but remove/change these roles: ...
3. Approve only the project skill, not Codex custom agents.
4. Revise the plan before writing files.

After approval I will create/modify only the listed files.
```

## After Approval

1. Create only approved files.
2. Preserve existing content.
3. Use minimal patches for existing files.
4. Validate that files exist.
5. Parse TOML if a parser is available.
6. Check skill frontmatter.
7. Run `git diff --stat`.
8. Report files changed, invocation commands, checks run, manual steps, and risks.
