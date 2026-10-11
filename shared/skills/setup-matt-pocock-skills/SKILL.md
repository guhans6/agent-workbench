---
name: setup-matt-pocock-skills
description: "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them
- **Validated checkpoints**: a checked-in project protocol and relative instruction pointer for dependent increments or uncertain integration boundaries

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Existing workflow/checkpoint pointers and delivery references: identify the current authority before proposing adoption; inspect pending edits and preserve local adaptations.
- [Shared checkpoint protocol](../../workflows/validated-checkpoints.md): resolve this relative to the installed skill folder and read the actual file. If missing, stop setup and report the missing reference plus the need to install the consuming skills with their shared `workflows/` directory. Use the supplied protocol, not invented replacement contents. Record its SHA-256 content digest and available source revision for project-copy provenance.
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

**Section D: Validated checkpoints.** Recommend reusing an existing equivalent
project reference and pointer. Otherwise propose a checked-in copy at
`docs/agents/validated-checkpoints.md` with the provenance footer from
[checkpoint-adoption.md](./checkpoint-adoption.md), and its relative pointer in the
chosen instruction file. Resolve conflicting checkpoint pointers with the user
before selecting one. For an existing copy, compare its recorded source digest
with the current project protocol body's digest (bytes before the adoption marker
defined in the seed) and the proposed source digest. A changed project body is a local modification:
merge the proposed update with those changes and preview the exact diff. If the
recorded source identity is missing or cannot establish the baseline, resolve that
gap before replacing content. Identical source and approved project copy need no
update. Consume existing delivery guidance; leave its Definition of
Done and delivery authority with that reference. Establishing missing delivery
agreements belongs to `setup-delivery-workflow`, a separate explicit setup.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)
- The complete checkpoint copy and provenance footer (or proposed edits to the existing reference), and its exact relative pointer diff

Let them edit, then obtain explicit approval for the exact proposed changes
before any project write. If declined or unresolved, report the remaining gap and
stop without writes. Recheck pending edits before applying approval; request a
revised approval if intervening changes conflict.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update only the approved contents in-place rather than appending a duplicate. Preserve surrounding sections and local edits within the block. Reuse an existing workflow/checkpoint pointer instead of creating a second one; identical approved setup is a no-op.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Merge the approved checkpoint pointer from
[checkpoint-adoption.md](./checkpoint-adoption.md) into this block, or update the
existing workflow pointer once. When reusing another reference, point to its
actual project-relative path. Copy the resolved shared
protocol into the approved project path and append completed provenance fields;
keep existing local changes unless their replacement was explicitly approved.
This skill configures project files only; global instructions, skill installation,
publication and enablement are outside this setup.

Then write the other docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Read back every approved file and resolve the relative instruction pointer from
the chosen file's directory. Inspect the diff for preserved unrelated/pending
edits and evaluate a rerun: identical setup must make no changes. Report the
changed paths (or already present), checkpoint source revision and digest, pointer
reachability and unresolved gaps. Static inspection establishes the configured
files, not host loading or live-model adherence; in a CLAUDE-only repo, retain
CLAUDE-first selection and report any unverified host loading explicitly.

Tell the user which engineering skills now have project references. They can edit
`docs/agents/*.md` directly later; checkpoint copies retain their provenance and
local adaptations when reviewed source updates are adopted. Setup is complete
only when approved files and their pointer agree and existing content is preserved.
