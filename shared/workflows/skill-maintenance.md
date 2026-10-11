# Maintaining adapted engineering skills

Agent-workbench is the source of truth. AI may prepare a scoped change on a branch; publishing, installation and project adoption are separate authorized actions. The checkpoint protocol and Matt-informed advisor are local additions. The three modified Matt skills are adaptations, not unchanged upstream copies.

## Prepare an update

1. Inspect repository state and the requested change. Read writing-for-agents and its skill mechanics for skill edits; use matt-informed-engineering when a principle or design decision is uncertain. Preserve invocation policies and repository verification/permission rules.
2. Read [local-adaptations.json](../upstream/matt-pocock/local-adaptations.json). For an upstream refresh, fetch the selected upstream revision and inspect its diff against each recorded baseline. Use a three-way comparison: saved upstream baseline, proposed upstream revision, and current local file. Resolve each conflict against the recorded local intent and approved requirements. Updating a source pin requires understanding the source changes, not merely changing a hash.
3. Draft the smallest change and observable completion conditions. Keep adapted skill bodies small and the checkpoint rules in their shared reference. For source cards, distinguish published attribution from local inference and record source revision/date. Preserve the upstream MIT notice in copied/substantially derived material.
4. Run `python3 scripts/verify-checkpoint-assets.py`, then the affected scenarios in [checkpoint qualification](checkpoint-qualification.md) and the advisor's scenario file. Inspect actual decisions/artifacts: text checks and reference resolution alone do not establish model adherence or host invocation behavior. Review standards and requested behavior separately.
5. For a refresh, save the new unmodified upstream baseline, its license, revision and checksum; retain the previous baseline in Git history. Record retained local differences and evidence in the change. Commit/push through publish-workflow within the user's authorization. Keep runtime installation and project updates separately reported.

If an upstream behavior conflicts with a local requirement, retain the proven local behavior and surface the decision. A routine source update is not authority to alter invocation, credentials, permissions, global instructions, delivery agreements, or unrelated skills.

## Install a complete checkpoint bundle

The layout is `<agent-assets>/skills/<skill>/` alongside `<agent-assets>/workflows/validated-checkpoints.md`. The consuming skills use `../../workflows/validated-checkpoints.md`; copying one of those folders alone is incomplete. Install the four selected skill folders together with the workflow reference. For the usual shared Codex location this means `~/.agents/skills/` and `~/.agents/workflows/`; for other agents choose the actual loaded skill root and preserve this sibling layout. Confirm host loading separately.

Preview differences at the destination and preserve local edits before replacing files. Run `python3 scripts/verify-checkpoint-assets.py --installation-root <agent-assets>` against the proposed or installed bundle. This command reads the target; it does not install, update instructions or contact a service. Single-folder copying remains suitable only for skills with no external dependency.

Project adoption uses setup-matt-pocock-skills after a draft is approved. It creates a checked-in project reference and a relative AGENTS.md/CLAUDE.md pointer, preserving the existing file and delivery authority. Existing project copies remain pinned until an explicit project update; global skill updates do not silently replace them. On a project refresh, compare the recorded source digest with the existing project copy and proposed source, preserve local changes, preview the exact diff and confirm before writing.

## Maintenance evidence

Record affected requirement, base/source revision, retained local differences, structural/install results, behavioral scenarios actually run, and remaining host/install/adoption boundaries. Publishing a tested bundle is not proof it is installed, loaded, or followed everywhere.
