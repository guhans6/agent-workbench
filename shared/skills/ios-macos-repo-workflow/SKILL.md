---
name: ios-macos-repo-workflow
description: Creates and maintains a small repo-local workflow contract for Xcode-first Apple app repositories. Use when bootstrapping, refreshing, or auditing build/test/verify commands, AGENTS.md workflow guidance, or lightweight repo workflow scripts for iOS/macOS projects.
---

# iOS macOS Repo Workflow

## Purpose

This skill is a workflow contract generator and auditor for Apple app repos.
It is not a build-system framework, CI manager, or deep Apple engineering guide.

## Modes

- `bootstrap`: inspect a repo and propose an initial workflow contract
- `refresh`: inspect a repo with existing workflow artifacts and propose updates
- `audit`: inspect and report workflow drift without proposing writes by default

Infer a default mode from repo state, but announce it and allow override.
If uncertainty is high, prefer `audit`.
If repo rules indicate the active implementation surface is a different worktree or root than the provided path, use `audit` only until the active surface is confirmed.
If the checkout is already known to contain unrelated in-flight local changes, prefer `audit` until the write scope is explicit.

## Do Not Do

- Do not run commands during static inspection unless the user explicitly approves a probe phase.
- Do not assume every profile field is knowable from files alone.
- Do not write files before showing a proposal and getting approval.
- Do not install tools, activate hooks, rewrite CI, or boot simulators in v1.
- Do not force repo normalization when existing workflow truth is stronger.
- Do not turn this skill into a general Apple-platform advice dump.
- Do not switch to compact/caveman-style output unless the user explicitly asks for token reduction.

## Workflow

1. Perform static inspection only.
2. Build a partial repo profile.
3. Mark uncertain fields as `unknown`.
4. If repo rules indicate the active implementation surface lives in a different worktree or root than the provided path, switch to `audit`, summarize the divergence, and stop to ask before writing.
5. If the checkout is already known to contain unrelated in-flight local changes, switch to `audit`, summarize the risk, and stop to ask before writing.
6. Read [profile-schema.md](references/profile-schema.md) and use only that schema.
7. Render a concise proposal using [proposal-format.md](references/proposal-format.md).
8. Separate output into:
   - core changes
   - optional generated extensions
   - recommendations only
9. After approval, render repo-local artifacts from `templates/`.

When a repo already has a strong script layout signal such as `script/` or `scripts/`, preserve that layout instead of normalizing it to a new directory name in v1.

## V1 Scope

V1 targets Xcode-first Apple app repos.
Support only a narrow set of optional extensions:

- `ui_tests`
- `generated_project_support`
- `context_graph`
- `linting`
- `formatting`

Generated-project repos should be detected and handled conservatively.

For generated-project support:

- prefer Tuist for new clean repos when the user asks for generated-project adoption
- preserve XcodeGen when it already exists unless migration is explicitly approved
- do not auto-install Tuist or XcodeGen
- do not auto-migrate `.xcodeproj` ownership; proposals must explain learning curve, generated-file ownership, and rollback

Mixed Xcode/SPM repos should also be handled conservatively:

- preserve app-first intent when the repo shows an authoritative Xcode surface plus a supporting `Package.swift`
- keep the structured profile narrow; describe package support and workflow conflicts in prose instead of adding v1 takeover logic
- do not assume app target names, package products, and test import module names all match
- when module-surface drift is visible or likely, carry it as a risk or recommendation rather than inventing a global fixup rule

Repos with no established automated test surface should also be handled conservatively:

- allow `test_stack: none` when static inspection shows no meaningful repo test target or routine test command
- avoid inventing fake test automation just to fill the command surface
- in those repos, `test.sh` may remain an explicit no-test-yet placeholder and `verify-fast` may be build-first

## Rendered Artifacts

Core rendered artifacts:

- bounded managed workflow block in repo `AGENTS.md`
- small script surface for `build`, `test`, `verify-fast`, `verify-deep`, `bootstrap-dev`
- shared shell helper for logs and command checks

Optional rendered artifacts:

- `test-ui.sh`
- generation helper script for XcodeGen/Tuist-backed repos
- `graphify-refresh.sh` for optional agent context graph refresh
- inactive hook templates only when explicitly requested; manual installation and `chmod +x` remain repo decisions

## Context Graph Guidance

Graphify is optional and should reduce agent context overhead, not become part of normal verification.

Use an existing graph before broad architecture/refactor work, when file relationships are unclear, or when manual search would require reading many files.
Refresh graph output after meaningful structural changes if the repo has opted into the `context_graph` extension.
Do not run Graphify automatically during build, test, verify, commit, or CI paths in v1.

## Compact Output Guidance

If the user asks for lower token usage, caveman mode, or brief output, keep proposals and status updates compact while preserving technical accuracy.
Use normal clarity for approval-sensitive proposals, docs, destructive operations, and irreversible actions unless the user explicitly asks otherwise.

## Templates

- Managed AGENTS block: [workflow-block.md](templates/agents/workflow-block.md)
- Shell helper: [common.sh](templates/scripts/common.sh)
- Core scripts: `templates/scripts/*.sh`
- Inactive hook template: [pre-commit](templates/hooks/pre-commit)

## When To Stop And Ask

- primary workflow surface is ambiguous
- managed artifact ownership is unclear
- generated-project tooling is detected but existing command truth conflicts
- graph context exists but is stale and the requested task depends on broad architecture knowledge
- repo rules indicate the active implementation surface is a different worktree or root
- the checkout is already known to contain unrelated in-flight local changes
- a write would replace human-authored workflow files rather than patch skill-owned ones

## Validation Target

`MDZen` is the first validation repo for this skill, but repo-specific decisions must not become global defaults.
