# Global Agent Routing

- In Swift, iOS, macOS, Xcode, SwiftUI, UIKit, AppKit, SwiftData, or XCTest repos, prefer `swift_explorer` over `explorer` for read-only mapping.
- Use `spark_editor` only for tiny localized edits, renames, preview stubs, and small UI glue. Use `swift_worker` for normal implementation.
- Use `xcode_triager` for build, test, scheme, simulator, and log triage before escalating to `deep_debugger`.
- Use `apple_docs_researcher` when Apple API behavior, platform availability, or framework semantics are uncertain.
- Use `swift_reviewer` for read-only review of diffs, regressions, behavior changes, and missing tests.

## Matt Workflow Routing

- Use `ask-matt` when the workflow is unclear; use `grill-with-docs` for an idea needing clarification and `wayfinder` for an uncertain multi-session effort.
- Use `implement` for approved tickets, `tdd` at agreed public seams, and `code-review` before committing non-trivial changes.
- Use `to-spec` then `to-tickets` to turn a resolved plan into implementation work.

## Commit / Issue Hygiene

- Use `publish-workflow` for normal branch, commit, push, and PR-boundary operations.
- Before committing or opening a PR, check whether the work maps to issues/PRD tasks. If yes, reference issue numbers in commits/PRs and use `Closes/Fixes/Resolves #N` in the PR body when merge should close them.
- Don't assume and commit.

<!-- delivery-completion:start -->
## Completion

Report the user-agreed outcome against its acceptance criteria and applicable Definition of Done, with observed evidence and remaining work/next owner. Read the repo’s delivery/workflow reference before planning or reporting delivery. Distinguish implementation and local validation from installation, publication and enablement where relevant; identify the artifact/revision and target, and mark not performed, unknown or out of scope honestly. If no repo convention exists, report honestly now and offer explicit `$setup-delivery-workflow` setup when useful, without repeated offers or blocking legitimate work. Setup requires user approval before writes; never run it automatically.
<!-- delivery-completion:end -->
