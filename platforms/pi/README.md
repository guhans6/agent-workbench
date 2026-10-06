# Pi guidance

`AGENTS.md` contains the approved global completion guidance, not a runtime export.

Before installation, confirm the actual loaded global context file in the Pi agent directory (default `~/.pi/agent`, relocated by `PI_CODING_AGENT_DIR`), including any override. Preview the diff, obtain approval, and merge the marked Completion block once, preserving existing instructions. Do not overwrite a user's global file or edit trust/settings to activate it.

Shared skills live under `../../shared/skills/`. Pi supports `~/.agents/skills`; an existing `~/.pi/agent/skills` link is also usable. Avoid duplicate copies. `disable-model-invocation: true` makes a skill explicit-only; invoke the new setup with `/skill:setup-delivery-workflow`. This is routing policy, not a security boundary.

See `../../shared/workflows/session-asset-sync.md` for provenance and verification limits.
