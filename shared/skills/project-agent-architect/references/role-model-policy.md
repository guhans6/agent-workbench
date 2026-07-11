# Role, Model, Skill, MCP, and Research Policy

Use this reference when designing the project team and generated files.

## Team Sizing

If no repo-local project team exists, default to the main agent for the architect setup and draft.

If a repo-local project team exists, default to main-agent orchestration plus the cheapest suitable worker for non-trivial work. The main agent should not do all implementation, research, testing, or exploration itself when a suitable project worker exists.

Use project subagents when at least one condition is true:

- work is naturally parallel
- the codebase area is unfamiliar or large
- implementation and verification should be separated
- independent review is valuable
- external docs/tool research should be isolated
- multiple independent surfaces are involved, such as frontend, backend, tests, infra, or platform APIs
- the user explicitly says to use the team
- the task has an approved plan and needs implementation

Defaults:

- max depth: 1
- max open threads: 4 to 6
- subagent outputs: concise summary, file paths, risks, evidence, and next action

## Delegation Policy

The main agent is the orchestrator and integrator, not the default worker. It should define scope, choose the smallest useful worker set, delegate scoped work to cheaper subagents, integrate returned evidence, make final decisions, and report to the user.

Direct main-agent execution is allowed only for:

- tiny one-file edits, typo fixes, or small documentation/catalog wording changes
- sensitive integration decisions where preserving full context is more valuable than delegation
- secret-sensitive tasks where copying context to a worker is risky
- cases where no suitable project subagent exists or subagent spawning is unavailable
- explicit user instruction to avoid subagents

Delegate by default when:

- the task touches multiple files or an unfamiliar area
- an approved plan exists and needs implementation
- targeted docs/API research is needed
- validation or failure triage is needed
- implementation and verification should be separated
- the user says to use the team

| Work Type | Default Worker | Reasoning | Sandbox | Rule |
|---|---|---|---|---|
| Bounded repository discovery | scout | medium | read-only | Start here for clear file, symbol, manifest, dependency, test, or configuration inventory. |
| Analytical exploration | explorer | medium | read-only | Use when findings require subsystem interpretation, cross-component tracing, or impact analysis. |
| Architectural investigation | investigator | medium | read-only | Escalation only for conflicting evidence, competing hypotheses, or architecture and migration tradeoffs. |
| Focused implementation | implementer | medium | workspace-write | Spawn for most non-trivial approved implementation. |
| Simple mechanical edit | main or small worker | medium | workspace-write | Main may do it only when delegation costs more than the work. |
| Test running or failure summary | tester | medium | workspace-write | Spawn when validation is needed. |
| Targeted docs/API research | docs researcher | high | read-only | Spawn for version-sensitive, unfamiliar, or API-specific questions. |
| Issue slicing or acceptance criteria | PM or issue slicer | high | read-only | Spawn for PRD/plan breakdowns and acceptance criteria. |
| Hard debugging | debugger | high | workspace-write | Escalation only; counts against high-reasoning budget. |
| Risky review, security, concurrency, or architecture | reviewer or specialist | high | read-only | Escalation only; counts against high-reasoning budget. |
| Final tradeoff and user report | main agent | current | current session | Do not delegate final judgment. |

## High-Reasoning Budget Policy

High-reasoning subagents are expensive. Treat them as an escalation, not a default worker pool.

Default per user task:

- high-reasoning subagent budget: 1
- high-reasoning retry budget: 0
- max concurrent high-reasoning subagents: 1
- max sequential high-reasoning subagents without user approval: 1

The main orchestrator may use one high-reasoning subagent when the task is clearly risky, ambiguous, security-sensitive, concurrency-heavy, architecture-heavy, or blocked after normal exploration.

After one high-reasoning subagent returns, the main orchestrator must integrate the result itself or use medium-reasoning workers for follow-up. Do not automatically spawn another high-reasoning implementer, reviewer, debugger, or tester.

If another high-reasoning pass appears necessary, stop and report to the user:

- what was already tried
- why medium-reasoning work is insufficient
- what the next high-reasoning agent would do
- expected cost/latency tradeoff
- the exact approval needed

Allowed without extra approval:

- one high-reasoning reviewer for a risky completed diff
- one high-reasoning debugger for a hard unresolved failure
- one high-reasoning security reviewer for security-sensitive code

Not allowed without explicit user approval:

- high-reasoning implementer followed by high-reasoning reviewer for the same small task
- repeated high-reasoning debuggers after each failed attempt
- parallel high-reasoning reviewers unless the user asks for a big audit
- upgrading every role to high because the task feels important

Generated project skills and Codex agent instructions must include this budget rule. Generated project-team workflows should say: "Use at most one high-reasoning subagent per user task by default; if more high-reasoning work is needed, report back and ask before spawning it."

## Current Model Policy

This policy is parent-model neutral. The main orchestrator is the currently invoking agent/session, not a hardcoded model identity. Any capable main agent may use this skill, draft project teams, and orchestrate subagents under the same evidence, budget, and approval rules.

Use the GPT-5.6 family for newly generated subagents. Sol handles complex, open-ended, high-value, or high-risk work; Terra handles everyday implementation, analytical exploration, and source-backed synthesis; Luna handles clear, repeatable, structured work.

Changing this central policy never updates an existing generated team. Generated agents pin exact model strings. A refresh must inventory those strings, show every current and proposed assignment, and obtain approval before changing any model or reasoning effort.

| Role Type | Model | Reasoning | Sandbox | Use For |
|---|---|---|---|---|
| Main orchestrator | current invoking session | current | current session | planning, user intent, integration, final judgment |
| Repository scout | `gpt-5.6-luna` | medium | read-only | locate files, symbols, tests, manifests, dependencies, and configurations; return bounded inventories or structured summaries |
| Analytical explorer | `gpt-5.6-terra` | medium | read-only | understand unfamiliar subsystems, trace behavior across components, interpret conventions, and assess impact |
| Architectural investigator | `gpt-5.6-sol` | medium | read-only | resolve conflicting evidence or hypotheses and analyze architecture or migration tradeoffs |
| Simple mechanical worker | `gpt-5.6-luna` | medium | workspace-write | narrow renames, formatting, catalog edits, or command-only work |
| Implementer | `gpt-5.6-terra` | medium | workspace-write | normal code changes, refactors, and test updates |
| Complex implementer | `gpt-5.6-sol` | high | workspace-write | risky architecture, concurrency, security-sensitive, data, build, or deploy changes |
| Tester | `gpt-5.6-luna` | medium | workspace-write | run checks, summarize failures, and perform simple diagnosis |
| Debugger | `gpt-5.6-sol` | high | workspace-write | hard bugs, flakes, runtime behavior, and unclear failures |
| Reviewer | `gpt-5.6-sol` | high | read-only | correctness, regressions, maintainability, tests, and security-sensitive review |
| Docs researcher | `gpt-5.6-terra` | high | read-only | official docs lookup and source-backed synthesis |
| PM or issue slicer | `gpt-5.6-terra` | high | read-only | issue breakdown, acceptance criteria, and risk lists |
| Release manager | `gpt-5.6-luna` | medium | read-only or workspace-write | changelog, release checklist, and PR hygiene |
| Security reviewer | `gpt-5.6-sol` | high | read-only | threat modeling, auth, data risk, and exploitability review |

Within exploration, start with the Luna scout. The main orchestrator evaluates its evidence, uses Terra when interpretation is needed, and uses Sol only for unresolved ambiguity or architectural judgment. Outside exploration, use Sol for the explicitly listed high-risk roles. When repo evidence justifies a reusable exploration lane, generate both the Luna scout and Terra explorer so this routing is available; an architectural investigator remains escalation-only unless that work recurs.

Generated Codex custom agents must set model and reasoning explicitly instead of relying on parent inheritance. Describe the main role by domain responsibility, such as "Senior Apple Platform Engineer plus product-minded technical lead," never by a required parent model.

Model family and reasoning effort are independent. Every high-reasoning role counts against the single high-reasoning budget. Use medium reasoning for the architectural investigator by default and raise it to high only as an explicit escalation under that budget. Do not assign `xhigh`, `max`, or `ultra` by default; propose them separately and obtain explicit approval. Automatic delegation associated with `ultra` must not bypass the skill's team-depth, concurrency, or high-reasoning limits.

Before drafting assignments, verify that each named model is observable in the current environment. If a model is unavailable, do not silently choose the closest model. Mark the assignment `unknown`, propose a specific observed fallback in the draft, and wait for approval. An older model such as `gpt-5.4-mini` may be proposed as a fallback when it is observed and justified, but it is not part of the current default roster.

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

Reviewer output must include more than findings. After listing concrete issues, reviewers must also recommend checks to run, files or behaviors to inspect during fixes, and post-fix review areas that could catch regressions.

Generated custom-agent instructions should include explicit skill rules, for example:

```text
For behavior-changing implementation, use the `tdd` skill when available before editing.
For SwiftUI changes, use the `swiftui-pro` skill when available.
For Swift concurrency changes, use the `swift-concurrency-expert` skill when available.
For unclear failures, use the `diagnose` skill when available before proposing fixes.
If a required skill is unavailable, report the fallback approach.
```

## Refresh and Reassignment Policy

Use this policy when the user installed new skills, MCPs, custom agents, or local tools and wants an existing project team updated.

Refresh starts with a delta inventory:

| Surface | Name | Previous State | Current State | Change | Evidence |
|---|---|---|---|---|---|

Every refresh must produce a separate model-assignment delta before proposing file edits:

| Agent | Current Model | Current Reasoning | Proposed Model | Proposed Reasoning | Reason | Files To Patch |
|---|---|---|---|---|---|---|

If no model or reasoning assignment would change, state `No model-assignment changes proposed` instead of omitting this section. The refresh still stops for approval before writing files.

Compare current inventory against:

- existing project-team skill role roster
- existing Codex custom-agent TOML files
- existing `.agents/project-profile/agent-roster.md`
- existing `.agents/project-profile/evidence.md`
- existing `AGENTS.md` guidance

Decision rules:

1. Add a new skill to an existing role when it strengthens that role's current responsibility.
2. Add a new MCP to an existing role only when that role needs that external surface and auth/status evidence supports it.
3. Prefer conditional assignment for new skills/MCPs until repeated use proves they are workflow-defining.
4. Promote a skill to always-use only when it defines the role workflow, such as `tdd` for behavior-changing implementers or a debugging loop for debugger roles.
5. Create a new role only when the new capability introduces a distinct responsibility that existing roles should not own.
6. Do not create roles for every installed skill. Capability inventory is not a team roster.
7. Remove or mark assignments unavailable only when the current inventory shows the surface is missing or disabled.
8. Keep manual repo-specific edits. Patch the smallest section needed.
9. If a new skill/MCP is useful but risky, unauthenticated, or write-capable, recommend it but require approval before assignment.
10. If the new surface does not add value to the repo's domain or workflow, document `no role change recommended`.
11. Preserve all current model and reasoning assignments during unrelated skill, MCP, or instruction refreshes.
12. Migrate assignments to the current model policy only after an explicit user request and approved model-assignment delta.
13. Apply no model-assignment change until the user approves the separate delta.

Refresh recommendations should use:

| Recommendation | Apply To | Reason | Risk | Files To Patch |
|---|---|---|---|---|

Examples:

- New `swift-testing-expert` in an Apple repo: add as conditional skill for tester and reviewer.
- New `context7` MCP in a web repo: add to docs researcher, not implementer, unless implementation requires API examples.
- New deploy skill in a non-deployed library repo: record as available but do not assign.
- New security scanner skill in an auth-heavy repo: add conditional use to reviewer or create `security_reviewer` only if security review is a recurring workflow.

## MCP and Tool Assignment Policy

Assign MCPs narrowly.

- Explorers: file/search tools, read-only docs tools when needed
- Implementers: repo file tools and build/test tools needed for the task
- Testers: build/test tools, simulator/browser tools only when relevant
- Reviewers: read-only file/search/diff tools
- Docs researchers: official docs, Context7, Apple docs, web search, or framework docs tools when observed; use the current model policy's docs-researcher assignment
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
| Approved plan exists | Read plan, verify touched files, delegate implementation to the cheapest suitable implementer unless the work is tiny or crucial, and do targeted research only if needed |
| No plan and non-trivial change | Draft plan from repo evidence, delegate research/exploration for uncertain parts, then proceed according to user scope |
| Bug/debugging | Reproduce or collect failure evidence, delegate failure triage or exact-error research when useful, then inspect local path before fixes |
| Framework/API change | Check official docs for current version before editing |
| Security/concurrency/data/build/deploy | Use at most one high-reasoning specialist by default plus targeted official-doc research |
| Simple edit | Main agent only, no web unless uncertainty appears |

For any task that would use high reasoning, first check whether the single high-reasoning budget has already been spent. If it has, stop and ask before spawning another high-reasoning subagent.

## Generated Project Skill Requirements

The repo-local project skill must include:

- repo identity
- architecture summary
- setup/build/test commands with evidence
- done criteria
- local conventions
- when to use subagents
- delegation defaults and when the main agent may work directly
- role roster
- model-selection rationale and exact pinned model assignments
- model/reasoning/sandbox assignments
- high-reasoning budget and stop/report rule
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
- high-reasoning budget rule when the role uses or requests high reasoning
- allowed skills and conditional skill rules
- allowed MCPs/tools
- research gate
- output format
- evidence requirements
- reviewer follow-up checks and post-fix inspection areas
