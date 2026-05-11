# Apple CI Bootstrap Reference

## Purpose

This skill creates or refines narrow GitHub Actions CI aligned to repo-local Apple build and test truth.
It is opinionated about keeping CI aligned with local workflow truth.
It is not a release, signing, notarization, or deployment skill.

## Inspection Order

Prefer this source order:

1. repo-local canonical scripts
2. repo docs and `AGENTS.md`
3. authoritative Xcode or SwiftPM surfaces
4. existing CI workflows and their ownership boundaries
5. secondary signals such as README examples or stale helper scripts

If these conflict, bias toward the highest trustworthy active workflow surface and explain the conflict.
In `refresh`, treat existing CI as active repo truth unless it is clearly stale, contradictory, or explicitly approved for replacement.

## Repo Shapes

### Xcode-first

Use when an authoritative `.xcodeproj` or `.xcworkspace` and real schemes drive app or test workflow truth.
Preferred CI behavior:

- fast path uses repo-local `verify-fast` or equivalent when trustworthy
- deeper path may use `xcodebuild test`, `build-for-testing`, or `test-without-building` when the repo already implies that split
- preserve project generation steps only when Tuist or XcodeGen is real workflow truth

Evidence rules:

- prefer workspace over project when the authoritative shared scheme lives in a workspace
- require shared schemes for CI
- prefer repo evidence for scheme choice: scripts, docs, existing CI, shared scheme files, or xcodebuild listings
- account for `.xctestplan` when repo truth already uses it
- stop and ask if only private or local-only schemes are visible
- stop and ask if simulator destination or SDK choice is unclear

### SwiftPM-first

Use when `Package.swift` is the real build and test surface.
Preferred CI behavior:

- fast path wraps `swift build` or repo-local fast verification
- tests use `swift test` or the repo's canonical test wrapper
- use macOS runners when Apple-platform package behavior depends on Apple SDKs or Xcode tools

Edge cases:

- pure cross-platform Swift packages may still be Apple-repo adjacent but should not be forced into Xcode-shaped CI
- executable-only packages may be build-only if no test surface exists
- plugin or macro usage may affect runner/toolchain assumptions
- if `swift test` is not the repo's real supported CI surface, do not invent it

### Mixed

Use when the repo has one primary app workflow surface and one supporting surface.
Do not flatten mixed truth into a fake single-system story.
Examples:

- app-first Xcode repo with supporting `Package.swift`
- XcodeGen-driven app repo with handwritten helper scripts

State the primary and supporting surfaces explicitly in the proposal.
Default mixed-repo rule:

- run CI against the primary workflow surface
- add supporting-surface jobs only when the repo already treats that surface as an independent validation contract
- do not add duplicate SwiftPM jobs when `Package.swift` is only supporting infrastructure for an app-first Xcode repo

## Job Design

V1 should stay small.
Preferred default:

- one workflow file
- one routine fast job
- one optional deeper job when the repo already has a meaningful deeper path

Fast job goals:

- cheap enough for routine PR signal
- buildable on the chosen runner
- mapped to repo-local `verify-fast` or equivalent

Deep job goals:

- broader confidence than fast
- slower or more expensive checks isolated from routine signal
- mapped to `verify-deep`, app tests, UI tests, or generation-aware validation only when repo truth supports it

Do not invent a deep job just because the concept sounds nice.

## GitHub Actions Standards

Prefer:

- `pull_request` plus `push` to the default branch
- `permissions: contents: read` unless a narrower CI need requires more
- workflow-level `concurrency` with stale-run cancellation
- explicit `runs-on` selection
- minimal permissions unless the workflow actually needs more
- artifact upload for `.xcresult` bundles or retained logs when test/build output would otherwise be too large or lossy
- one clear entrypoint command per job

Be careful with:

- path filters, because skipped required checks can block merges
- runner cost, especially macOS minutes
- community actions that add opaque behavior
- `pull_request_target`, because routine CI should not widen trust boundaries
- secret-dependent CI steps, because routine validation should not require secrets by default

Action policy:

- prefer official actions when needed
- pin action versions deliberately
- avoid opaque third-party setup actions unless repo truth requires them
- explain every third-party action in the proposal

## Runner Guidance

Default to GitHub-hosted macOS runners for Apple app repos because Xcode tooling and `xcodebuild` require Xcode.
If the repo is a pure Swift package and local workflow truth is host-portable, a macOS runner may still be the safer default for Apple-focused projects; explain if you intentionally choose otherwise.

Do not pin to an arbitrary runner label without reason.
Derive runner and Xcode expectations from repo evidence when possible.
Avoid arbitrary `macos-latest` use when the repo clearly depends on a known Xcode or SDK surface.
Stop and ask if the needed Xcode version, SDK, or simulator availability is uncertain.
State the runner choice and why.

## Diagnostics And Artifacts

Prefer concise logs in the live job output.
If a step produces large Xcode output, preserve useful artifacts instead of flooding CI logs.

Examples:

- upload `.xcresult` after Xcode test runs
- store generated logs under a bounded path and upload on failure or always, depending on repo needs
- keep summary text human-readable in the job output

Never claim artifact value that the workflow does not actually produce.
Default artifact policy:

- upload diagnostics on failure by default
- use always-upload only when repo truth or the proposal justifies the cost
- keep artifact names predictable
- keep retention bounded
- do not upload secrets, provisioning material, or unnecessary build products

## Optional Recommendations

These may appear in the recommendations-only section when detected or strongly justified:

- SwiftLint integration
- SwiftFormat integration
- XcodeGen or Tuist generation check
- UI test workflow
- nightly scheduled deeper verification

Do not write these by default in v1 unless repo truth already supports them and the user approved them.

## Hard Prohibitions

Never:

- add release or deploy jobs in v1
- add signing or secret-heavy distribution flows by default
- replace repo-local script truth with generic raw commands unless the local scripts are clearly untrustworthy
- assume simulator destinations or schemes that were not derived from repo evidence
- invent validation steps and call them standard
- silently rewrite multiple workflows into one when ownership is unclear
- touch release, deploy, or signing workflows in v1

Existing broad permissions are repo truth, not automatically safe defaults.
If existing CI uses broader permissions than the proposed narrow CI needs, preserve them only when required for ownership safety and flag them explicitly in the proposal for later tightening.

## Proposal Shape

Keep the proposal brief.
Recommended sections:

- summary
- detected workflow truth
- proposed workflow files
- fast path
- optional deep path
- artifact/log handling
- recommendations-only
- confidence and risks

## Source Notes

This skill should stay consistent with current GitHub Actions and Apple command-line guidance:

- GitHub Actions workflow syntax and filters
- GitHub Actions concurrency
- GitHub-hosted macOS runner availability
- Apple `xcodebuild` testing and `.xcresult` handling

If current docs conflict with repo-local truth, explain the tradeoff instead of forcing a generic best practice.
