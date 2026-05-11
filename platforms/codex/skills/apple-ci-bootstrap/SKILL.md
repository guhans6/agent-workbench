---
name: apple-ci-bootstrap
description: Proposes and creates narrow GitHub Actions CI for Apple-platform repositories with repo-truth-first command selection, fast/deep verification structure, and concise diagnostics. Use when bootstrapping, auditing, or refreshing CI workflows for iOS, macOS, Xcode-first, or SwiftPM Apple repos.
---

# Apple CI Bootstrap

Create or refine GitHub Actions CI for Apple-platform repositories.
This skill is CI only.
It is not release automation, signing automation, deployment, or general DevOps.

## Modes

- `bootstrap`: propose an initial CI workflow
- `refresh`: update an existing CI workflow toward repo truth
- `audit`: inspect CI drift and recommend changes without writing by default

Infer the mode from repo state, but announce it.
If CI is already present or the repo is ambiguous, prefer `audit`.

## Rules

- Inspect repo-local workflow truth first: scripts, docs, AGENTS.md, project files, and existing workflows.
- Prefer the highest trustworthy local command abstraction, not raw `xcodebuild` by reflex.
- Align CI with canonical repo-local scripts when they exist.
- If no trustworthy script surface exists, derive commands from the authoritative Xcode or SwiftPM surface and say so explicitly.
- Keep one primary fast path. Add a deeper path only when repo truth already supports it.
- Use GitHub Actions in `.github/workflows/`.
- Prefer concise diagnostics, artifact upload, and log preservation over huge inline logs.
- Use concurrency to cancel stale runs on the same branch or PR when appropriate.
- Do not install tools, rewrite repo architecture, or invent untrusted lint/format/test steps.
- Recommend optional tools only when they are already configured, documented, or strongly implied by repo structure; never auto-install them.
- Do not add release, signing, notarization, TestFlight, App Store, or deployment jobs in v1.
- Do not use `pull_request_target` for routine CI in v1.
- Do not introduce secret-dependent jobs, scheduled jobs, or manual dispatch by default. Keep those in recommendations-only unless repo truth already uses them and the user approved them.
- Do not write CI before showing a proposal and getting approval.

## Workflow

1. Inspect the repo statically first.
2. Identify the authoritative workflow surface:
   - `.xcodeproj` or `.xcworkspace`
   - `Package.swift`
   - repo-local scripts such as `script/verify-fast.sh`
   - existing `.github/workflows/*.yml`
   - generated-project manifests such as Tuist or XcodeGen
3. Determine whether the repo is:
   - Xcode-first
   - SwiftPM-first
   - mixed, with one primary surface and one supporting surface
4. Identify the routine CI path:
   - build-only
   - test-only via wrapper
   - build + unit tests
   - build + app tests
   - scripted verify only
   - build-for-testing and test-without-building split
   - fast and optional deep split
5. Propose a narrow workflow shape with:
   - trigger policy
   - runner choice
   - fast job
   - optional deep job
   - artifact/log policy
   - recommendations-only section
6. After approval, write or patch the workflow files.

When writing:

- patch existing CI when ownership is clear
- create a new workflow file when that is safer than rewriting human-authored workflows
- preserve human-authored job names, required check names, `env`, `defaults`, and existing release or deploy workflows
- do not edit release, deploy, signing, or distribution workflows in v1
- preserve existing `permissions` shape unless the proposal explicitly calls out a narrower safe change or flags an existing broad permission for follow-up
- do not rewrite multiple workflows into one unless explicitly approved
- after writing, verify that:
  - only intended workflow files changed
  - workflow YAML remains structurally valid
  - required check names and trigger intent were preserved unless explicitly approved to change
  - permissions and trust boundaries were not accidentally broadened
  - repo-available workflow validators or linters were used when present

## Default CI Shape

- Run on `pull_request` and `push` to the default branch unless repo truth says otherwise.
- Use path filters only when the repo already has a safe, stable split and the filter includes workflow-defining files such as workflow YAML, scripts, project/workspace files, package manifests, generated-project manifests, and relevant lockfiles or docs.
- Use workflow concurrency to cancel stale runs for the same PR or branch.
- Use the repo's fast verification entrypoint when it exists.
- Keep deep verification separate from the routine fast path.
- Upload `.xcresult` bundles or concise logs when Xcode-based testing runs.
- Prefer one main workflow over many fragmented workflows in v1.

## When To Stop And Ask

- primary workflow surface is ambiguous
- existing CI conflicts with local scripts or docs
- simulator destination, scheme, or test surface cannot be inferred safely
- generated-project tooling appears required but generation steps are unclear
- shared scheme, workspace/project choice, destination, or test plan cannot be derived safely
- the repo has multiple plausible CI shapes with materially different cost or signal
- a write would replace human-authored CI with unclear ownership boundaries
- existing CI ownership, required check names, or workflow boundaries would be disturbed by the write

## Output Contract

Proposal should stay compact and include:

- repo profile summary
- authoritative workflow surface
- recommended workflow files
- fast job shape
- optional deep job shape
- artifact/log handling
- confidence and risk notes

See [REFERENCE.md](REFERENCE.md) for inspection rules, workflow standards, and v1 boundaries.
