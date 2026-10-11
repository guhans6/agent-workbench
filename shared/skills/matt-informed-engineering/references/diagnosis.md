# Diagnosis

**Use when:** the bug resists inspection or keeps returning after plausible fixes.

**Published method:** pinned [diagnosing-bugs](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/diagnosing-bugs/SKILL.md) prioritizes a tight signal for the user's exact symptom before hypotheses, then minimizes, probes falsifiable predictions, and checks the fix. No book attribution is asserted here.

**Local inference:** if no command or captured signal can distinguish the broken behavior from success, that missing signal is the next task. A nearby assertion such as “did not crash” is inadequate when the reported symptom is incorrect output. For intermittent failures, identify a bounded, reproducible trigger and measured failure rate.

**Installed authority:** read `diagnosing-bugs`; its actual diagnostic phases and local resource/verification limits govern execution.

**Observable done:** one bounded check has already captured the exact symptom and reports its verdict and reproduction conditions. Until then, recommend evidence collection rather than another speculative fix.
