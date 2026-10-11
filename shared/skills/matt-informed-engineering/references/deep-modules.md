# Deep modules

**Use when:** callers or tests must understand internals, or splitting code might spread complexity.

**Published method:** pinned [codebase-design](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/SKILL.md) judges depth by caller leverage, locality, and a public test surface; it expressly rejects an implementation-line/interface-line ratio.

**Published attribution:** [How To Make Codebases AI Agents Love](https://www.aihero.dev/how-to-make-codebases-ai-agents-love) explicitly credits John Ousterhout's *A Philosophy of Software Design*. The pinned skill's leverage framing is the applicable published behavior, not a claim that every detail comes from that book.

**Local inference:** compare two interface shapes by what callers can stop knowing and where a change would concentrate. More modules or larger files are not independently evidence of depth.

**Installed authority:** read `codebase-design` for vocabulary and design rules. Any architecture rewrite remains subject to the project's approval requirements.

**Observable done:** a concrete caller example and change scenario distinguish the alternatives, with the chosen observable test seam stated.
