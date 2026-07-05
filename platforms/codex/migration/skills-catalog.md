# Skills Catalog

Snapshot date: 2026-07-06.

This catalog combines the current Codex-visible skill list, local skill folders, plugin cache evidence, and this repo's curated skills. Codex may shorten or omit some installed skills from the initial prompt when the skill list exceeds the prompt budget, so installed-on-disk plugin skills are tracked separately.

## Install Sources

| Source | Portable? | Install method |
| --- | --- | --- |
| This repo: `platforms/codex/skills/*` | Yes | Clone `https://github.com/guhans6/agent-workbench.git`, then copy selected skill folders into `~/.agents/skills` or a repo `.agents/skills` folder. |
| User shared skills: `~/.agents/skills/*` | Partly | Local-only unless an upstream repo is named below. Add upstream links before relying on these for migration. |
| User Codex skills: `~/.codex/skills/*` | Partly | Local-only unless checked into this repo or installed through `$skill-installer`. |
| OpenAI system skills | Yes, via Codex | Install/update Codex; do not copy system folders. |
| Codex plugins | Yes, via plugin install | Install through Codex `/plugins`; do not copy plugin caches. |

## Repo-Curated Skills

These are the portable personal skill sources already checked into this repo.

| Skill | Description | Install |
| --- | --- | --- |
| `apple-ci-bootstrap` | Proposes and creates local-first verification for Apple-platform repositories. | `cp -R platforms/codex/skills/apple-ci-bootstrap ~/.agents/skills/` |
| `ios-macos-repo-workflow` | Creates and maintains a repo-local workflow contract for Xcode-first Apple repositories. | `cp -R platforms/codex/skills/ios-macos-repo-workflow ~/.agents/skills/` |
| `publish-workflow` | Creates or reuses a branch, commits intentionally, and prepares PR-ready output. | `cp -R platforms/codex/skills/publish-workflow ~/.agents/skills/` |

## OpenAI System Skills

These come with Codex itself.

| Skill | Description | Source |
| --- | --- | --- |
| `imagegen` | Generate or edit raster images. | Codex system skill |
| `openai-docs` | Current OpenAI and Codex product documentation workflow. | Codex system skill |
| `plugin-creator` | Scaffold Codex plugin directories and manifests. | Codex system skill |
| `skill-creator` | Create or update Codex skills. | Codex system skill |
| `skill-installer` | Install Codex skills from curated lists or GitHub repo paths. | Codex system skill |

## User-Global Skills Visible To Codex

These are available from local user skill folders on this machine. They should be copied into this repo or linked to upstream repos before relying on the catalog for a clean migration.

| Skill | Short description | Current source |
| --- | --- | --- |
| `apple-on-device-ai` | Foundation Models, Core ML, and local LLM integration on Apple Silicon. | `~/.agents/skills` |
| `cavecrew` | Dispatch guide for caveman-style subagents. | `~/.agents/skills` |
| `caveman` | Ultra-compressed communication mode. | `~/.agents/skills` |
| `caveman-commit` | Compact commit message generator. | `~/.agents/skills` |
| `caveman-compress` | Compress memory and preference files. | `~/.agents/skills` |
| `caveman-help` | Quick reference for caveman modes and commands. | `~/.agents/skills` |
| `caveman-review` | Compact code review comments. | `~/.agents/skills` |
| `caveman-stats` | Token usage and savings report. | `~/.agents/skills` |
| `chatgpt-apps` | Build and troubleshoot ChatGPT Apps SDK apps. | `~/.agents/skills` |
| `cli-creator` | Build composable CLIs from APIs, SDKs, web apps, or scripts. | `~/.agents/skills` |
| `cloudflare-deploy` | Deploy apps and infrastructure to Cloudflare. | `~/.agents/skills` |
| `context7-mcp` | Use Context7 for current library docs. | `~/.agents/skills` |
| `define-goal` | Define concrete measurable goals. | `~/.agents/skills` |
| `diagnose` | Disciplined debugging loop. | `~/.agents/skills` |
| `figma-create-design-system-rules` | Generate design system rules from codebase and Figma context. | `~/.agents/skills` |
| `gh-address-comments` | Address GitHub PR review comments. | `~/.agents/skills` |
| `gh-fix-ci` | Debug or fix failing GitHub Actions checks. | `~/.agents/skills` |
| `graphify` | Generate knowledge graphs and audit reports from input. | `~/.agents/skills` |
| `grill-me` | Pressure-test requirements or plans. | `~/.agents/skills` |
| `grill-with-docs` | Pressure-test plans against domain docs. | `~/.agents/skills` |
| `handoff` | Create compact continuation handoff docs. | `~/.agents/skills` |
| `huashu-design` | HTML prototypes, interaction demos, and expert design review. | `~/.agents/skills` |
| `impeccable` | Design, critique, polish, and adapt product experiences. | `~/.agents/skills` |
| `improve-codebase-architecture` | Architecture review informed by repo domain language. | `~/.agents/skills` |
| `ios-debugger-agent` | Build, run, launch, and debug iOS apps with XcodeBuildMCP. | `~/.agents/skills` |
| `ios-hig` | iOS HIG, accessibility, Dynamic Type, and SwiftUI interface guidance. | `~/.agents/skills` |
| `ios-macos-repo-workflow` | Apple repo workflow contract. | `~/.agents/skills` and this repo |
| `migrate-to-codex` | Migrate instructions, skills, agents, and MCP config into Codex. | `~/.agents/skills` |
| `mobile-ios-design` | Native iOS interface and SwiftUI patterns. | `~/.agents/skills` |
| `netlify-deploy` | Deploy web projects to Netlify. | `~/.agents/skills` |
| `pdf` | Read, create, inspect, render, and verify PDFs. | `~/.agents/skills` |
| `playwright` | Browser automation from the terminal. | `~/.agents/skills` |
| `playwright-interactive` | Persistent browser and Electron interaction. | `~/.agents/skills` |
| `prototype` | Build throwaway prototypes to clarify design. | `~/.agents/skills` |
| `screenshot` | Take desktop or system screenshots. | `~/.agents/skills` |
| `security-best-practices` | Language/framework security best-practice review. | `~/.agents/skills` |
| `security-ownership-map` | Security ownership topology and bus-factor mapping. | `~/.agents/skills` |
| `security-threat-model` | Repository-grounded threat modeling. | `~/.agents/skills` |
| `sentry` | Inspect Sentry issues and recent production errors. | `~/.agents/skills` |
| `setup-matt-pocock-skills` | Set up repo issue-tracker and docs context for engineering skills. | `~/.agents/skills` |
| `speech` | Text-to-speech narration and batch speech generation. | `~/.agents/skills` |
| `swift-architecture-skill` | Swift architecture patterns and playbooks. | `~/.agents/skills` |
| `swift-concurrency-expert` | Swift Concurrency review and remediation. | `~/.agents/skills` |
| `swift-testing-expert` | Swift Testing structure, macros, traits, and plans. | `~/.agents/skills` |
| `swiftdata-pro` | SwiftData writing, review, and improvement. | `~/.agents/skills` |
| `swiftui-pro:swiftui-pro` | SwiftUI code review for APIs, maintainability, and performance. | `~/.agents/skills` |
| `tdd` | Red-green-refactor feature and bugfix workflow. | `~/.agents/skills` |
| `thermo-nuclear-code-quality-review` | Strict maintainability review. | `~/.agents/skills` |
| `to-issues` | Break plans or PRDs into shippable issues. | `~/.agents/skills` |
| `to-prd` | Turn conversation context into a PRD. | `~/.agents/skills` |
| `triage` | Issue triage state-machine workflow. | `~/.agents/skills` |
| `write-a-skill` | Create new agent skills with proper structure. | `~/.agents/skills` |
| `zoom-out` | Provide broader system context. | `~/.agents/skills` |

## Plugin-Bundled Skills Visible To Codex

Install these through Codex plugins, not by copying plugin cache folders.

| Plugin family | Skills visible in current Codex prompt |
| --- | --- |
| `browser` | `browser:control-in-app-browser` |
| `chrome` | `chrome:control-chrome` |
| `computer-use` | `computer-use:computer-use` |
| `build-ios-apps` | `ios-app-intents`, `ios-debugger-agent`, `ios-ettrace-performance`, `ios-memgraph-leaks`, `ios-simulator-browser`, `swiftui-liquid-glass`, `swiftui-performance-audit`, `swiftui-ui-patterns`, `swiftui-view-refactor` |
| `build-macos-apps` | `appkit-interop`, `build-run-debug`, `liquid-glass`, `packaging-notarization`, `signing-entitlements`, `swiftpm-macos`, `swiftui-patterns`, `telemetry`, `test-triage`, `view-refactor`, `window-management` |
| `canva` | `canva-resize-for-all-social-media`, `canva-translate-design` |
| `github` | `github`, `gh-address-comments`, `gh-fix-ci`, `yeet` |
| `superpowers` | `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans` |
| `openai-primary-runtime` | `pdf:pdf`, `template-creator:template-creator` |

## Installed On Disk But Not Always In Initial Prompt

Codex may omit some installed skills from the initial prompt when descriptions exceed the skill-list budget. The following plugin cache evidence exists on this machine and should be installed through the matching plugin if needed:

| Plugin family | Additional skill folders found on disk |
| --- | --- |
| `canva` | `canva-branded-presentation` |
| `codex-security` | `attack-path-analysis`, `deep-security-scan`, `finding-discovery`, `fix-finding`, `security-diff-scan`, `security-scan`, `threat-model`, `track-findings`, `triage-finding`, `validation` |
| `game-studio` | `game-playtest`, `game-studio`, `game-ui-frontend`, `phaser-2d-game`, `react-three-fiber-game`, `sprite-pipeline`, `three-webgl-game`, `web-3d-asset-pipeline`, `web-game-foundations` |
| `remotion` | `remotion` |

## Migration Gaps To Close

- Add upstream repo links for user-global skills that should be portable.
- Decide which `~/.agents/skills` folders should be vendored into this repo under `platforms/codex/skills/`.
- Add `agents/openai.yaml` metadata for any repo-curated skill that depends on an MCP server.

