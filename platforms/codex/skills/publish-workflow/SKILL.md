---
name: publish-workflow
description: Safe neutral Git/GitHub workflow for creating or reusing branches/worktrees, committing intended changes, pushing/publishing branches, and preparing PR-ready handoff. Use when the user asks to create a branch or worktree, commit, push, publish, or make local changes PR-ready. Do not create/edit/merge/close/delete PRs or rewrite history without explicit approval.
---

# Git Publish Workflow

Turn local work into a clean branch, commit set, optional push, and PR-ready handoff without sweeping in unrelated changes.

## Defaults

- Use a dedicated branch for non-trivial work.
- Use a worktree only when requested or when isolation protects unrelated local changes.
- Commit only files clearly owned by the current task.
- Push only when the user asks to push/publish or explicitly approves it.
- Create or edit PRs only when the user explicitly asks for that PR action.

## First Checks

Before branch, worktree, staging, commit, or push, inspect repo state:

```bash
git status --short --branch
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
git branch --show-current
git branch -vv
git remote -v
git worktree list
```

When GitHub PR state matters and `gh` is available, inspect it with `gh pr status` or `gh pr view`.

Do not modify, stage, commit, or push until staged, unstaged, and untracked changes have been treated as separate scopes.

## Hard Rules

- Do not commit or push directly on the default/protected/release/production branch unless the user explicitly approves that exact target.
- Do not use `git add -A` or `git add .` unless the whole worktree is clearly in scope.
- Do not invent issue numbers, PR links, validation results, branch state, remotes, or repo conventions.
- Do not add AI, tool, assistant, model, or agent attribution to branch names, commits, tags, or PR text.
- Do not run destructive or history-changing commands without explicit approval: `reset --hard`, `clean`, force push, rebase, branch deletion, worktree removal, amend-after-push, or history rewrite.
- Stop if the diff contains secrets, tokens, private keys, credentials, private data, or suspicious generated artifacts.
- When publishing existing work, do not make extra source changes just to clean it up. Report needed fixes, or make them only when they are clearly part of the requested task.
- Report only observed validation. If none ran, say `unverified`.

## Branches

Reuse the current branch only when it is non-default, task-matched, and safe to update.

Create a branch when the current branch is default, detached, unrelated, unsafe, or the user asks for one.

Branch format:

```text
<type>/<short-kebab-slug>
```

Preferred prefixes:

```text
feature/  fix/  refactor/  docs/  test/  chore/  ci/  build/  perf/  hotfix/  release/  spike/
```

Rules:

- Prefer semantic names: `fix/popover-row-spacing`, not `fix-123` or `123`.
- Add an issue suffix only when mapping is reliable: `fix/popover-row-spacing-123`.
- Use lowercase kebab-case after the prefix.
- Avoid spaces, shell-special characters, emoji, private context, and tool/agent names.
- Validate uncertain names with `git check-ref-format --branch <branch>`.
- If base freshness matters, verify the base from local/remote evidence or stop and ask before branching from a stale or unclear base.

## Worktrees

Use a worktree when the user asks, parallel work is needed, the current checkout has unrelated changes, or isolation is safer.

Before creating one:

- Run `git worktree list`.
- Confirm the branch is not already checked out elsewhere.
- Prefer a sibling path outside the repo, such as `../<repo>-<slug>`, unless the user gives a path.
- If using a repo-local worktree directory, verify it is ignored before creating it.
- Confirm the base branch/commit is appropriate for the requested work.

Commands:

```bash
# New branch in a new worktree
git worktree add -b <branch> <path> <base>

# Existing branch in a new worktree
git worktree add <path> <branch>
```

Do not remove, prune, lock, unlock, or delete worktrees without explicit approval. Before removal, verify the target worktree is clean.

## Issues

Use issue references only when reliable:

- User-provided issue number or URL.
- Repo docs such as `AGENTS.md`, `CONTRIBUTING.md`, `.github/pull_request_template.md`, or tracker docs.
- Existing branch, PR, or issue state verified through repo tools or `gh`.

If issue mapping is unclear, omit issue references unless issue linkage materially changes the result.

Commit footer style when reliable:

```text
Refs: #123
```

Use closing keywords such as `Closes #123` or `Fixes #123` only when the change fully resolves the issue and the user/repo convention supports auto-closing. Prefer those in the PR body, not every commit.

## Staging And Commits

Stage only task-owned files:

```bash
git add path/to/fileA path/to/fileB
git add -p path/to/file
```

Before each commit:

```bash
git diff --cached --name-status
git diff --cached
```

Stop before staging or committing when changes are mixed, surprising, generated unexpectedly, binary-heavy, secret-looking, or ambiguous.

Commit grouping:

- Use a small number of meaningful commits.
- Separate unrelated fixes/features.
- Separate formatting-only changes from behavior changes.
- Keep tests with the behavior change unless test infrastructure changed separately.
- Keep dependency or lockfile changes separate when meaningful.
- If hooks modify files, re-inspect before finalizing.

Use the repo's existing commit style. If none is clear, use Conventional Commits:

```text
<type>(optional-scope): <imperative summary>

<body only when useful>

<footer only when useful>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`, `style`, `revert`.

Message rules:

- Subject describes the code change, not the issue number.
- Use imperative mood.
- Body explains rationale, risk, migration, or non-obvious behavior only when useful.
- Footer is only for reliable metadata such as `Refs: #123` or a real `BREAKING CHANGE:`.
- No AI/tool/agent attribution.

## Validation

Run validation when practical and proportional:

- Prefer repo-documented commands from README, CONTRIBUTING, package scripts, Makefile, CI config, or prior conversation.
- Use targeted tests before full suites when faster and meaningful.
- Run formatting/linting only when already configured.

If skipped, state why. If failed, report the exact command and short failure summary.

## Push And PR Handoff

Push only when requested or approved.

Before pushing:

```bash
git status --short --branch
git branch -vv
git remote -v
```

Rules:

- If there is one obvious writable remote and no upstream, `git push -u <remote> <branch>` is allowed.
- If multiple remotes exist and the target is unclear, stop and ask.
- If an open PR already exists for this branch, push only when updating that PR is in scope.
- If push fails due to auth, protection, hooks, non-fast-forward, or rejection, stop and report the failure.
- Do not force push unless explicitly approved for the exact branch and reason.

After push, provide PR-ready output. Create/edit the PR only when explicitly requested.

Final report format:

```text
Branch: <branch>
Worktree: <path or none>
Commits:
- <short-sha> <subject>
Pushed: <yes/no, remote/branch>
PR: <existing PR or recommended title; not created unless approved>
Issues: <refs or none>
Validation: <observed result or unverified>
Notes: <important caveats only>
```

Suggested PR body format:

```markdown
## Summary
- ...

## Validation
- ...

## Issue links
Refs: #123
```

If the change fully resolves an issue, separately recommend whether the PR body should use `Closes #123`.

## Stop And Ask

Stop when any of these would affect correctness or safety:

- Branch, base, worktree path, remote, upstream, or PR target is unclear.
- Current branch is default, detached, protected, unrelated, or unsafe for the requested action.
- Existing staged changes are not clearly in scope.
- Untracked, generated, binary, lockfile, or secret-looking files are ambiguous.
- The diff could belong to multiple unrelated tasks or issues.
- Issue linkage materially affects branch name, commit wording, or PR body.
- A destructive operation, history rewrite, force push, branch deletion, or worktree removal is needed.
