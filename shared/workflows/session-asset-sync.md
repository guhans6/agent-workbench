# Session asset sync — 2026-10-06

## Scope and provenance

- Matt Pocock’s 38 active skills are pinned to [`4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`](https://github.com/mattpocock/skills/tree/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d). Upstream files are unchanged. Codex invocation metadata accompanies the preserved Pi frontmatter: 23 user-only and 15 model-invocable skills.
- Remove retired `resolving-merge-conflicts` and `writing-great-skills` from vendored assets/catalogs; neither is installed by this sync.
- `shared/skills/setup-delivery-workflow/` is independently owned, copied byte-for-byte from the approved source in [Pix PR #38](https://github.com/guhans6/pix/pull/38). It requires exact-diff approval before repository writes and leaves globals/settings/upstream skills alone. Invoke with Pi `/skill:setup-delivery-workflow` or Codex `$setup-delivery-workflow`.
- `platforms/pi/AGENTS.md` and the marked Completion section in `platforms/codex/AGENTS.md` preserve the approved global reporting convention. Installation is a separate approval-first merge into the actually loaded host instruction file, not a setup-skill side effect. Preserve existing routing and other instructions.

These assets distinguish recurring Definition of Done from task acceptance criteria and report only observed, relevant delivery evidence. Installation, publication and enablement are independent facts, not mandatory stages. Delegated Roles report their assigned scope; the parent verifies aggregate completion.

## Validation boundary

Verify byte equality against the pinned upstream and approved local skill source; verify both hosts’ invocation metadata; parse catalogs and resolve every added skill path; check removed names have no active catalog entries and unrelated assets are unchanged. The catalog's original snapshot date remains historical; `session_sync_date` marks this limited update, not a fresh MCP/platform inventory.

The preceding Pix work verified installed Pi discovery, model-prompt exclusion, explicit command expansion and loaded global/project instruction paths. Codex live discovery, model compliance and child context inheritance remain untested; static metadata is not proof of those behaviors. This repo sync does not run skill scripts, perform repository setup, reinstall runtime assets, or copy auth/session/cache state. Pix’s repository-specific host tests and delivery gates remain in Pix.
