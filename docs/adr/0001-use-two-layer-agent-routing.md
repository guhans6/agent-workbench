---
status: accepted
---

# Use two-layer agent routing

Agent Workbench will separate reusable global execution profiles from repository-specific context and exceptional local profiles. The orchestrator will select the best-value profile from an automatically loaded routing contract, then specialize that worker through repository instructions and composable skills. This avoids duplicating general engineering expertise in every repository while preserving local architecture, safety, tooling, and verification boundaries. Repository-local profiles are created only when a materially distinct local lane cannot be expressed cleanly by global profiles plus repository context.
