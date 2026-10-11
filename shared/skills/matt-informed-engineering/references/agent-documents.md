# Agent documents

**Use when:** an agent document repeatedly misses a branch or ends before its intended bound.

**Published method:** pinned [writing-for-agents](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents/SKILL.md) distinguishes pointers, steps, reference, and checkable completion criteria. Its [mechanics](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents/SKILL-MECHANICS.md) govern invocation and router behavior; the [official guide](https://www.aihero.dev/skills-writing-for-agents) explains the approach. No book attribution is asserted here.

**Local inference:** inspect the failed output and pointer before adding instructions. Distinguish an untriggered pointer, an unreached reference, and an unclear done condition. Change the smallest responsible passage and replay the failed branch plus one unaffected branch. Length alone does not locate the failure.

**Installed authority:** read `writing-for-agents` and its mechanics; they own authoring. This advisor diagnoses which question to take there, without duplicating its rules.

**Observable done:** the failed branch reaches the required behavior after the edit, and the comparison branch still succeeds, with outputs or actions recorded.
