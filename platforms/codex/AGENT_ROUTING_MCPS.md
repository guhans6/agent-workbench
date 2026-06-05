# Agent MCP Routing Guide

This file is the fast-routing surface for MCP choice.
Read this before choosing an MCP server for a task.

For the full machine-readable inventory, read:

- `AGENT_ROUTING_MCPS.yaml`

## Routing Order

Use this order:

1. Decide whether the task is docs lookup, repo exploration, design work, browser or JS automation, macOS host control, or Apple build and runtime control.
2. Pick the narrowest MCP that directly matches the task.
3. Prefer specialized MCPs over generic execution surfaces.
4. Only fall back to general-purpose surfaces when the specialized MCP does not fit.

## Quick Picks

### `apple-docs`

Use when:

- Apple API behavior is uncertain
- platform availability matters
- SwiftUI, UIKit, AppKit, SwiftData, XCTest, or Xcode semantics need official references

Do not use when:

- the docs needed are for non-Apple libraries

### `context7`

Use when:

- current third-party library or framework docs are needed
- setup, migration, API syntax, or examples depend on current documentation
- the task mentions libraries such as React, Next.js, Prisma, Tailwind, Express, Django, or similar ecosystems

Do not use when:

- the question is Apple-framework specific

### `fff`

Use when:

- you need fast file finding in a project
- you need to locate likely files or modules before reading or editing

Do not use when:

- the task is documentation lookup rather than repo exploration

### `xcodebuildmcp`

Use when:

- you need to discover, build, run, test, inspect, or automate Apple projects
- you need simulator workflows
- you need logs, UI inspection, or Apple runtime automation

Do not use when:

- the task is only Apple docs lookup

### `xcode`

Use when:

- the task specifically needs Xcode to perform an IDE action
- you need an Xcode-directed step rather than a build-system oriented step

### `macpilot`

Use when:

- the task needs macOS host automation
- the task needs system-level UI or app interaction outside normal repo tools

### `node_repl`

Use when:

- you need persistent JavaScript execution
- you need scripted browser helpers or iterative automation
- you need JS-based control loops that should persist across calls

Do not use when:

- a specialized MCP already covers the task directly

### `codex_apps`

Use when:

- the task depends on an installed app or connector-backed tool
- the tool is exposed through Codex apps rather than a repo-local skill
- the task is explicitly running in Codex where this surface exists

### `excalidraw`

Use when:

- the task is diagramming or whiteboard-style visual explanation

### `pencil`

Use when:

- the task is editing or validating `.pen` design files

### `idesign`

Use when:

- the task is design-oriented and needs an MCP-backed design workflow
- the target machine has `idesign` enabled

Do not use when:

- the current platform config disables it

### `ifallow`

Use when:

- the task depends on policy-aware gating or allowlist-style tool flows

### `MCP To Task Map`

| Task shape | Preferred MCP | Notes |
| --- | --- | --- |
| Apple framework docs | `apple-docs` | Official Apple docs first |
| Current non-Apple framework docs | `context7` | Current library docs first |
| Find files in a repo | `fff` | Fast repo exploration |
| Build or test an Apple project | `xcodebuildmcp` | Main Apple build surface |
| Perform an Xcode IDE action | `xcode` | Narrow IDE-oriented action |
| Automate macOS host behavior | `macpilot` | System and app level control |
| Persistent JS automation | `node_repl` | Good for iterative automation loops |
| Use installed app or connector tools | `codex_apps` | App-backed capabilities |
| Diagramming | `excalidraw` | Whiteboard and diagram tasks |
| `.pen` design editing | `pencil` | Use only through Pencil tools |
| General design workflow from MCP surface | `excalidraw` or `pencil` | `idesign` is disabled in the current config snapshot |
| Policy-aware tool flow | `ifallow` | Specialized policy surface |

## Selection Rules

- Prefer `apple-docs` for Apple APIs and `context7` for non-Apple libraries.
- Prefer `xcodebuildmcp` before generic shell workflows for Apple build, run, and test tasks.
- Prefer `fff` before broad manual file crawling when the task starts with repo exploration.
- Prefer `node_repl` only when persistent JavaScript execution materially helps.
- Do not use a design MCP when the task is really docs lookup or code execution.

## Source Of Truth

The detailed MCP inventory lives here:

- `platforms/codex/AGENT_ROUTING_MCPS.yaml`

If this guide and the catalog disagree, the catalog wins.
