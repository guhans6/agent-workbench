# DSV Workflow Audit v1

Inferred mode: `audit`
Reason: the provided checkout already has workflow docs, but repo rules indicate the active implementation surface is a different worktree, so writing to the main checkout would be unsafe without surface confirmation.

## Repo Summary

- Repo: `DSV`
- Template type: `swiftui_app`
  - confidence: `medium`
  - source: top-level `DSV.xcodeproj`, `DSV/DSVApp.swift`, `DSV/ContentView.swift`
- Project system: `xcodeproj`
  - confidence: `medium`
  - source: top-level `DSV.xcodeproj`
- Workflow state: `unmanaged_existing`
  - confidence: `high`
  - source: existing `AGENTS.md` plus repo docs, but no canonical managed `script/` surface in the provided checkout
- Primary workflow surface: `unknown`
  - confidence: `low`
  - source: top-level checkout conflicts with repo guidance pointing to an active worktree
- Top risk flags:
  - `ambiguous_primary_surface`
  - `missing_core_entrypoints`

## Managed Artifact Status

- `AGENTS.md`
  - status: present but not workflow-managed
  - note: repo rules explicitly say to stop if the main checkout is not the active worktree
- Core script surface
  - status: absent in the provided checkout
- Optional extensions
  - status: absent in the provided checkout
- CI signals
  - status: no clear CI workflow surface detected

## Findings

- The provided path is not a safe bootstrap target for direct writes.
- Static inspection shows the top-level checkout looks like a simple Xcode SwiftUI app, but repo rules and docs point to a separate active worktree as the real implementation surface.
- Because of that divergence, inferring platform, test surface, and canonical build/test commands from the top-level checkout alone would be misleading.

## Recommendations

- Confirm the active implementation worktree before attempting `bootstrap` or `refresh`.
- Treat the main checkout as an `audit` target until the active surface is selected.
- Keep worktree-first repos out of automatic write flows in reduced v1 unless the write target is explicit.
