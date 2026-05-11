# SwiftPM Workflow Proposal v1

Inferred mode: `bootstrap`
Reason: the target repo is a clean SwiftPM-only Apple package with `Package.swift` as the authoritative workflow surface and no existing managed build/test/verify contract.

No files will be written until you approve this proposal.

## Repo Summary

- Repo: `ExamplePackage`
- Project family: `swiftpm_apple`
  - confidence: `high`
  - source: `Package.swift`, `Sources/`, package docs
- Template type: `swift_package`
  - confidence: `high`
  - source: `Package.swift`
- Project system: `swiftpm`
  - confidence: `high`
  - source: `Package.swift`; no `.xcodeproj`, `.xcworkspace`, Tuist, or XcodeGen surface detected
- Workflow state: `missing`
  - confidence: `high`
  - source: no managed `AGENTS.md` workflow block and no canonical script surface
- Primary workflow surface: `Package.swift`
  - confidence: `high`
  - source: package root
- Primary workflow unit: `whole_package`
  - confidence: `medium`
  - source: no product-specific docs, scripts, or CI detected
- SwiftPM command driver: `swift_cli`
  - confidence: `high`
  - source: host-buildable package evidence and no stronger driver detected
- Test stack: `swift_testing`
  - confidence: `medium`
  - source: `Tests/` package test target
- Top risk flags:
  - `missing_core_entrypoints`

`Package.swift` appears to be the authoritative workflow surface. Routine commands should use `swift build` and `swift test`; no Xcode scheme is required.

## Core Changes

### 1. Patch `AGENTS.md`

- File: `AGENTS.md`
- Action: `patch`
- Rationale: add one bounded managed workflow block that identifies `Package.swift` as the package-first workflow surface and points routine work at canonical entrypoints

### 2. Add managed shell helper

- File: `scripts/common.sh`
- Action: `create`
- Rationale: shared helper for repo-root detection, logging, and command checks

### 3. Add canonical build entrypoint

- File: `scripts/build.sh`
- Action: `create`
- Rationale: define one package-first build surface around `swift build`
- Intended command:
  - `run_logged "swift build" swift build`

### 4. Add canonical test entrypoint

- File: `scripts/test.sh`
- Action: `create`
- Rationale: define one routine package test surface around `swift test`
- Intended command:
  - `run_logged "swift test" swift test`

### 5. Add canonical fast verification

- File: `scripts/verify-fast.sh`
- Action: `create`
- Rationale: provide one cheap verification command for routine work
- Intended direction:
  - run `scripts/build.sh`
  - run `scripts/test.sh`

### 6. Add canonical deep verification

- File: `scripts/verify-deep.sh`
- Action: `create`
- Rationale: provide a merge-grade package verification entrypoint without inventing app-specific checks
- Intended direction:
  - run `scripts/build.sh`
  - run `scripts/test.sh`
  - add formatter/linter checks only when repo-local tooling is established

### 7. Add repo-local bootstrap helper

- File: `scripts/bootstrap-dev.sh`
- Action: `create`
- Rationale: make the managed contract discoverable and point humans/agents back to workflow audit/refresh

## Optional Generated Extensions

- None.

`test-ui.sh` is skipped because this is a SwiftPM-only package without UI-test tooling.
`generate-project.sh` is skipped because this repo has no generated Xcode project workflow.

## Recommendations Only

### 1. Product-specific workflow validation

- Rationale: the whole package is the safest default, but a future refresh can narrow `primary_workflow_unit` if docs or CI establish one primary product.

### 2. CI alignment follow-up

- Rationale: once canonical local commands exist, CI can wrap `scripts/verify-fast.sh` or `scripts/verify-deep.sh`.

## Questions

- None required before proposal approval.

## Approval Reminder

No files will be written until you approve this proposal.
