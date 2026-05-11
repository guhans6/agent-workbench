---
name: publish-workflow
description: Create or reuse the right branch, commit and optionally push code changes with issue-aware scope, then recommend PR follow-up without creating or editing the PR unless approved. Use when user asks to create a branch, commit, push, publish local changes, or prepare PR-ready git output with disciplined workflow hygiene.
---

# Publish Workflow

Create the right branch when needed, then commit and optionally push with deliberate scope, issue hygiene, and clean history.
Default behavior is branch if needed, then `commit` + `push` only when the user asked to publish or push.
PR creation or PR metadata updates require explicit approval after push.
Pushing new commits to a branch with an existing PR is allowed unless the user says to hold push for review.

## Quick Start

Use this skill when the user says:

- "create a branch for this"
- "commit this"
- "commit and push"
- "publish these changes"
- "push and prepare a PR"

## Rules

- Use current conversation context first to infer scope.
- For non-trivial implementation work, prefer a dedicated branch over working on the default branch.
- If already on a clearly scoped non-default branch that matches the task, reuse it.
- If on the default branch, do not commit there without explicit approval. Create a branch before staging or committing unless the user clearly asked to stay on the default branch.
- Do not use issue-number-only branch names by default.
- Default branch naming should be semantic and prefixed by work type, such as `feature/<slug>`, `fix/<slug>`, `refactor/<slug>`, or `chore/<slug>`.
- Add an issue identifier in the branch name only when issue mapping is explicit and useful. Prefer semantic slug first, then issue, for example `feature/editor-selection-188`.
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
3. Check the current branch, default branch base, and remote tracking state against the task.
4. If a new branch is needed, ensure the default branch base is validated by remote-tracking evidence, an approved fetch/update step, or explicit user acceptance of branching from the current local base. Otherwise stop and ask.
5. If a new branch is needed, create one with a semantic prefix and concise slug before staging or committing.
6. Check whether the chosen branch already backs an open PR and confirm that updating that branch is in scope when it matters.
7. Check for issue-tracker truth in repo docs such as `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `AGENTS.md`, or equivalent local guidance.
8. If issue linkage is still unclear and the user expects issue-aware publishing, inspect the tracker before committing. If no reliable issue mapping is found, omit issue refs or stop and ask when issue linkage materially changes the result.
9. Propose an internal commit grouping plan and apply it directly unless scope is ambiguous.
10. Stage only the files for the first coherent commit.
11. Write a clean Conventional Commit message. Add body only when needed. Add footer refs when relevant.
12. Repeat for each meaningful commit group.
13. If the user asked to publish or push, check branch name, upstream, default branch, and whether the branch already backs an open PR.
14. If the user asked to publish or push, push the branch when the target is safe.
15. Stop and present a concise summary:
   - branch created or reused
   - commits created
   - whether the branch was pushed
   - linked issues, if reliably known
   - whether the branch already has an open PR
   - recommended PR title
   - whether the PR should close any issues
   - observed validation or `unverified`
16. Create or update the PR only after explicit approval.

## When To Stop And Ask

- unrelated or surprising local changes are mixed into the worktree
- current branch is unrelated to the task or branch naming intent is ambiguous
- the default branch base is stale or unclear before creating a new branch
- issue mapping materially affects commit grouping or wording
- no reliable issue mapping exists and issue linkage matters
- the diff could reasonably belong to multiple unrelated issues
- the repo has conflicting issue-tracker guidance
- push target, branch strategy, PR target, or direct-push safety is unclear
- the branch is detached, unnamed, default, protected, or points at an unsafe upstream
- the branch has no upstream and there is no single obvious remote target
- the branch already backs an open PR and the user asked not to update it yet

## Branch And Commit Policy

- Branch: semantic work-type prefix plus concise slug, no issue-only names by default, optional issue suffix only when explicit
- Subject: Conventional Commit form, short, imperative, no issue numbers by default
- Body: only when rationale, risk, migration, or behavior change is not obvious
- Footer: structured metadata using the repo's issue-reference convention
- Small self-explanatory commit may omit body and footer when no issue mapping is needed

See [REFERENCE.md](REFERENCE.md) for branch strategy, grouping rules, commit standards, and PR policy.
