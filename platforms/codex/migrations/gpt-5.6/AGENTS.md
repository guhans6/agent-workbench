# Proposed Global Agent Routing

This is a proposed runtime replacement source. It is not live configuration.

<!-- routing:start -->
## General best-value routing

General routing first. Select `global_scout` for bounded inventory or mechanical checks, `global_worker` for normal implementation and analysis, `spark_editor_gpt56` for a tiny localized edit, `global_docs_researcher` for current documentation, `global_debugger` for difficult investigation, and `global_reviewer` for high-risk review. Every assignment is exact; an unavailable model stops routing instead of falling back. The orchestrator owns classification and workers do not self-promote. A concrete Luna failure escalates once to Terra. Terra escalates to Sol only for conflicting evidence, architectural ambiguity, repeated failure, or elevated risk. At most one Sol/high subagent runs automatically per user task.

## Matt workflow routing

Matt workflow routing. Use `implement` for approved ticket work, `tdd` at agreed public seams, and `code-review` before commit. Use `to-spec` then `to-tickets` for a grilled multi-session build; use `diagnosing-bugs` for unclear failures. Select a workflow independently of the execution profile.

## Apple exceptions

Apple exceptions second. Prefer `swift_explorer`, `swift_worker`, and `xcode_triager` for Apple repositories. Use `apple_docs_researcher` for Apple semantics, `deep_debugger` only after triage for difficult Apple investigation, and `swift_reviewer` for Apple-specific review. `gatekeeper` remains manual-only.
<!-- routing:end -->
