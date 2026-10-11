# Checkpoint adoption seeds

Use these seeds only in the exact-diff preview required by setup. The protocol
contents come from the resolved [shared reference](../../workflows/validated-checkpoints.md),
not this template. Reuse an existing equivalent project reference/pointer when present.

## Instruction pointer

Merge this once into the existing `## Agent skills` section, or adapt an existing
workflow pointer to the approved project-relative path:

```markdown
### Validated checkpoints

For approved implementation with dependent increments or an uncertain integration boundary, read `docs/agents/validated-checkpoints.md` and the repository's delivery reference before planning, advancing or reporting completion.
```

## Project-copy provenance footer

Append this directly after the exact copied source bytes, preserving their final
newline and adding no separator before the marker. Fill every field from observed
source identity and existing project guidance:

```markdown
<!-- checkpoint-adoption:start -->

## Project adoption provenance

- Source: `agent-workbench/shared/workflows/validated-checkpoints.md`.
- Source revision: <verified repository revision, or unavailable for this installed source>.
- Source content SHA-256: <digest of the copied source protocol bytes before adding this footer>.
- Local adaptations: <approved differences from that source, or none>.
- Delivery authority: <existing project-relative delivery reference, or no reference established; reporting uses the existing project convention>.

Source updates compare this recorded digest with the current protocol body
(bytes before the adoption marker) and proposed source, then require a reviewed project diff
that preserves local adaptations. This copy does not replace the repository's delivery authority.
```
