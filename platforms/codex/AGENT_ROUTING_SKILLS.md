# Agent Skill Routing Guide

This file is the fast-routing surface for another agent.
Read this before starting work in an agent-configured repository.

The goal is simple:

- identify the task shape
- pick the right agent first
- pick the right skill only when it matches the job
- avoid using heavyweight agents or workflow skills for the wrong problem

For the full machine-readable inventory, read:

- `AGENT_ROUTING_SKILLS.yaml`

## Routing Order

Use this order:

1. Identify whether the task is read-only exploration, implementation, debugging, review, docs research, or workflow hygiene.
2. Pick the agent that matches the work mode.
3. Add a skill only if the task clearly matches a skill's "use when" boundary.
4. Prefer the narrowest tool that can complete the job correctly.

## Agent Quick Picks

### `swift_explorer`

Use when:

- the repo is Apple-platform focused
- you need to map files, symbols, entry points, state ownership, or likely edit targets
- no edits should happen yet

Do not use when:

- the repo is not Apple-specific
- you already know the exact files and need to edit

### `explorer`

Use when:

- you need generic read-only repo mapping
- the repo is not mainly Swift, Xcode, iOS, or macOS

### `swift_worker`

Use when:

- the task is normal implementation work in Swift, SwiftUI, UIKit, AppKit, or tests
- the change spans more than a tiny one-file tweak
- you need a practical default Apple implementation agent

Do not use when:

- the task is only a tiny localized edit
- the main task is triage, review, or deep debugging

### `spark_editor`

Use when:

- the scope is already clear
- the edit is tiny and localized
- examples include renames, preview stubs, small UI glue, and boilerplate

Do not use when:

- the task involves architecture, concurrency, SwiftData, multi-file refactors, or root-cause debugging

### `xcode_triager`

Use when:

- builds fail
- tests fail
- schemes, simulators, or logs need investigation
- the problem is not yet understood

Do not use when:

- you already have the root cause and need implementation
- the issue is mainly API semantics or framework behavior

### `deep_debugger`

Use when:

- the bug is hard
- prior triage did not isolate the cause
- the problem involves runtime behavior, concurrency, SwiftData, simulator failures, or a risky migration

Do not use when:

- a narrower agent can handle the task
- the issue has not been triaged at all

### `swift_reviewer`

Use when:

- reviewing diffs
- looking for regressions
- checking architecture drift, concurrency issues, state bugs, or missing tests

### `gatekeeper`

Use when:

- you want stricter-than-normal review
- the target includes code, docs, specs, prompts, or plans
- exhaustive findings matter more than speed

### `apple_docs_researcher`

Use when:

- Apple API behavior is uncertain
- you need framework semantics, version availability, or platform-specific references
- guessing would be risky

## Skill Quick Picks

There are two layers of skills here:

- repo-curated platform workflow skills under `platforms/codex/skills/`
- shared local skills cataloged from `~/.agents/skills` in `AGENT_ROUTING_SKILLS.yaml`

Use this file as the fast router.
Use `AGENT_ROUTING_SKILLS.yaml` when you need the broader inventory.

For shared local skills:

- on the same machine, resolve them from `~/.agents/skills/<skill-name>/SKILL.md`
- on a new machine, do not assume that path exists
- if the shared skill set is missing, tell the agent to install or sync the shared skills for that machine, or fall back to repo-curated skills when possible

### `ios-macos-repo-workflow`

Description:

- Creates and maintains a small repo-local workflow contract for Xcode-first Apple app repositories and SwiftPM-only Apple codebases.

Use when:

- bootstrapping repo-local workflow scripts
- refreshing `AGENTS.md` workflow guidance
- auditing build, test, or verify entrypoints
- standardizing lightweight workflow surfaces in an Apple repo

Do not use when:

- the task is feature implementation
- the task is CI-only
- the user only wants build triage rather than workflow structure

### `apple-ci-bootstrap`

Description:

- Proposes and creates narrow GitHub Actions CI for Apple-platform repositories with repo-truth-first command selection and concise diagnostics.

Use when:

- creating CI for an Apple repo
- auditing existing GitHub Actions workflow drift
- refreshing CI to match repo-local command truth

Do not use when:

- the task is local workflow scripting only
- the task is release automation, signing, deployment, or notarization

### `publish-workflow`

Description:

- Creates or reuses the right branch, commits scoped changes, optionally pushes, and keeps issue and PR hygiene disciplined.

Use when:

- the user asks to create a branch
- the user asks to commit
- the user asks to push or publish local changes
- the user wants PR-ready git output without auto-creating a PR

Do not use when:

- the work is still being implemented
- the diff scope is unclear or mixed

## Shared Skill Families

Use these families from `AGENT_ROUTING_SKILLS.yaml` when the task clearly matches them:

- `apple_platform`: Apple AI, iOS design, SwiftUI, SwiftData, Swift Concurrency, testing, and iOS debugging
- `workflow_git_ci`: CI, GitHub comments, CI failure repair, publish flows, and commit helpers
- `planning_product`: PRDs, issue slicing, handoffs, architecture improvement, prototype work, and goal shaping
- `docs_research`: current docs, PDFs, screenshots, and framework-reference tasks
- `design_visual`: Figma, design systems, diagrams, graph views, prototypes, pets, and visual exploration
- `deployment_platforms`: Cloudflare, Netlify, Render, and Vercel deploy flows
- `quality_debugging`: diagnosis, TDD, strict review, AppSec review, threat modeling, and Sentry inspection
- `content_media`: notebooks, Notion capture, speech, and transcription
- `devtools_and_meta`: CLIs, migration-to-Codex, browser automation, WinUI, and skill-authoring

## Task To Agent And Skill Map

| Task shape | Preferred agent | Preferred skill | Notes |
| --- | --- | --- | --- |
| Understand an Apple repo before editing | `swift_explorer` | none | Default first pass for Swift/Xcode repos |
| Understand a non-Apple repo before editing | `explorer` | none | Generic read-only mapping |
| Small localized code or UI tweak | `spark_editor` | none | Use only when scope is already clear |
| Normal Apple implementation or medium refactor | `swift_worker` | none | Default write-capable Apple agent |
| Build/test/simulator/scheme failure | `xcode_triager` | none | Triage before deeper debugging |
| Hard runtime or concurrency bug | `deep_debugger` | none | Use after evidence-based triage |
| Apple API uncertainty | `apple_docs_researcher` | none | Docs-first, read-only |
| Review a diff for regressions and missing tests | `swift_reviewer` | none | Findings-first review |
| Exhaustive pre-submit review of code/docs/specs | `gatekeeper` | none | Stricter manual gate |
| Create or refresh repo-local workflow scripts and AGENTS guidance | `swift_worker` or `swift_explorer` | `ios-macos-repo-workflow` | Start read-only if ownership is unclear |
| Create or refresh Apple CI workflows | `swift_worker` or `swift_explorer` | `apple-ci-bootstrap` | Treat CI as separate from local workflow |
| Create branch, commit, push, prepare PR-ready output | `swift_worker` | `publish-workflow` | Use only after work is ready to publish |

## Common Combinations

Use these combinations when the task spans multiple phases:

1. Repo orientation for Apple codebase:
   `swift_explorer` -> `apple_docs_researcher` if semantics are unclear -> `swift_worker` for implementation
2. Build failure:
   `xcode_triager` -> `deep_debugger` only if triage does not isolate the cause
3. Workflow modernization:
   `swift_explorer` -> `ios-macos-repo-workflow`
4. CI modernization:
   `swift_explorer` -> `apple-ci-bootstrap`
5. Ready to publish:
   `swift_worker` -> `swift_reviewer` if review is needed -> `publish-workflow`

## Selection Rules

- Prefer `swift_explorer` over `explorer` in Swift, iOS, macOS, Xcode, SwiftUI, UIKit, AppKit, SwiftData, or XCTest repositories.
- Prefer `spark_editor` only for tiny changes. If you are debating whether the edit is tiny, it probably is not.
- Prefer `xcode_triager` before `deep_debugger`.
- Prefer `apple_docs_researcher` when Apple framework behavior is uncertain.
- Use `publish-workflow` only after implementation scope is stable enough to commit intentionally.
- Do not attach a skill just because one exists. Use the skill only when the task matches its boundary.

## Source Of Truth

The detailed behavior for each surface lives here:

- `platforms/codex/AGENTS.md`
- `platforms/codex/AGENT_ROUTING_SKILLS.yaml`
- `platforms/codex/agents/*.toml`
- `platforms/codex/skills/apple-ci-bootstrap/SKILL.md`
- `platforms/codex/skills/ios-macos-repo-workflow/SKILL.md`
- `platforms/codex/skills/publish-workflow/SKILL.md`

If this guide and a source file disagree, the source file wins.
