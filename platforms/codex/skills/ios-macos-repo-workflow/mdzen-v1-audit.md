# MDZen Workflow Audit v1

Inferred mode: `audit`
Reason: `MDZen` already has a managed workflow contract and canonical script surface, so the narrow v1 question is whether static inspection shows workflow drift that needs follow-up.

## Repo Summary

- Repo: `MDZen`
- Template type: `mixed_apple_app`
  - confidence: `high`
  - source: `README.md`, `project.yml`, `Sources/MDZenApp`
- Project system: `mixed`
  - confidence: `high`
  - source: `MDZen.xcodeproj`, `project.yml`, `Package.swift`
- Workflow state: `managed`
  - confidence: `high`
  - source: `AGENTS.md` managed block, `script/` managed command surface
- Primary workflow surface: `xcodeproj`
  - confidence: `medium`
  - source: `AGENTS.md`, `MDZen.xcodeproj`, `project.yml`
- Primary target or scheme: `MDZen`
  - confidence: `high`
  - source: `MDZen.xcodeproj/xcshareddata/xcschemes/MDZen.xcscheme`, managed `script/build.sh`
- Top risk flags:
  - `generated_project_detected`
  - `workflow_conflict`

## Managed Artifact Status

- `AGENTS.md`
  - status: managed block present
  - note: repo is explicitly marked app-first and points to the canonical `script/` surface
- Core script surface
  - status: present
  - files:
    - `script/build.sh`
    - `script/test.sh`
    - `script/verify-fast.sh`
    - `script/verify-deep.sh`
    - `script/bootstrap-dev.sh`
    - `script/common.sh`
- Optional extensions
  - status: present
  - files:
    - `script/test-ui.sh`
    - `script/generate-project.sh`
- Legacy wrappers
  - status: preserved
  - files:
    - `script/build_and_run.sh`
    - `script/build_and_test.sh`

## Findings

- No core workflow drift requiring a managed write was identified from static inspection.
- The repo still has deliberate mixed workflow truth:
  - app-first build and deeper verification use `xcodebuild`
  - routine tests use `swift test --disable-sandbox`
- Generated project support remains a real workflow dependency because `project.yml` is authoritative for project shape.

## Recommendations

- Re-run `audit` after changes to:
  - `project.yml`
  - `Package.swift`
  - shared schemes
  - the canonical `script/` surface
- Keep mixed Xcode/SPM handling conservative:
  - do not assume app module names and package-facing test imports stay aligned without a probe phase
- Validate the global skill on at least one more Xcode-first repo before expanding scope.
