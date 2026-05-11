# Proposal Format

Every `bootstrap` or `refresh` proposal should stay short and use the same order.

## 1. Repo Summary

Include:

- inferred mode
- template type
- project system
- workflow state
- top risk flags

When the repo is mixed Xcode/SPM, also state in prose:

- whether the package surface appears primary or supporting
- whether module-name or test-import drift is visible or should remain `unknown` pending probes

When the repo is SwiftPM-only, also state in prose:

- whether `Package.swift` is the authoritative workflow surface
- package name, command driver, and primary workflow unit
- whether package tests are present
- whether any product, target, platform, or driver ambiguity needs a probe
- do not ask for an Xcode scheme unless `swiftpm_command_driver: xcodebuild_package`

## 2. Core Changes

List only the workflow contract changes that would be written in v1:

- managed `AGENTS.md` block
- core script surface
- shared helper

For each item:

- file path
- action: `create`, `patch`, `preserve`, `skip`
- one-line rationale

If the repo has no established automated test surface:

- say that explicitly in the proposal
- do not present `test.sh` as if it already has real coverage
- allow `verify-fast` to be build-first rather than claiming routine tests exist

For SwiftPM-only repos:

- `build.sh` should wrap `swift build` unless existing repo truth points at a stronger package driver
- `test.sh` should wrap `swift test` when package tests exist
- `verify-fast.sh` should run package build plus routine package tests when tests exist, otherwise build-only
- `verify-deep.sh` should start with package build/tests and add slower package-specific checks only when statically justified
- if `swiftpm_command_driver` is `unknown`, propose a probe phase instead of inventing commands

## 3. Optional Generated Extensions

Only include strong-fit extensions:

- `test-ui.sh`
- generated-project helper
- `graphify-refresh.sh` for optional context graph refresh
- inactive hook templates when explicitly requested

Do not include `test-ui.sh` or generated-project helpers for SwiftPM-only repos unless static evidence shows those workflows are real repo truth.

For generated-project helper proposals:

- prefer Tuist for new clean repos when generated-project adoption is requested
- preserve XcodeGen when it already exists unless migration is explicitly approved
- explain that Tuist/XcodeGen will not be installed automatically
- explain generated-file ownership and rollback expectations before any migration proposal

For Graphify proposals:

- present it as an optional agent context layer, not a build/test dependency
- recommend it before broad architecture/refactor work or when file relationships are unclear
- recommend refresh after meaningful structural changes
- do not include Graphify in normal `build`, `test`, `verify-fast`, `verify-deep`, commit, or CI paths in v1

## 4. Recommendations Only

Use for improvements that should not be written automatically:

- formatter adoption
- linter adoption
- hook activation
- CI alignment follow-up
- probe phase for unknown fields
- module-surface validation when mixed Xcode/SPM evidence suggests import-name drift
- package product or driver validation when SwiftPM-only evidence is ambiguous
- caveman/compact output for low-token status updates and summaries

## 5. Questions

Only include questions that are necessary to avoid a bad write.
Prefer one focused question over a list.

## 6. Approval Rule

End with a short reminder:

`No files will be written until you approve this proposal.`

## Audit Output

`audit` should output:

- concise repo summary
- managed artifact status
- findings only when needed
- optional recommendations

It should not present writes as already decided.
