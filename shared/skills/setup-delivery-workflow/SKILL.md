---
name: setup-delivery-workflow
description: Agree and record a repository Definition of Done and delivery reporting convention.
disable-model-invocation: true
---
# Setup delivery workflow

Explicit invocation: Pi `/skill:setup-delivery-workflow`; Codex `$setup-delivery-workflow`. This independently owned skill configures repo guidance, not delivery actions. Invocation is not write approval. Review-only/read-only Roles read existing guidance and report gaps; they do not perform setup.

## Process

1. **Inspect.** Read applicable root, ancestor and nested instructions, existing workflow/delivery references, issue/spec conventions, declared checks and release commands, and pending edits. Locate the instruction file actually loaded by the active host, including overrides or configured fallbacks. Finish with the existing agreements, authority paths and gaps identified; inspect sources rather than running new costly checks.
2. **Resolve gaps.** Recommend reusing an existing reference and pointer. Ask only unresolved questions about the completion boundary/exclusions, quality and acceptance evidence, delivery targets, and who may perform installation, publication or enablement. Existing issues/specs can supply answers; no mandatory interview or per-task document. Ask on conflicting pointers or nested authority before choosing a source. In a CLAUDE-only repo, explain that Codex does not load CLAUDE.md by default and request approval for an AGENTS.md pointer or a confirmed configured fallback; do not silently create competing authority.
3. **Propose and approve.** Show the exact proposed reference and pointer diff, including new-file contents. Use the recording guidance below. Prefer one section in an existing reference and its existing pointer; when none exists, recommend `docs/agents/delivery.md` and one pointer: “For scope, Definition of Done, and delivery reporting, read `docs/agents/delivery.md`.” Obtain explicit approval for this diff **before any repo write**. If approval is declined or unresolved, report the gap and stop without writes.
4. **Merge.** Recheck pending edits and merge only the approved content, preserving unrelated content and user changes; ask again if intervening changes conflict with the approval. Create/update at most one reference and one instruction pointer, never duplicate an existing authority. If the approved convention already exists, make no changes. Setup does not install, publish or enable anything, edit globals/settings/upstream skills, or run new costly checks without separate authority.
5. **Verify and report.** Read back the reference and loaded pointer: both must agree on scope and consumers must reach the reference. Inspect the diff for preserved unrelated/pending edits and evaluate a rerun: it must be a no-op. Report changed paths (or already present), agreed completion boundary, pointer reachability, checks performed, and unresolved gaps. Setup is complete only when the approved reference/pointer agree and unrelated content is preserved; do not claim live-model compliance from static inspection.

## What the reference records

- **Definition of Done:** the recurring quality/evidence bar applicable to this repo's work. **Acceptance criteria:** the task-specific agreed outcome and exclusions, sourced from the existing issue/spec or user agreement. Apply the relevant bar; research, refactoring and local tasks do not automatically require production rollout.
- Evidence for every applicable criterion, tied to the revision/artifact and checked target. Link check commands to their declared source rather than copying inventories. Required criteria without passing evidence leave the outcome incomplete: name remaining work and next owner. Out-of-scope actions are not failures or permission to expand scope.
- Implementation, validation, installation, publication and enablement are independent reporting facets, not ordered stages. Use only relevant facets, with observations/targets; mark not performed, unknown or out of scope honestly. No exhaustive table is required every turn, and local validation is not proof of installation, publication or enablement.
- Delegated Roles read the applicable reference and report their assigned scope/evidence only. The parent verifies aggregate acceptance; dispatch must carry the reference when child context discovery is uncertain. Reporting does not change a product's runtime lifecycle or action permissions.

## Foundations (adaptation)

This convention adapts the [Scrum Guide's Definition of Done](https://scrumguides.org/scrum-guide.html#commitment-definition-of-done), Humble's [delivery/deployment distinction](https://continuousdelivery.com/2010/08/continuous-delivery-vs-continuous-deployment/) and [deployment patterns](https://continuousdelivery.com/implementing/patterns/), and the publisher's [Pragmatic Programmer tips](https://assets3.pragprog.com/tips/) (8, 20, 68, 95). These accessible passages support agreed quality, target-specific evidence and thin end-to-end checks; this is not full-book reading, a Scrum mandate, or a prescribed delivery state machine. Approval-before-merge packaging follows setup-matt-pocock-skills; this skill is independently owned, not an upstream fork.
