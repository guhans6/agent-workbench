# Red → green

**Use when:** a concrete behavior needs trustworthy tests and its public seam is agreed.

**Published method:** pinned [tdd](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md) uses one failing test and minimal implementation at a time, observed through public interfaces. Expected values require an independent source.

**Version boundary:** the [current guide](https://www.aihero.dev/skills-tdd) says refactoring moved to review in June 2026. The [February article](https://www.aihero.dev/skill-test-driven-development-claude-code) describes the older red-green-refactor cycle. Read the installed `tdd` and apply its contract plus repository rules; report a material difference instead of silently mixing versions.

**Attribution limit:** the upstream README references Kent Beck's *Extreme Programming Explained* for continual design investment. That does not establish *TDD by Example* as this skill's source.

**Local inference:** select one worthwhile behavior example with an independently specified expected result, then use the smallest authorized focused check.

**Installed authority:** `tdd` governs seam agreement and the loop; `code-review` governs review-stage refactoring. This card creates neither a new seam approval nor a broader test gate.

**Observable done:** recorded red and green results demonstrate the agreed behavior at the public seam, within local verification scope.
