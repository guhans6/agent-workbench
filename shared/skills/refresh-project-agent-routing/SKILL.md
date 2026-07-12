---
name: refresh-project-agent-routing
description: Refresh an existing routing contract when relevant models, capabilities, tools, or repository evidence changed. First-time routing uses project-agent-architect.
---

# Refresh Project Agent Routing

Refresh an existing Managed Routing Block through a delta-only proposal. First-time routing uses `project-agent-architect`.

## Draft

1. Keep the target repository read-only while inspecting the existing managed block, agent TOMLs, repository context, and only changed model, skill, MCP, tool, or repository evidence. Record current model, skill, and tool availability in a temporary observations file outside the repository. Complete when every changed input cites evidence and every unaffected route and assignment is marked preserved.
2. Create a temporary proposed-files directory containing only affected files, patching each managed span or TOML field minimally. Complete when its relative paths exactly equal the intended approval list and no target file changed.
3. Run the bundled `scripts/refresh-routing.py --repository <repo> --routing <proposed-files> --observations <temporary-observations> --approved-file <path>` relative to this skill directory for every proposed file. Complete when the approval surface accounts for every changed routing row, capability identity, model assignment, and file, and states `Everything else preserved`.
4. When capability identities changed, replace stale references only in affected routing or profile fields. Complete when stale identities are absent from affected fields and unrelated file hashes remain unchanged.
5. Stop before applying the proposal and obtain approval for the exact delta. Complete when the user approves it, or the run ends without repository changes; every FAIL blocks approval and every WARN is fixed, accepted, or explicitly deferred.
6. After approval, apply only the reviewed patches and rerun the bundled validator against the final routing tree with `--observations <temporary-observations>`. Complete when no FAIL remains, every WARN has a recorded disposition, and the final changed-file list equals the approved list.
