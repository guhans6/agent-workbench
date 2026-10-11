# Sources and attribution boundaries

This advisor is locally authored for agent-workbench issue #15. It applies published methods; it is not a Matt-published skill, persona, or prediction of Matt's personal choice.

## Inspected evidence

The source research was performed on **2026-10-11**, inspecting `mattpocock/skills` at **`49dd158d1076134a641b33efb035946536778336`**. The implementation reviewed those downloaded skill texts and the written research proposal. GitHub source links in the cards pin that inspected revision. First-party AIHero pages are dated observations, not immutable source snapshots.

The [repository](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336), [pinned README](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/README.md), and [AIHero](https://www.aihero.dev/) establish the first-party source chain. The research read the cited pages' written content. It did not read the books, watch the videos, or obtain their transcripts.

Each card separates **published method**, **published attribution** where verified, and **local inference**. A linked book reference establishes the named public attribution only; it establishes neither a complete reading history nor that the whole skill derives from that book.

| Published attribution | Evidence | Applicable card |
| --- | --- | --- |
| Andrew Hunt and David Thomas, *The Pragmatic Programmer* | [Tracer Bullets](https://www.aihero.dev/tracer-bullets) explicitly credits the book | [Tracer bullets](tracer-bullets.md) |
| Frederick P. Brooks, *The Design of Design* | [5 Agent Skills I Use Every Day](https://www.aihero.dev/5-agent-skills-i-use-every-day) credits the design tree | [Decision frontier](decision-frontier.md) |
| John Ousterhout, *A Philosophy of Software Design* | [How To Make Codebases AI Agents Love](https://www.aihero.dev/how-to-make-codebases-ai-agents-love) credits the book | [Deep modules](deep-modules.md) |
| Martin Fowler, *Refactoring*, chapter 3 | [Code-review guide](https://www.aihero.dev/skills-code-review) identifies its smell baseline | [Review](review.md) |
| Kent Beck, *Extreme Programming Explained* | Pinned README references continual investment in system design | [Red → green attribution limit](red-green.md) |
| Eric Evans, *Domain-Driven Design* | Pinned README references shared language | Provenance only; installed `domain-modeling` owns that vocabulary |

## Version and execution boundary

Prefer the **actual installed skill contract plus user/repository rules** for execution. A newer upstream source can inform a recommendation but does not silently replace that contract. In particular, the February TDD article is historical: the inspected current source uses red → green and moves refactoring to review. The [Red → green card](red-green.md) carries that conflict.

The inspected [ask-matt](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/ask-matt/SKILL.md) and [official guide](https://www.aihero.dev/skills-ask-matt) provide workflow routing; this advisor adds evidence-gap rationale. Installed `writing-for-agents` retains authoring authority. Host enforcement of invocation metadata requires host evidence; these files make no discovery/compliance claim by themselves.

## Reuse

The cards are local summaries and adaptations. [LICENSE](../LICENSE) retains the MIT notice from the [inspected upstream license](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/LICENSE). No book chapter, transcript, or upstream skill body is bundled here. Source maintenance, publishing, installation, and runtime enablement remain separate boundaries under the repository's workflow.
