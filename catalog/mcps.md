# MCP Catalog

Snapshot date: 2026-07-06.

Source command:

```bash
codex mcp list
```

This catalog is written for any agent that can use MCP. Commands are shown with Codex examples because Codex is the current configured client; other agents should translate the same server command, URL, and auth requirements into their own MCP config format.

| MCP | Kind | Install or recreate | Source | Auth | Status |
| --- | --- | --- | --- | --- | --- |
| `apple-docs` | stdio | codex mcp add apple-docs -- npx -y @kimsungwhee/apple-docs-mcp@latest | https://github.com/kimsungwhee/apple-docs-mcp | Unsupported | enabled |
| `computer-use` | plugin-bundled stdio | Install the Codex Computer Use/browser-use plugin; do not copy the cache path. | Codex app/plugin runtime | Unsupported | enabled |
| `context7` | streamable-http | codex mcp add context7 --url https://mcp.context7.com/mcp | https://github.com/upstash/context7 | OAuth | enabled |
| `excalidraw` | streamable-http | codex mcp add excalidraw --url https://mcp.excalidraw.com | https://excalidraw.com | Unsupported | enabled |
| `fff` | local stdio | Install the owning fff-mcp binary, then run: codex mcp add fff -- fff-mcp | local-tool-required | Unsupported | enabled |
| `github` | streamable-http | codex mcp add github --url https://api.githubcopilot.com/mcp/ and configure GITHUB_PAT_TOKEN | https://github.com/github/github-mcp-server | Bearer token | enabled |
| `idesign` | local stdio | Install idesign-server, then register the local binary path. | local-tool-required | Unsupported | enabled |
| `ifallow` | local stdio | Install ifallow, then run: codex mcp add ifallow -- /path/to/ifallow serve --mcp | local-tool-required | Unsupported | enabled |
| `macpilot` | local stdio | Build or install MacPilotMCP, then register the release binary. | local-tool-required | Unsupported | enabled |
| `node_repl` | bundled stdio | Comes from the Codex app runtime. | Codex app runtime | Unsupported | enabled |
| `open-design` | local stdio | Install Open Design CLI and run/register: od mcp --daemon-url http://127.0.0.1:7456 | local-tool-required | Unsupported | enabled |
| `pencil` | local stdio | Install Pencil for the target editor/agent and register its generated MCP server path. | local-tool-required | Unsupported | enabled |
| `stitch` | streamable-http | codex mcp add stitch --url https://stitch.googleapis.com/mcp, then log in | https://stitch.withgoogle.com | Not logged in | enabled |
| `svelte` | stdio | codex mcp add svelte -- npx -y @sveltejs/mcp | https://github.com/sveltejs/ai-tools | Unsupported | enabled |
| `xcode` | platform stdio | Install Xcode and confirm xcrun mcpbridge exists. | Apple Xcode command line tools | Unsupported | enabled |
| `xcodebuildmcp` | stdio | codex mcp add xcodebuildmcp -- npx -y xcodebuildmcp@latest mcp | https://github.com/getsentry/XcodeBuildMCP | Unsupported | enabled |

## Verification

```bash
codex mcp list
```

Every MCP name above should appear in the target agent's MCP list or have a documented reason why the local tool is not installed on that machine.
