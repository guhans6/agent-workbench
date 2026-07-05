---
name: commit-and-push
description: Commit and push code changes with issue-aware scope, clean commit grouping, and intentional PR follow-up. Use when user asks to commit, push, publish local changes, prepare a PR after pushing, or wants issue-linked git hygiene without generic agent attribution.
---

# Commit And Push

Commit and push with deliberate scope, issue hygiene, and clean history.
Default behavior is `commit` + `push`.
PR creation or PR metadata updates require explicit approval after push.
Pushing new commits to a branch with an existing PR is allowed unless the user says to hold push for review.

## Quick Start

Use this skill when the user says:

- "commit this"
- "commit and push"
- "publish these changes"
- "push and prepare a PR"

## Rules

- Use current conversation context first to infer scope.
- Add issue references only when issue IDs or issue-reference convention are confirmed by explicit user input, repo-local docs, or tracker evidence.
- If issue mapping is unclear, inspect repo issue-tracker docs or tracker state before committing. If still unclear, omit issue refs and report that no reliable mapping was found, or stop and ask if issue linkage is materially important.
- Never add AI attribution, agent names, or generated-by text to commits or PRs.
- Never default to `git add -A` unless the whole worktree is clearly in scope.
- Treat `git diff --cached`, unstaged changes, and untracked files as separate scope surfaces.
- If the index already contains out-of-scope work, stop and ask before committing.
- Stage only clearly in-scope files when all of the following are true: files match the current task, diff intent is coherent, no unrelated staged or untracked files would be swept in, and issue mapping is confirmed if issue refs will be used.
- Stop and ask when the worktree contains mixed or ambiguous changes.
- Split into a small number of meaningful commits, not one dump and not micro-commits.
- Keep commit subjects focused on the code change, not issue metadata.
- Use the repo's issue-reference convention in commit footers by default, for example `Refs: #123`.
- Reserve `Closes:`, `Closes #123`, `Fixes #123`, and similar closing keywords for the PR body by default.
- Check current branch, upstream remote, and default branch before push.
- Do not push directly to the default or protected branch unless the user explicitly asked for that exact push after the branch target is clear.
- If the branch has no upstream, creating one against the expected primary writable remote is allowed only when there is a single obvious remote target. Otherwise stop and ask.
- After non-fast-forward, auth, protected-branch, or hook-related push failures, stop and ask unless the next step is unambiguously safe.
- Report only observed validation. If none ran, say unverified.

## Workflow

1. Inspect `git status`, `git diff`, `git diff --cached`, and untracked files separately.
2. Infer which files belong to the current request from conversation context and repo state.
3. Check for issue-tracker truth in repo docs such as `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `AGENTS.md`, or equivalent local guidance.
4. If issue linkage is still unclear and the user expects issue-aware publishing, inspect the tracker before committing. If no reliable issue mapping is found, omit issue refs or stop and ask when issue linkage materially changes the result.
5. Propose an internal commit grouping plan and apply it directly unless scope is ambiguous.
6. Stage only the files for the first coherent commit.
7. Write a clean Conventional Commit message. Add body only when needed. Add footer refs when relevant.
8. Repeat for each meaningful commit group.
9. Check branch name, upstream, default branch, and whether the branch already backs an open PR.
10. Push the branch when the target is safe.
11. Stop and present a concise PR recommendation summary:
   - branch pushed
   - commits created
   - linked issues, if reliably known
   - whether the branch already has an open PR
   - recommended PR title
   - whether the PR should close any issues
   - observed validation or `unverified`
12. Create or update the PR only after explicit approval.

## When To Stop And Ask

- unrelated or surprising local changes are mixed into the worktree
- issue mapping materially affects commit grouping or wording
- no reliable issue mapping exists and issue linkage matters
- the diff could reasonably belong to multiple unrelated issues
- the repo has conflicting issue-tracker guidance
- push target, branch strategy, PR target, or direct-push safety is unclear
- the branch is detached, unnamed, default, protected, or points at an unsafe upstream
- the branch has no upstream and there is no single obvious remote target
- the branch already backs an open PR and the user asked not to update it yet

## Commit Policy

- Subject: Conventional Commit form, short, imperative, no issue numbers by default
- Body: only when rationale, risk, migration, or behavior change is not obvious
- Footer: structured metadata using the repo's issue-reference convention
- Small self-explanatory commit may omit body and footer when no issue mapping is needed

See [REFERENCE.md](REFERENCE.md) for grouping rules, commit standards, and PR policy.
