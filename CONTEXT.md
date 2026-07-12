# Agent Workbench

Agent Workbench provides compact, composable operating guidance for coding agents without replacing the underlying engineering workflows.

## Language

**Project Agent Architect**:
A setup skill that derives the smallest justified repository-specific routing configuration from observed evidence.
_Avoid_: Team generator, agent framework

**Routing Contract**:
An ordered policy that maps task evidence to the best-value execution profile and defines when escalation is justified.
_Avoid_: Team handbook, role catalog

**Executable Agent Profile**:
A named worker configuration that pins an execution model, reasoning effort, access boundary, and narrow responsibility.
_Avoid_: Persona, team member

**Best-Value Profile**:
The executable agent profile that best balances expected quality, cost, latency, access, and coordination overhead for the observed task.
_Avoid_: Cheapest model, most capable model, default worker

**Escalation Evidence**:
Observed ambiguity, conflicting findings, failed attempts, or elevated risk that justifies routing work to a more capable or expensive profile.
_Avoid_: Task importance, task size

**Routing Bootstrap**:
The first-time creation of an approved repository-specific routing contract and its justified executable agent profiles.
_Avoid_: Refresh, regeneration

**Routing Refresh**:
A delta-only reassessment of an existing routing contract after relevant capabilities, models, or repository evidence change.
_Avoid_: Reinstall, regeneration

**Managed Routing Block**:
A concise, automatically loaded section of repository instructions that maps task evidence to executable agent profiles.
_Avoid_: Project-team skill, roster document

**Exact Model Assignment**:
The explicit model and reasoning effort pinned by an executable agent profile and changed only through an approved routing refresh.
_Avoid_: Stable profile, beta profile, inherited model

**Global Execution Profile**:
A reusable executable agent profile whose cost, access, and responsibility apply across repositories and specialize through repository context.
_Avoid_: Generic expert, project team member

**Repository Context**:
The authoritative local instructions, decisions, boundaries, commands, and terminology that a global execution profile reads before working in a repository.
_Avoid_: Generated profile prompt, duplicated handbook

**Repository Context Preflight**:
An evidence-first check that determines whether routing can proceed, proposes only directly supported context additions, and exposes unresolved or conflicting boundaries.
_Avoid_: Architecture generation, documentation rewrite

**Repository-Specific Profile**:
An executable agent profile justified by a materially distinct local responsibility, access boundary, tool surface, or verification lane that global profiles cannot express cleanly.
_Avoid_: Framework persona, default project implementer

**Approval Surface**:
A concise decision-first view of proposed routing, attention-required changes, file deltas, and approval checks, with supporting evidence available on demand.
_Avoid_: Evidence dump, full inventory report

**Orchestrator**:
The current parent session that classifies work, selects execution profiles, integrates worker results, applies escalation rules, and makes final decisions.
_Avoid_: Required parent model, team manager profile

**Escalation Ladder**:
The bounded evidence-driven progression from a selected execution profile to a more capable profile when the orchestrator observes a concrete quality, ambiguity, or risk trigger.
_Avoid_: Automatic retry chain, worker self-promotion
