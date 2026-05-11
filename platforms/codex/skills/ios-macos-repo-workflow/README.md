# ios-macos-repo-workflow

## Overview

`ios-macos-repo-workflow` is a reusable workflow/template for Xcode-first iOS/macOS repositories and SwiftPM-only Apple codebases that you want to develop with Codex or other coding agents.

Its job is simple:

- give the repo a small, explicit local command surface
- make build/test/verify entrypoints easy for humans and agents to find
- keep workflow decisions documented in-repo
- reduce repeated prompt setup and workflow ambiguity

This repo is intentionally narrow. It is not a build system, CI framework, or repo takeover tool.

## What this repo provides

| Item | What it provides | Why it exists |
| --- | --- | --- |
| `SKILL.md` | The Codex-facing workflow contract | Tells an agent how to inspect, propose, and safely write workflow files |
| `references/profile-schema.md` | The repo profiling rules | Keeps inspection structured and prevents vague guesses |
| `references/proposal-format.md` | The output/proposal rules | Forces proposal-before-write and keeps changes easy to review |
| `templates/agents/workflow-block.md` | Managed `AGENTS.md` block template | Gives each target repo a bounded workflow section instead of ad hoc instructions |
| `templates/scripts/*.sh` | Canonical command templates | Standardizes build/test/verify/bootstrap entrypoints |
| `templates/hooks/pre-commit` | Optional inactive hook template | Lets you add lightweight local guardrails without auto-installing hooks |
| Optional Graphify support | Context graph refresh guidance and script template | Helps agents inspect relationships without rereading large parts of the repo |
| Validation examples | Real proposals/audits from tested repos | Shows how the workflow behaves on actual Apple app repos |

## When to use it

Use this workflow when a repo is:

- Xcode-first
- SwiftPM-only and Apple-platform focused
- an iOS app, macOS app, or similar Apple app repo
- unclear about the right build/test/verify commands
- used by both humans and coding agents
- accumulating drift between docs, scripts, and actual project truth

Do not use it as-is when a repo is:

- not Apple-platform focused
- already governed by a stronger workflow system you do not want to disturb
- too ambiguous to identify a primary workflow surface safely

## Quick start

If you want to use this workflow on a target repo with Codex:

```text
Use ios-macos-repo-workflow in audit mode for /path/to/repo
```

Then move to:

```text
Use ios-macos-repo-workflow in bootstrap mode for /path/to/repo
```

or:

```text
Use ios-macos-repo-workflow in refresh mode for /path/to/repo
```

Recommended order:

1. Run `audit` first when the repo is active, unfamiliar, dirty, or has workflow ambiguity.
2. Use `bootstrap` for a clean repo that does not already have a managed workflow contract.
3. Use `refresh` after the repo already has managed workflow files and needs a careful update.

## How to use in a new iOS/macOS project

For a new project, the best use is an early `bootstrap`.

Typical flow:

1. Create the Xcode project first.
2. Add your initial `AGENTS.md` in the target repo if you already use repo-local agent rules.
3. Ask Codex to run the workflow in `bootstrap` mode.
4. Review the proposal before any write.
5. Approve the write only after the proposed build/test/verify surface matches the repo.

What you should expect in the target repo after the write:

- a managed workflow block in the target repo's `AGENTS.md`
- a canonical script surface in the target repo's `script/` or `scripts/`
- optional templates only when justified

Why this helps early:

- agents stop guessing which command to run
- project setup becomes repeatable
- later CI can wrap the same local commands instead of inventing different ones

## How to use in a SwiftPM-only codebase

For a package-first repo, use the workflow when `Package.swift` is the real source of build/test truth and there is no authoritative Xcode project, workspace, Tuist manifest, or XcodeGen manifest.

Typical flow:

1. Keep `Package.swift` as the primary workflow surface.
2. Ask Codex to run the workflow in `audit` or `bootstrap` mode.
3. Review whether the package should be treated as whole-package, product-specific, or target-specific.
4. Approve the write only after the proposed scripts match the package's real command surface.

What you should expect in the target repo after the write:

- a managed workflow block in the target repo's `AGENTS.md`
- a canonical script surface in the target repo's `script/` or `scripts/`
- `build.sh` wrapping `swift build`
- `test.sh` wrapping `swift test` when real package tests exist
- `verify-fast.sh` using package build plus routine tests when available

SwiftPM-only support does not imply generated Xcode project support, UI test support, or CI migration. Those stay explicit repo decisions.

## How to use in an existing project

For an existing repo, start with `audit`.

Use `audit` when:

- the repo already has scripts or workflow docs
- the checkout is dirty
- there are worktrees or multiple workflow surfaces
- you are not sure what the real build/test truth is

Use `refresh` only after:

- the primary repo surface is clear
- the managed ownership boundary is clear
- you agree with the proposal

Why this matters:

- existing repos usually have muscle memory and human-authored workflow truth
- this workflow is designed to preserve strong existing signals, not bulldoze them

## What each script does

These scripts are templates. They are rendered into a target repo and become that repo's local workflow contract.

| Script | What it does | Why it exists | When to run or modify it |
| --- | --- | --- | --- |
| `templates/scripts/common.sh` | Shared shell helper functions | Prevents duplicated repo-root, logging, and command-check logic | Modify only when the shared shell contract itself needs to change |
| `templates/scripts/build.sh` | Canonical build entrypoint | Gives the repo one obvious build command | Run for routine local builds; modify when the real build surface changes |
| `templates/scripts/test.sh` | Canonical routine test entrypoint | Makes the test surface explicit, even when the repo has no tests yet | Run when routine tests exist; keep honest if the repo has `test_stack: none` |
| `templates/scripts/verify-fast.sh` | Cheap routine verification | Gives one low-cost confidence check for humans and agents | Run before small changes, commits, or quick reviews |
| `templates/scripts/verify-deep.sh` | Broader verification entrypoint | Separates cheap checks from slower or wider checks | Run before merges or larger changes |
| `templates/scripts/bootstrap-dev.sh` | Local workflow discovery helper | Reminds contributors what the canonical commands are | Run when onboarding or checking the managed workflow shape |
| `templates/scripts/test-ui.sh` | Optional UI test entrypoint | Keeps UI validation explicit and separate from routine checks | Add only when the repo has a real UI test surface |
| `templates/scripts/generate-project.sh` | Optional generated-project entrypoint | Supports Tuist-first or existing XcodeGen repos without installing tools | Add when project generation is part of normal workflow truth |
| `templates/scripts/graphify-refresh.sh` | Optional context graph refresh entrypoint | Keeps Graphify output fresh for agent architecture discovery | Run after meaningful structural changes, not during normal build/test verification |

## What each hook/config/template does

| Item | What it does | Why it exists | When to use or modify it |
| --- | --- | --- | --- |
| `templates/agents/workflow-block.md` | Managed `AGENTS.md` workflow block template for the target repo | Keeps workflow guidance bounded and patchable | Use whenever the target repo has `AGENTS.md`; modify only if the managed contract itself changes |
| `templates/hooks/pre-commit` | Inactive pre-commit hook wrapper | Lets a repo opt into local verification without hidden installation | Use only when explicitly requested; render path placeholders first, install manually, then `chmod +x` |
| `references/profile-schema.md` | Inspection schema | Forces consistent repo profiling | Modify when the workflow contract needs a new stable field or rule |
| `references/proposal-format.md` | Proposal schema | Keeps outputs predictable and reviewable | Modify when proposal expectations change across all repos |
| `SKILL.md` | Agent execution contract | Defines workflow behavior for Codex | Modify when the workflow rules themselves need to change |

## Tuist and XcodeGen

This workflow prefers Tuist for new clean generated-project Apple app repos when you intentionally want project generation.
It preserves XcodeGen when a repo already uses `project.yml` or `project.yaml`.

| Tool | When to use | Why |
| --- | --- | --- |
| Tuist | New clean repo where generated projects are part of the plan | Stronger Apple-project platform, Swift manifests, and room for cache/selective-test features later |
| XcodeGen | Existing repo already using XcodeGen | Lower migration risk and simple YAML/JSON project specs |
| Manual `.xcodeproj` | Small app repo where Xcode project churn is not a problem | Lowest learning curve and no generator dependency |

This repo does not install Tuist, install XcodeGen, or migrate `.xcodeproj` files automatically.
Migration should stay proposal-first because it changes project ownership, onboarding steps, and rollback behavior.

## SwiftPM-only packages

SwiftPM-only repos are package-first when `Package.swift` is authoritative and no stronger Xcode surface exists.

| Situation | What to do | Why |
| --- | --- | --- |
| Single package product or clear package docs | Use `primary_workflow_unit` for that product or `whole_package` | Avoids forcing Xcode scheme vocabulary onto packages |
| Package has real test targets | Render `test.sh` around `swift test` | Keeps routine package tests discoverable |
| Package has no tests yet | Keep `test.sh` honest as a no-test placeholder | Avoids false confidence |
| Multiple products with no primary signal | Mark `ambiguous_package_product` | Prevents the workflow from choosing a product by guess |
| Platform or driver requirements are unclear | Mark `swiftpm_driver_unclear` and recommend a probe | Avoids writing commands that cannot run on the host |

## Graphify Context

Graphify is optional. Use it to reduce architecture-discovery overhead, not to replace build/test verification.

| Situation | What to do | Why |
| --- | --- | --- |
| Starting broad architecture or refactor work | Query `graphify-out/graph.json` if present | Finds related files and concepts before reading too much code |
| File relationships are unclear | Use `graphify query`, `graphify path`, or `graphify explain` | Gives agents a smaller context path through the repo |
| Architecture changed meaningfully | Run the rendered `graphify-refresh.sh` script | Keeps graph artifacts useful for later sessions |
| Routine build/test work | Do not run Graphify by default | Avoids turning context tooling into workflow friction |

Prompt examples:

```text
Use graphify first to identify related files before planning this refactor.
```

```text
If graphify-out/graph.json exists, query it before broad manual search.
```

## Caveman Token Mode

Caveman is a separate local skill for compact communication.
This workflow does not force it by default because proposals and workflow docs need to stay clear.

Use it when you want lower-token status, summaries, or repeated progress updates:

```text
Use caveman mode for status updates and summaries.
```

Use normal mode when clarity is more important:

```text
Use normal mode for proposals, docs, and irreversible actions.
```

## Recommended Codex workflow

Use this repo as a decision layer before code generation, not after.

Recommended operating sequence:

1. `audit` the target repo.
2. confirm the primary workflow surface
3. review the proposal
4. approve the managed workflow write
5. use the repo-local canonical commands for ongoing development

Practical guidance:

| Situation | Recommended mode | Reason |
| --- | --- | --- |
| Clean new Xcode app repo | `bootstrap` | Best time to establish a small command surface |
| Clean SwiftPM-only Apple package | `bootstrap` | Best time to establish `swift build` / `swift test` entrypoints |
| Existing repo with scripts/docs already present | `audit` then `refresh` | Avoids breaking existing workflow truth |
| Repo with worktree ambiguity | `audit` only | Write target is unsafe until clarified |
| Dirty active checkout | `audit` only | Avoids mixing workflow work with unrelated local edits |
| No test target yet | `bootstrap` or `refresh` with explicit no-test handling | The workflow should stay honest instead of pretending tests exist |

## Why this improves coding efficiency

This repo improves efficiency in four ways:

| Improvement | Why it matters |
| --- | --- |
| Fewer repeated prompts | Agents do not need the build/test/verify surface re-explained every session |
| Less workflow guessing | One canonical command surface beats ad hoc shell history |
| Better reviewability | Proposal-before-write makes workflow changes easier to inspect and approve |
| Better scaling across repos | The same contract can be applied repeatedly without turning into a full framework |

For Codex-assisted development, the biggest practical win is token reduction through stable repo-local conventions.

## Repo layout

| Path | Purpose |
| --- | --- |
| [README.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/README.md) | User guide |
| [SKILL.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/SKILL.md) | Agent-facing workflow contract |
| [references/profile-schema.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/references/profile-schema.md) | Inspection/profile rules |
| [references/proposal-format.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/references/proposal-format.md) | Proposal output rules |
| [templates/agents/workflow-block.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/agents/workflow-block.md) | Managed `AGENTS.md` block template |
| [templates/scripts/common.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/common.sh) | Shared shell helper |
| [templates/scripts/build.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/build.sh) | Build template |
| [templates/scripts/test.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/test.sh) | Test template |
| [templates/scripts/verify-fast.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/verify-fast.sh) | Fast verify template |
| [templates/scripts/verify-deep.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/verify-deep.sh) | Deep verify template |
| [templates/scripts/bootstrap-dev.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/bootstrap-dev.sh) | Bootstrap helper template |
| [templates/scripts/test-ui.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/test-ui.sh) | Optional UI test template |
| [templates/scripts/generate-project.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/generate-project.sh) | Optional generated-project template |
| [templates/scripts/graphify-refresh.sh](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/scripts/graphify-refresh.sh) | Optional Graphify context refresh template |
| [templates/hooks/pre-commit](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/templates/hooks/pre-commit) | Optional inactive hook template |
| [mdzen-v1-proposal.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/mdzen-v1-proposal.md) | MDZen refresh example |
| [mdzen-v1-audit.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/mdzen-v1-audit.md) | MDZen audit example |
| [dsv-v1-audit.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/dsv-v1-audit.md) | DSV audit example |
| [whisperv-v1-audit.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/whisperv-v1-audit.md) | WhisperV audit example |
| [whisperv-v1-proposal.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/whisperv-v1-proposal.md) | WhisperV bootstrap example |
| [swiftpm-v1-proposal.md](/Users/guhan/Guhan/Projects/Tools/codex/ios-macos-repo-workflow/swiftpm-v1-proposal.md) | SwiftPM-only bootstrap example |

## Maintenance and customization

Modify this repo carefully and at the right level.

| If you want to change... | Change here | Why |
| --- | --- | --- |
| How agents inspect/profile repos | `SKILL.md` and `references/profile-schema.md` | That is contract behavior, not template behavior |
| How proposals are written | `references/proposal-format.md` | Keeps proposal output consistent |
| The managed `AGENTS.md` section | `templates/agents/workflow-block.md` | Avoids repo-by-repo drift |
| Shared shell behavior | `templates/scripts/common.sh` | One helper affects many rendered scripts |
| One specific command surface | Relevant script template in `templates/scripts/` | Keeps behavior localized |
| Optional hook behavior | `templates/hooks/pre-commit` | Hooks should remain explicit and minimal |
| Generated-project policy | `SKILL.md`, `references/profile-schema.md`, and `templates/scripts/generate-project.sh` | Tuist/XcodeGen decisions affect repo ownership and onboarding |
| SwiftPM-only policy | `SKILL.md`, `references/profile-schema.md`, and `references/proposal-format.md` | Package-first repos should not inherit Xcode scheme assumptions |
| Graphify context behavior | `SKILL.md`, `references/proposal-format.md`, and `templates/scripts/graphify-refresh.sh` | Context graphs should help agents without becoming required verification |

Guidelines:

1. Keep the workflow small.
2. Preserve existing repo truth when it is stronger than the template.
3. Prefer `audit` when the write target is ambiguous.
4. Do not add automation that hides repo-specific risk.
5. Keep examples current as validation evolves.
