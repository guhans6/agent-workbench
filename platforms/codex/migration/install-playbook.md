# Install Playbook

Use this playbook when setting up a new Mac or giving another agent enough context to recreate the user's current Codex working surface.

## 1. Clone The Portable Source

```bash
git clone https://github.com/guhans6/agent-workbench.git ~/agent-workbench
cd ~/agent-workbench
```

This repo is the portable source for:

- repo-curated Codex skills under `platforms/codex/skills/`
- Codex agent TOMLs under `platforms/codex/agents/`
- routing and migration catalogs
- redacted config examples

## 2. Install Repo-Curated Skills

Install personal skills from this repo into the user skill folder:

```bash
mkdir -p ~/.agents/skills
cp -R platforms/codex/skills/apple-ci-bootstrap ~/.agents/skills/
cp -R platforms/codex/skills/ios-macos-repo-workflow ~/.agents/skills/
cp -R platforms/codex/skills/publish-workflow ~/.agents/skills/
```

Alternative for repo-scoped use:

```bash
mkdir -p .agents/skills
cp -R ~/agent-workbench/platforms/codex/skills/publish-workflow .agents/skills/
```

## 3. Install OpenAI System Skills

OpenAI system skills such as `skill-creator`, `skill-installer`, `plugin-creator`, `openai-docs`, and `imagegen` are bundled with Codex. Install or update Codex itself rather than copying those folders.

Relevant upstreams:

- OpenAI skills examples: https://github.com/openai/skills
- Agent Skills specification: https://agentskills.io/specification
- Codex skills docs: https://developers.openai.com/codex/skills

## 4. Install Codex Plugins

Do not copy `~/.codex/plugins/cache`. Install plugins through Codex:

```text
codex
/plugins
```

Install or enable these plugin families when available:

- `browser-use@openai-bundled`
- `computer-use@openai-bundled`
- `build-ios-apps@openai-curated`
- `build-macos-apps@openai-curated`
- `github@openai-curated`
- `canva@openai-curated`
- `superpowers@openai-curated`
- `documents@openai-primary-runtime`
- `spreadsheets@openai-primary-runtime`
- `presentations@openai-primary-runtime`
- `remotion@openai-curated`

Plugin docs: https://developers.openai.com/codex/plugins

## 5. Recreate MCP Servers

Use `mcps-catalog.md` for the command list. Run only the servers you actually need on the new machine.

Common public installs:

```bash
codex mcp add apple-docs -- npx -y @kimsungwhee/apple-docs-mcp@latest
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp add svelte -- npx -y @sveltejs/mcp
codex mcp add xcodebuildmcp -- npx -y xcodebuildmcp@latest mcp
```

After installing OAuth or bearer-token MCPs, authenticate them with the relevant provider-specific flow, for example:

```bash
codex mcp login context7
```

## 6. Restore Local-Only Tools Deliberately

Several current MCPs point at private or machine-local binaries:

- `fff` -> `fff-mcp`
- `idesign` -> `/Users/guhan/.local/bin/idesign-server`
- `ifallow` -> `/Users/Guhan/.local/bin/ifallow serve --mcp`
- `macpilot` -> `/Users/guhan/Guhan/Projects/Xc-build-mcp-mac/MacPilotMCP/release/MacPilotMCP`
- `open-design` -> `od mcp --daemon-url http://127.0.0.1:7456`
- `pencil` -> `/Users/guhan/.pencil/.../mcp-server-darwin-arm64`

Do not assume these exist on a new machine. Install their owning projects first, then add the MCP server once the binary path exists.

## 7. Verify The New Machine

```bash
codex mcp list
codex debug prompt-input
```

Confirm:

- expected MCPs are enabled
- expected skills appear in the available skills section
- plugin skills use plugin-prefixed names such as `build-ios-apps:*` or `github:*`
- no secrets were copied into this repo

