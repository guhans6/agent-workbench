# Codex Migration Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn this repo into a practical source of truth for recreating the user's Codex skills, plugins, and MCP setup on another machine.

**Architecture:** Keep existing routing catalogs as task-selection surfaces. Add `platforms/codex/migration/` as the migration surface with human-readable inventory, install commands, source links, and explicit local-only gaps.

**Tech Stack:** Markdown documentation, YAML catalog metadata, existing Codex CLI and MCP configuration.

---

### Task 1: Add Migration Surface

**Files:**
- Create: `platforms/codex/migration/README.md`
- Create: `platforms/codex/migration/install-playbook.md`
- Create: `platforms/codex/migration/skills-catalog.md`
- Create: `platforms/codex/migration/mcps-catalog.md`
- Create: `platforms/codex/migration/surfaces.yaml`

- [x] **Step 1: Inventory current surfaces**

Run:

```bash
codex debug prompt-input
codex mcp list
find /Users/guhan/.codex/skills /Users/guhan/.agents/skills /Users/guhan/.codex/plugins/cache -path '*/SKILL.md' -type f
```

Expected: current Codex-visible skills, configured MCPs, and local skill folders are visible without exposing secrets.

- [x] **Step 2: Create migration docs**

Write the migration directory with grouped skill and MCP lists, install commands, upstream links where known, and local-only notes for private binaries or untracked skill folders.

- [x] **Step 3: Link migration docs from platform entrypoints**

Update `README.md`, `platforms/codex/README.md`, and `platforms/codex/AGENT_ROUTING_INDEX.md` so future agents start from the migration docs when setting up a new machine.

- [x] **Step 4: Verify docs and catalog syntax**

Run:

```bash
ruby -e 'require "psych"; Psych.load_file("platforms/codex/migration/surfaces.yaml"); puts "yaml ok"'
rg -n "platforms/codex/migration|codex mcp add|github.com|local-only" README.md platforms/codex
```

Expected: YAML parses, and repo entrypoints point to the migration surface.
