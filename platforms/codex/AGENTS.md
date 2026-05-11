# Global Agent Routing

- In Swift, iOS, macOS, Xcode, SwiftUI, UIKit, AppKit, SwiftData, or XCTest repos, prefer `swift_explorer` over `explorer` for read-only mapping.
- Use `spark_editor` only for tiny localized edits, renames, preview stubs, and small UI glue. Use `swift_worker` for normal implementation.
- Use `xcode_triager` for build, test, scheme, simulator, and log triage before escalating to `deep_debugger`.
- Use `apple_docs_researcher` when Apple API behavior, platform availability, or framework semantics are uncertain.
- Use `swift_reviewer` for read-only review of diffs, regressions, behavior changes, and missing tests.

## Commit / Issue Hygiene

- Use `publish-workflow` for normal branch, commit, push, and PR-boundary operations.
- Before committing or opening a PR, check whether the work maps to issues/PRD tasks. If yes, reference issue numbers in commits/PRs and use `Closes/Fixes/Resolves #N` in the PR body when merge should close them.
- Don't assume and commit.
