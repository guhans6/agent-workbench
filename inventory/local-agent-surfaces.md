# Local Agent Surfaces

## Copied Into This Repo

### Codex skills

- `platforms/codex/skills/publish-workflow`
- `platforms/codex/skills/apple-ci-bootstrap`
- `platforms/codex/skills/ios-macos-repo-workflow`

### Codex config

- `platforms/codex/AGENTS.md`
- `platforms/codex/config.redacted.toml`
- `platforms/codex/rules/default.rules`
- `platforms/codex/agents/*.toml`

### Shared agent notes

- `shared/rules/graphify.md`
- `shared/workflows/graphify.md`

## Detected Locally But Not Copied By Default

These were detected in user-local skill roots, but were not copied into this repo in the first pass because ownership or source-of-truth status is less clear than the curated assets above.

### `~/.agents/skills`

- `apple-on-device-ai`
- `caveman`
- `caveman-commit`
- `caveman-compress`
- `caveman-help`
- `caveman-review`
- `compress`
- `context7-mcp`
- `diagnose`
- `graphify`
- `grill-me`
- `grill-with-docs`
- `huashu-design`
- `improve-codebase-architecture`
- `ios-debugger-agent`
- `ios-hig`
- `ios-macos-repo-workflow`
- `mobile-ios-design`
- `prototype`
- `setup-matt-pocock-skills`
- `swift-architecture-skill`
- `swift-concurrency-expert`
- `swift-testing-expert`
- `swiftdata-pro`
- `swiftui-pro`
- `tdd`
- `to-issues`
- `to-prd`
- `triage`
- `write-a-skill`
- `zoom-out`

### `~/.codex/skills`

Excluded from copy when they were clearly system, bundled, or runtime-installed duplicates of source assets:

- `.system/*`
- local installed duplicates of source skills already copied from source workspace
- other locally installed skills that appear to be runtime mirrors rather than source-of-truth

## Redaction Notes

The exported Codex config snapshot is redacted:

- API keys removed
- project trust blocks omitted
- auth/session/runtime files not copied

If you want this repo to absorb more of `~/.agents/skills` later, do that as an explicit second curation pass instead of a blind dump.
