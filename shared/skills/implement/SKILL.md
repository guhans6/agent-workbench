---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the approved work in the spec or tickets. Read the repository's domain,
design and delivery guidance, then
[validated checkpoints](../../workflows/validated-checkpoints.md).

For dependent increments or an uncertain integration boundary, work the ticket's
checkpoint plan: establish its baseline, implement the smallest remaining
increment, prove its observable completion and advance within existing authority.
Derive a compact plan from approved acceptance criteria if the ticket lacks one.
For one-step work, use its acceptance criteria and focused proof directly.

Use /tdd where possible at pre-agreed public seams. Run the focused checks and
release gates required by the repository; honor its test scope and execution path.

Use /code-review at the repository's agreed review boundary; if none is specified,
review before reporting implementation complete or making an authorized commit.
Use publish-workflow for commit and publication actions only when authorized.

Report acceptance evidence and remaining delivery work using the repository's
completion convention. Local validation, installation, publication and enablement
are separate claims, supported only by their observed evidence.
