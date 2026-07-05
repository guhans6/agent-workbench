# MCP Catalog

Snapshot date: 2026-07-06.

Source command:

```bash
codex mcp list
```

## Public Or Reinstallable MCPs

| MCP | Purpose | Recreate command | Source |
| --- | --- | --- | --- |
| `apple-docs` | Apple Developer Documentation search for Swift, SwiftUI, UIKit, AppKit, WWDC, and APIs. | `codex mcp add apple-docs -- npx -y @kimsungwhee/apple-docs-mcp@latest` | https://github.com/kimsungwhee/apple-docs-mcp |
| `context7` | Current third-party library and framework docs. | `codex mcp add context7 --url https://mcp.context7.com/mcp` | https://github.com/upstash/context7 |
| `svelte` | Official Svelte documentation and code examples. | `codex mcp add svelte -- npx -y @sveltejs/mcp` | https://github.com/sveltejs/ai-tools |
| `xcodebuildmcp` | Xcode project discovery, simulator workflows, build, run, test, logs, and UI automation. | `codex mcp add xcodebuildmcp -- npx -y xcodebuildmcp@latest mcp` | https://github.com/getsentry/XcodeBuildMCP |
| `github` | GitHub MCP endpoint backed by a bearer token. | `codex mcp add github --url https://api.githubcopilot.com/mcp/` then configure `GITHUB_PAT_TOKEN`. | https://github.com/github/github-mcp-server |
| `excalidraw` | Whiteboard and diagramming MCP. | `codex mcp add excalidraw --url https://mcp.excalidraw.com` | https://excalidraw.com |
| `stitch` | Google Stitch MCP endpoint. | `codex mcp add stitch --url https://stitch.googleapis.com/mcp` then log in. | https://stitch.withgoogle.com |

## Bundled Or Plugin-Provided MCPs

| MCP | Current command | Migration note |
| --- | --- | --- |
| `computer-use` | Plugin-bundled `SkyComputerUseClient ... mcp` | Install the Codex Computer Use/browser-use plugin through Codex; do not copy the cache path. |
| `node_repl` | Codex app bundled Node REPL | Comes from the Codex app runtime. Reinstall/update Codex rather than copying it. |
| `xcode` | `xcrun mcpbridge` | Comes from Apple/Xcode tooling. Install Xcode and confirm `xcrun mcpbridge` exists. |

## Local-Only MCPs

These are enabled on this machine but are not reproducible from this repo alone.

| MCP | Current command | What a new machine needs |
| --- | --- | --- |
| `fff` | `fff-mcp` | Install the owning `fff` fast-file-finder MCP binary, then run `codex mcp add fff -- fff-mcp`. |
| `idesign` | `/Users/guhan/.local/bin/idesign-server` | Install the local iDesign server first, then add its actual binary path. |
| `ifallow` | `/Users/Guhan/.local/bin/ifallow serve --mcp` | Install `ifallow`, then run `codex mcp add ifallow -- /path/to/ifallow serve --mcp`. |
| `macpilot` | `/Users/guhan/Guhan/Projects/Xc-build-mcp-mac/MacPilotMCP/release/MacPilotMCP` | Build or copy the MacPilotMCP project, then register the release binary. |
| `open-design` | `od mcp --daemon-url http://127.0.0.1:7456` | Install Open Design CLI and ensure the daemon is running at the configured URL. |
| `pencil` | `/Users/guhan/.pencil/.../mcp-server-darwin-arm64 --app antigravity_ide --agent codexCLI` | Install Pencil for the target editor/agent and register the generated MCP server path. |

## Auth And Secrets

- `context7` currently uses OAuth in the live list.
- `github` uses `GITHUB_PAT_TOKEN`; do not store the token in this repo.
- `stitch` is installed but not logged in.
- Current `codex mcp list` reports `Auth: Unsupported` for most local stdio servers.

## Verification

After recreating MCPs:

```bash
codex mcp list
```

Expected: required MCPs show `enabled`, and authenticated remotes show a usable auth state.

