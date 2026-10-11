# Tracer bullets

**Use when:** work exists in separate layers, but no complete path proves their integration.

**Published method:** Matt's [Tracer Bullets](https://www.aihero.dev/tracer-bullets) describes a small complete path through the layers, exercised for feedback before expansion. The pinned [to-tickets](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets/SKILL.md) uses vertical slices.

**Published attribution:** the article explicitly credits Andrew Hunt and David Thomas's *The Pragmatic Programmer*. This is attribution in the article, not evidence that we read the book.

**Local inference:** name the narrow user-visible path and the integration assumption it must test. Prefer one demo or focused check that can expose a broken connection before completing more isolated layers. The exact checkpoint format is our packaging choice.

**Installed authority:** read `to-tickets` when ticket decomposition is authorized; otherwise consult the active implementation workflow. The advisor supplies rationale, not another ticket workflow.

**Observable done:** the chosen path exercises its required layers and yields a recorded result against an explicit expected outcome. File counts alone do not establish integration.
