---
name: matt-informed-engineering
description: "Engineering uncertainty: use when choosing evidence for stalled progress, unproven integration, unclear module seams, or repeated agent-document failures. Applies Matt's published methods to one decision and its smallest observable next move."
---

# Matt-informed engineering

A local, source-backed advisor. `ask-matt` owns workflow routing; `writing-for-agents` owns agent-document authoring. Use this layer to explain why a method fits a concrete evidence gap. Routine known edits continue under their existing workflow.

1. **Decision.** Name the bounded decision or observed failure, the agreed outcome, and the last proven state. Done when one question gates the next increment.
2. **Evidence.** Identify the missing fact, human decision, reproducible signal, interface choice, or integration proof. Inspect available facts before requesting a human decision; reuse decisions already made. Done when the missing evidence and its effect on progress are explicit.
3. **Method.** Read the matching card below and the actual installed skill before describing its behavior or suggesting a skipped step. Load a second card only when a second evidence gap changes the move. Done when the cited published method supports the recommendation and the applicable installed workflow is identified. If unavailable, report the missing contract and offer a bounded evidence-gathering move.
4. **Move.** Recommend the smallest action that resolves the gap and a checkable completion condition. Done when another person can observe success or failure and knows which decision remains human-owned.
5. **Return.** Give the decision, missing evidence, published method with its source link, local inference (if any), next move, and done condition. Existing user scope and the active workflow govern further execution; this advice grants no new authority.

## Choose one card

| Evidence gap | Read | Consult installed authority |
| --- | --- | --- |
| Layers exist but the complete path is unproven | [Tracer bullets](references/tracer-bullets.md) | `to-tickets` or the active implementation workflow |
| Dependent decisions block a plan | [Decision frontier](references/decision-frontier.md) | `grilling`; `ask-matt` for choosing the wrapper |
| Callers or tests must know too much | [Deep modules](references/deep-modules.md) | `codebase-design` |
| A concrete behavior lacks an independent test signal | [Red → green](references/red-green.md) | `tdd` |
| Plausible bug fixes keep failing | [Diagnosis](references/diagnosis.md) | `diagnosing-bugs` |
| A diff's quality or requested outcome is uncertain | [Review](references/review.md) | `code-review` |
| An agent document repeatedly misses a branch or completion bound | [Agent documents](references/agent-documents.md) | `writing-for-agents` and its skill mechanics |

## Authority and attribution

Repository and user rules govern execution, verification scope, delivery, and publication. A user-invoked skill is a suggested invocation until the user supplies its scope; recommending it does not invoke it. Already authorized work can continue without an additional approval caused by this advisor.

Use “Matt's published method suggests…” for supported advice; label adaptations as **local inference**. When selecting a book-backed principle, identify the credited book and authors from its card. Attribute only what the linked source states. Personal preferences, private thoughts, book-reading history, and unwatched video content are outside this evidence. For disputed attribution or conflicting versions, read [Sources](references/SOURCES.md).

For bounded evaluation of discovery, source correctness, and authority, use [pilot scenarios](evals/scenarios.md). Those scenarios are local evaluation definitions, not upstream tests or evidence of host behavior.
