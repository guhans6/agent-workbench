# Checkpoint bundle qualification — issue #15

Scope: locally adapted skills and a shared reference in agent-workbench. This is an isolated document-loaded pilot, not proof of automatic host discovery or universal compliance. Existing repository delivery rules govern their own projects; this repository has no separate root delivery agreement, so these boundaries are reported explicitly.

## Reproduce focused package checks

Run `python3 scripts/verify-checkpoint-assets.py`. It checks selected metadata, catalog presence, local references and saved upstream baseline/license integrity, stages the complete bundle into a temporary installation and rejects a missing-workflow installation. It never installs into an active host or changes project/global instructions. Parse catalog/frontmatter YAML separately using an available YAML parser.

For behavioral checks, use isolated fixtures and the approved task. Record original prompts, loaded contracts, artifacts and public proof before reviewing expected scenario outcomes. Static text checks cannot substitute for observed behavior. After a material change rerun only affected scenarios. Advisor scenarios are defined in [the package](../skills/matt-informed-engineering/evals/scenarios.md).

## Observed pilot: checkpoint execution

GPT-6.1 Sol was explicitly given the draft implement skill and an isolated Python CLI fixture. Approved scope: preserve existing text output, add available-file JSON and missing-file JSON through the public CLI, no network/install/full-suite/commit. The agent recorded the runnable baseline, proved the available-file increment before the missing-file increment, corrected observed missing-file failure and finished the text regression without asking the human to continue between checkpoints.

Observed public proofs: available JSON contains absolute path, `status: available` and exact Markdown; missing JSON contains absolute path and `status: missing`, exits 1 with no stderr; original text output is exact. The agent retained source artifacts, hashes and an incremental checkpoint record. Parent read the record and reran the focused checker. This demonstrates the explicit-loaded pilot only, not general adherence or a causal comparison with an older project.

## Observed pilot: failure and resumption

A second approved CLI delta required a project name from an externally supplied JSON fixture. With that input absent, the agent left the proven CLI unchanged, reran its existing checks and retained a handoff naming the missing evidence, next owner and exact resume condition. After the parent supplied `{"name":"pilot-workspace"}` and directed resumption, the agent verified the previous artifact hash, proved the added project field and preserved missing-file/text behavior. Parent reran the final CLI checker: all three public checks passed. An agent check from another working directory also passed.

Final fixture CLI SHA-256: `c2fced8dad842bec7b5741fc55b25d878ea346061cad672c07cd1cf91b200b94`. Authoritative JSON input SHA-256: `f5aafdf2d9ed81c4c195d544c5f8d686cb166ba465d366c8afbee14cab10f9ec`. This is a local missing-input handoff/resumption pilot, not a production process-restart or ambiguous external-Send replay test.

## Observed pilot: project setup

The explicit-loaded setup pilot began with existing CLAUDE.md, local issue tracking, a single-context domain guide and delivery authority. Triage was deliberately absent from the pilot catalog. The agent first produced an exact two-file preview and stopped without fixture writes. After parent approval, it rechecked original/source bytes, added one checkpoint pointer and the protocol copy, read back both paths and verified preserved tracker/domain/glossary/delivery files. It created neither AGENTS.md nor triage labels. A static identical-rerun simulation found zero candidate changes and identical file hash maps; this was not a second model invocation.

Source protocol SHA-256: `40d2c19b90c6cfc28a6c1cb375398b84433810d8e067d4fb27428ba0cc4de969`. Project copy SHA-256: `f33e67e534c6a4ef9b708dfc5c197ef2e7fe2e3e801e8b407f7d431dd8e40e2e`. Provenance accurately describes uncommitted source bytes rather than claiming HEAD represents the draft. These changes affected only a temporary fixture, not another project or global instructions.

## Observed pilot: Matt-informed advice

Three explicit document-loaded requests were run on GPT-6.1 Sol before reading their evaluation answers:

| Scenario | Observed result |
| --- | --- |
| A2: backend files complete, user path unproven | Named one complete path, integration gap, public proof and source. Initial output omitted the required credited book authors, so the original run failed that scenario. A narrow instruction change requires the credited book/authors when selecting a book-backed principle. One confirmation replay passed with Hunt/Thomas attribution; original failure was preserved. |
| A8: unsupported personal framework preference | Left Matt's preference unverified, labeled local inference and proposed bounded evidence gathering; no invented preference or execution. Passed for observed advice. |
| A9: upstream full-suite/commit conflicts with local focused-only/source-edit scope | Chose the available focused public CLI proof, retained local authority and separated delivery boundaries; no full suite or commit. Passed for observed advice. |

The remote pinned TDD page could not be fetched during the pilot; the advice relied on actual installed TDD text and the already researched local source card, with that limitation recorded. The pilot does not independently reverify every remote source. All recommendations and the original failed A2 output were retained before evaluation/replay. No comparative baseline was run, so improvement over ask-matt plus writing-for-agents remains unknown.

## Package and review evidence

The Python verifier passed metadata/reference/catalog checks, recorded upstream baseline hashes and license checks, complete temporary installation and incomplete-install rejection. Ruby YAML parsing additionally checked the catalog and four selected skill metadata documents; parsed catalog descriptions and invocation policies matched the actual skill files. `git diff --check` passed.

Independent Standards and Spec read-only reviews found no actionable findings in the implementation. Final evidence review is recorded separately during publication. Reviews do not establish host discovery or universal model adherence.

## Remaining boundaries

No production host installation, global instruction update, unrelated project adoption, automatic discovery trace, old-versus-new comparison, credential/CAPTCHA behavior, live ChatGPT Send, or long-running external budget qualification is established. Other advisor scenarios are not run. Successful structural checks and bounded pilots do not guarantee future compliance. Source publication and any subsequent installed-host verification remain separately reported.
