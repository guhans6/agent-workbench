# WhisperV Workflow Audit v1

Inferred mode: `audit`
Reason: `WhisperV` is an active root checkout with existing workflow docs and a real `scripts/` layout, but it does not yet have a managed build/test/verify contract and the checkout is already dirty with unrelated in-flight changes.

## Repo Summary

- Repo: `WhisperV`
- Template type: `swiftui_app`
  - confidence: `medium`
  - source: `WhisperV.xcodeproj`, app sources, status-bar app structure
- Project system: `xcodeproj`
  - confidence: `medium`
  - source: `WhisperV.xcodeproj`
- Workflow state: `unmanaged_existing`
  - confidence: `high`
  - source: existing `AGENTS.md`, `docs/tasklog`, `TESTING.md`, `PROJECT_SETUP.md`, and `scripts/whisperv-bench.sh`
- Primary workflow surface: `xcodeproj`
  - confidence: `medium`
  - source: `WhisperV.xcodeproj`, `AGENTS.md`, project context
- Existing script layout: `scripts`
  - confidence: `high`
  - source: `scripts/whisperv-bench.sh`
- Top risk flags:
  - `missing_core_entrypoints`
  - `workflow_conflict`

## Managed Artifact Status

- `AGENTS.md`
  - status: present but not workflow-managed
  - note: repo has strong local process rules and docs, but no managed workflow block
- Core script surface
  - status: absent
  - note: there is no canonical `build`, `test`, `verify-fast`, `verify-deep`, or `bootstrap-dev` surface yet
- Existing scripts
  - status: present
  - files:
    - `scripts/whisperv-bench.sh`
- Supporting workflow docs
  - status: present
  - files:
    - `TESTING.md`
    - `PROJECT_SETUP.md`
    - `docs/tasklog/*`

## Findings

- `WhisperV` is a valid audit target for reduced v1, but not a safe direct write target in the current session because the root checkout already contains unrelated local modifications.
- The repo has strong process/documentation signals but no small canonical command surface for routine build/test/verify work.
- `WhisperV` confirms that preserving existing `scripts/` layout matters. A generated hook or script contract that assumes `script/` would be wrong for this repo.

## Recommendations

- Preserve `scripts/` if this repo is later refreshed into the workflow contract.
- Treat dirty active checkouts as audit-first unless the user explicitly confirms the exact write scope.
- Validate one clean active-root repo next where direct bootstrap writes are both safe and representative.
