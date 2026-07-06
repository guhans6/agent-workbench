# Role, Model, Skill, MCP, and Research Policy

Use this reference when designing the project team and generated files.

## Team Sizing

Default to the main agent only. Use subagents only when at least one condition is true:

- work is naturally parallel
- the codebase area is unfamiliar or large
- implementation and verification should be separated
- independent review is valuable
- external docs/tool research should be isolated
- multiple independent surfaces are involved, such as frontend, backend, tests, infra, or platform APIs

Defaults:

- max depth: 1
- max open threads: 4 to 6
- subagent outputs: concise summary, file paths, risks, evidence, and next action

## Model Budget Policy

Generated Codex custom agents must set model and reasoning explicitly instead of relying on parent inheritance.

| Role Type | Default Model | Reasoning | Sandbox | Use For |
|---|---|---|---|---|
| Main orchestrator | `gpt-5.5` | medium or high | current session | planning, user intent, integration, final judgment |
| Explorer | `gpt-5.4-mini` | medium | read-only | cheap mapping, file discovery, impact scan |
| Complex explorer | `gpt-5.4` | medium | read-only | large repo tracing or subtle architecture mapping |
| Implementer | `gpt-5.4` | medium | workspace-write | normal code changes, refactors, test updates |
| Complex implementer | `gpt-5.4` | high | workspace-write | risky architecture, concurrency, security-sensitive, data, build, deploy |
| Tester | `gpt-5.4-mini` | medium | workspace-write | run checks, summarize failures, simple diagnosis |
| Debugger | `gpt-5.4` | high | workspace-write | hard bugs, flakes, runtime behavior, unclear failures |
| Reviewer | `gpt-5.4` | high | read-only | correctness, regressions, maintainability, tests, security-sensitive review |
| Docs researcher | `gpt-5.4-mini` | medium | read-only | official docs lookup and concise source-backed summary |
| PM or issue slicer | `gpt-5.4-mini` | medium | read-only | issue breakdown, acceptance criteria, risk list |
| Release manager | `gpt-5.4-mini` | medium | read-only or workspace-write | changelog, release checklist, PR hygiene |
| Security reviewer | `gpt-5.4` | high | read-only | threat modeling, auth, data risk, exploitability review |

If a named model is unavailable, use the closest available fallback and state the fallback in the draft.

## Domain-Specific Personas

Do not create generic roles unless evidence is too thin. Derive personas from:

- language and framework
- product/domain clues from README and docs
- architecture and runtime
- platform constraints
- test/build/deploy workflow
- existing conventions
- available skills and MCPs

Examples:

- Apple repo: `Senior Apple Platform Engineer` specializing in Swift, SwiftUI, UIKit/AppKit, Xcode, accessibility, concurrency, and HIG-aligned implementation.
- macOS repo: `Senior macOS App Engineer` specializing in SwiftUI/AppKit interop, windowing, signing, packaging, and local-first Xcode workflows.
- Web repo: `Senior Product Web Engineer` specializing in the detected stack, routing, state, API boundaries, accessibility, tests, and deploy surface.
- ML repo: `ML Systems Engineer` specializing in model pipelines, evals, data contracts, reproducibility, and runtime constraints.
- CLI/tooling repo: `Senior Tooling Engineer` specializing in command UX, integration tests, packaging, config, and release flow.

For every role, define:

| Field | Requirement |
|---|---|
| Persona | Specific senior role, not `developer` |
| Specialty | What makes this role useful for this repo |
| Thinking style | How the agent approaches work |
| Boundaries | What it must not do |
| Trigger | When the main agent should use it |
| Skills | Available skills it should always or conditionally use |
| MCPs/tools | Available MCPs/tools it may use |
| Model policy | Model, reasoning, and sandbox |
| Evidence | File/config/docs evidence that justifies the role |

## Skill Assignment Policy

Inventory all observable skills before assigning them. Assign only skills that were observed.

For each role, produce:

| Agent | Always-Use Skills | Conditional Skills | MCPs/Tools | Disabled/Avoid | Reason |
|---|---|---|---|---|---|

Rules:

1. Prefer conditional skill invocation over always-use.
2. Always-use is allowed only for workflow-defining skills and only when available and approved.
3. For behavior-changing implementation, assign `tdd` as always-use when available unless the repo evidence says otherwise.
4. For debugging, assign a debugging skill such as `diagnose` or `systematic-debugging` when available.
5. For Apple work, assign Apple/Swift skills conditionally, such as iOS HIG, SwiftUI, Swift concurrency, Swift testing, Xcode, or Apple docs skills when observed.
6. For web UI work, assign browser, Playwright, design, accessibility, framework, or deployment skills only when observed and relevant.
7. Reviewers should be read-only and should not use implementation skills unless the review task explicitly asks for a fix.
8. Implementers should not get broad external-system tools unless needed.
9. Docs researchers should get docs/search MCPs and no write access.
10. If a useful skill is missing, list it as `recommended but unavailable`.

Generated custom-agent instructions should include explicit skill rules, for example:

```text
For behavior-changing implementation, use the `tdd` skill when available before editing.
For SwiftUI changes, use the `swiftui-pro` skill when available.
For Swift concurrency changes, use the `swift-concurrency-expert` skill when available.
For unclear failures, use the `diagnose` skill when available before proposing fixes.
If a required skill is unavailable, report the fallback approach.
```

## MCP and Tool Assignment Policy

Assign MCPs narrowly.

- Explorers: file/search tools, read-only docs tools when needed
- Implementers: repo file tools and build/test tools needed for the task
- Testers: build/test tools, simulator/browser tools only when relevant
- Reviewers: read-only file/search/diff tools
- Docs researchers: official docs, Context7, Apple docs, web search, or framework docs tools when observed
- Release managers: GitHub or issue tracker tools only when needed and authenticated

Do not assign an MCP that is not observed in the inventory. Do not include secrets or local absolute credential paths in generated files.

## Research Gate

Before implementation, debugging, refactoring, or review, decide whether external research is needed.

Use existing repo evidence first:

- approved plan, PRD, or issue
- failing test output or stack trace
- README/docs and architecture notes
- CI config and package versions
- existing project skill/profile files

If a clear approved plan exists and the change is straightforward, do not do broad research. Do a targeted check only when the work touches version-sensitive APIs, security, concurrency, data migrations, deployment, build systems, platform APIs, or unfamiliar framework behavior.

If no plan exists, or the task is ambiguous, risky, unfamiliar, or failure-driven, perform targeted research before editing.

Good research questions:

- What is the official recommended pattern for this framework/version?
- What are common causes of this exact error?
- What changed in this library/framework version?
- What are current testing/debugging strategies for this failure type?
- What platform constraints apply to this API or deployment path?

Preferred sources:

1. Official docs
2. Project/framework migration guides
3. Maintainer docs or release notes
4. Source repository issues/discussions when official docs are insufficient
5. High-quality engineering posts only as secondary context

Avoid:

- broad best-practices searches without a concrete question
- old answers that are not version-matched
- copying patterns that conflict with repo conventions
- researching instead of reading local code

Summarize used research as:

| Question | Source | Finding | How it changes the plan |
|---|---|---|---|

## Work Start Policy

| Task Type | Required First Step |
|---|---|
| Approved plan exists | Read plan, verify touched files, do targeted research only if needed |
| No plan and non-trivial change | Draft plan from repo evidence, research uncertain parts, then proceed according to user scope |
| Bug/debugging | Reproduce or collect failure evidence, inspect local path, research exact error/pattern if local evidence is insufficient |
| Framework/API change | Check official docs for current version before editing |
| Security/concurrency/data/build/deploy | Use high-reasoning role and targeted official-doc research |
| Simple edit | Main agent only, no web unless uncertainty appears |

## Generated Project Skill Requirements

The repo-local project skill must include:

- repo identity
- architecture summary
- setup/build/test commands with evidence
- done criteria
- local conventions
- when to use subagents
- role roster
- model/reasoning/sandbox assignments
- skill/MCP assignments
- research gate
- validation checklist
- common gotchas
- paths to `.agents/project-profile/` references

Keep it concise. Put long evidence in `.agents/project-profile/evidence.md`.

## Generated Codex Agent TOML Requirements

Each `.codex/agents/*.toml` file must include:

```toml
name = "<repo>_<role>"
description = "..."
model = "..."
model_reasoning_effort = "..."
sandbox_mode = "read-only"
developer_instructions = """
...
"""
```

Use `workspace-write` only for implementation or testing agents that need it.

Recommended optional field:

```toml
nickname_candidates = ["...", "...", "..."]
```

Generated instructions must include:

- domain-specific persona
- trigger and boundaries
- required first step
- allowed skills and conditional skill rules
- allowed MCPs/tools
- research gate
- output format
- evidence requirements
