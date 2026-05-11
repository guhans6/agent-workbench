# WhisperV Workflow Proposal v1

Inferred mode: `bootstrap`
Reason: the clean validation checkout has strong Xcode-first workflow truth and supporting repo docs, but it does not yet have a small managed workflow contract or canonical build/test/verify entrypoint surface.

No files will be written until you approve this proposal.

## Repo Summary

- Repo: `WhisperV`
- Template type: `swiftui_app`
  - confidence: `high`
  - source: `WhisperV/WhisperVApp.swift`, status-bar SwiftUI app structure
- Project system: `xcodeproj`
  - confidence: `high`
  - source: `WhisperV.xcodeproj`
- Workflow state: `unmanaged_existing`
  - confidence: `high`
  - source: existing `AGENTS.md`, `TESTING.md`, `PROJECT_SETUP.md`, `scripts/whisperv-bench.sh`
- Platforms: `macos`
  - confidence: `high`
  - source: `AGENTS.md`, `project.pbxproj`
- UI stack: `mixed`
  - confidence: `medium`
  - source: SwiftUI app plus AppKit activation usage
- Test stack: `none`
  - confidence: `high`
  - source: no repo test target, no committed test directories, `docs/STATUS.md`
- Primary workflow surface: `xcodeproj`
  - confidence: `high`
  - source: `WhisperV.xcodeproj`, repo docs
- Existing script layout: `scripts`
  - confidence: `high`
  - source: `scripts/whisperv-bench.sh`
- Top risk flags:
  - `missing_core_entrypoints`
  - `unknown_target_or_scheme`

## Core Changes

### 1. Patch `AGENTS.md`

- File: `AGENTS.md`
- Action: `patch`
- Rationale: add one bounded managed workflow block that preserves `scripts/` as the repo-local workflow surface and points routine work at canonical entrypoints

### 2. Add managed shell helper

- File: `scripts/common.sh`
- Action: `create`
- Rationale: shared helper for repo-root detection, logging, and command checks

### 3. Add canonical build entrypoint

- File: `scripts/build.sh`
- Action: `create`
- Rationale: define one app-first build surface around `WhisperV.xcodeproj`

### 4. Add canonical test entrypoint

- File: `scripts/test.sh`
- Action: `create`
- Rationale: make the absence of routine automated tests explicit rather than pretending real coverage exists yet

### 5. Add canonical fast verification

- File: `scripts/verify-fast.sh`
- Action: `create`
- Rationale: provide one cheap build-first verification command without claiming test coverage that the repo does not yet have

### 6. Add canonical deep verification

- File: `scripts/verify-deep.sh`
- Action: `create`
- Rationale: keep a merge-grade entrypoint available even if it currently composes build-first checks and repo-specific higher-cost validation

### 7. Add repo-local bootstrap helper

- File: `scripts/bootstrap-dev.sh`
- Action: `create`
- Rationale: make the managed contract discoverable and point humans/agents back to workflow audit/refresh

## Optional Generated Extensions

### 1. Inactive pre-commit hook template

- File: `hooks/pre-commit`
- Action: `create`
- Rationale: repo has an established `scripts/` layout, so an inactive wrapper around `scripts/verify-fast.sh` is a reasonable optional extension if explicitly requested

## Recommendations Only

### 1. Add a real automated test target

- Rationale: the repo currently has `test_stack: none`, so any generated `test.sh` would be an explicit placeholder until tests exist

### 2. Probe phase after approval

- Rationale: static inspection can identify the project surface, but a probe phase should confirm the best scheme and concrete xcodebuild invocation

### 3. CI alignment follow-up

- Rationale: once canonical local commands exist, CI can be added around that command surface rather than around ad hoc documentation

## Questions

- None required before proposal approval.

## Approval Reminder

No files will be written until you approve this proposal.
