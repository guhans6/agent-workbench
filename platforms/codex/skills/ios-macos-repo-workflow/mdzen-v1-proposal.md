# MDZen Workflow Proposal v1

Inferred mode: `refresh`
Reason: `MDZen` already has workflow artifacts (`AGENTS.md`, `script/`, CI), but they are unmanaged and internally inconsistent.

No files will be written until you approve this proposal.

## Repo Summary

- Repo: `MDZen`
- Template type: `mixed_apple_app`
  - confidence: `high`
  - source: `README.md`, `project.yml`, `Sources/MDZenApp`, AppKit-backed editor plus SwiftUI app layer
- Project system: `mixed`
  - confidence: `high`
  - source: `MDZen.xcodeproj`, `project.yml`, `Package.swift`
- Workflow state: `unmanaged_existing`
  - confidence: `high`
  - source: existing `AGENTS.md`, `script/build_and_run.sh`, `script/build_and_test.sh`, `.github/workflows/ci.yml`
- Platforms: `macos`
  - confidence: `high`
  - source: `README.md`, `project.yml`, `Package.swift`
- UI stack: `mixed`
  - confidence: `high`
  - source: `README.md`, `project.yml`
- Test stack: `xctest`
  - confidence: `high`
  - source: `project.yml`, `Tests/*`
- Primary target or scheme: `MDZen`
  - confidence: `high`
  - source: `MDZen.xcodeproj/xcshareddata/xcschemes/MDZen.xcscheme`, docs

## Observed Workflow Truth

- Existing script layout: `script/`
  - confidence: `high`
  - source: repo file tree
- Existing build/run surface:
  - `./script/build_and_run.sh`
  - builds via `swift build`, assembles a `.app` manually, and opens it
- Existing test surface:
  - `./script/build_and_test.sh`
  - runs `swift test`
- Existing CI truth:
  - `swift build --disable-sandbox`
  - `swift test --disable-sandbox`
- Existing app-first truth signals:
  - `project.yml` defines app target `MDZenApp`, test bundles, and `MDZen` scheme
  - `Package.swift` explicitly says the canonical Xcode build target is `MDZen.xcodeproj`, not the package
  - docs recommend Xcode for real app development

## Risk Flags

- `workflow_conflict`
  - current routine verification is package-first, while app intent is Xcode/XcodeGen-first
- `generated_project_detected`
  - `project.yml` exists and appears authoritative for the app project shape
- `missing_core_entrypoints`
  - repo has legacy scripts, but not a small canonical `build/test/verify-fast/verify-deep/bootstrap-dev` surface

## Core Changes

### 1. Patch `AGENTS.md`

- File: `AGENTS.md`
- Action: `patch`
- Rationale: add one bounded workflow-managed block near the top that states:
  - repo is app-first
  - `script/` is the preserved repo-local command surface
  - canonical entrypoints are:
    - `script/build.sh`
    - `script/test.sh`
    - `script/verify-fast.sh`
    - `script/verify-deep.sh`
    - `script/bootstrap-dev.sh`
  - `Package.swift` is supporting infrastructure, not sole workflow truth

### 2. Add managed shell helper

- File: `script/common.sh`
- Action: `create`
- Rationale: shared repo-root, logging, and command-check helpers for managed scripts

### 3. Add canonical build entrypoint

- File: `script/build.sh`
- Action: `create`
- Rationale: establish a stable app-first build surface
- Intended direction:
  - build the app-first target rather than relying on package-only build truth
  - keep implementation conservative in v1

### 4. Add canonical test entrypoint

- File: `script/test.sh`
- Action: `create`
- Rationale: separate routine tests from packaging/build concerns
- Intended direction:
  - use the routine non-UI test surface
  - keep UI tests out of this script

### 5. Add canonical fast verification

- File: `script/verify-fast.sh`
- Action: `create`
- Rationale: provide one cheap routine verification command
- Intended direction:
  - app-first build truth
  - routine non-UI validation
  - concise surfaced diagnostics with full logs in `.logs/`

### 6. Add canonical deep verification

- File: `script/verify-deep.sh`
- Action: `create`
- Rationale: provide a merge-grade verification entrypoint
- Intended direction:
  - build plus broader non-UI test coverage in v1
  - do not force UI tests into the core deep path yet

### 7. Add repo-local workflow helper

- File: `script/bootstrap-dev.sh`
- Action: `create`
- Rationale: make the workflow discoverable in-repo and point humans/Codex back to the global skill for audit/refresh

### 8. Preserve and mark legacy wrappers

- Files:
  - `script/build_and_run.sh`
  - `script/build_and_test.sh`
- Action: `patch`
- Rationale: preserve existing muscle memory and references, but mark them as legacy wrappers that point to the new canonical surface

## Optional Generated Extensions

### 1. UI test entrypoint

- File: `script/test-ui.sh`
- Action: `create`
- Rationale: repo has a real `MDZenUITests` target, but UI verification should stabilize outside the core surface first

### 2. Generated-project helper

- File: `script/generate-project.sh`
- Action: `create`
- Rationale: `project.yml` is an authoritative project signal; generation should be explicit support, not built into every routine command

## Recommendations Only

### 1. Probe phase after approval

- Rationale: static inspection cannot safely prove the final app-first command surface
- Follow-up probes should be limited to:
  - list or validate schemes
  - confirm the best non-UI test command
  - confirm whether app build should use `xcodebuild` directly or a repo-local wrapper

### 2. CI alignment follow-up

- Rationale: current CI is package-first; once the canonical local surface is stable, CI should be reviewed for alignment
- Not part of v1 write scope

### 3. Formatting and linting

- Rationale: no strong repo-local evidence yet that SwiftFormat or SwiftLint are established workflow truth
- Recommend as future standardization work, not initial generated scripts

## Open Questions

- None required before proposal approval.
- One likely question will remain before script implementation inside `MDZen`: whether the app-first canonical build/test commands should be driven primarily by `xcodebuild` or by a thin repo-local wrapper over XcodeGen plus Xcode.
  - Answer: Whichever is the best optimal option

## Approval Reminder

No files will be written until you approve this proposal.
