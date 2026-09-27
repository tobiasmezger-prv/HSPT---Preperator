# Question import and sample review process

**Canonical creation and calibration policy:** [QUESTION_BANK_CREATION_PROCESS.md](../../QUESTION_BANK_CREATION_PROCESS.md), version 2.0. Use its Gables source pairings, already-seen-content exclusions, and source-key verification requirements. This file retains the original CLI workflow; a passing CLI gate alone does not complete the newer novelty or visual checks.

**Current accepted revision:** `gables-v2` replaced the two identified overlaps and passed the user-approved 20-question sample. Published release `quantitative-v0001` uses that revision. Older-bank commands below remain historical; use the v2 evidence workflow and [central publishing operations](../CONTENT_PUBLISHING.md) for new releases. The normal human review remains 20 per 100.

This replaces the earlier requirement to human-review every item. The normal human workload is **20 questions per 100**, after all-item automated checks and a content calibration audit. It is an editorial quality process, not a statistical guarantee or a claim that all 100 were individually reviewed.

## 1. Stage an immutable batch

Import a JSON array in the app’s question format into `content/imports/`. Work in complete batches of 100; the tool rejects a partial last batch instead of silently omitting it. Sort order does not affect fingerprints or sampling. Keep stable IDs; preserve completed-session snapshots. Do not automatically insert imports into the live bank.

Required content: ID, skill, provisional difficulty (1–3), template family, stem, four distinct choice strings, correct A–D key, explanation, shortcut. Record origin, author/license, and revision in the batch record. Use original authored or licensed content. Public visibility is not permission to republish a question. For the current batch, all items are original AI-assisted drafts, not copied source content and not human-approved.

## 2. Check all 100

- Structural gate: complete metadata, IDs, four choices, valid key, explanation/tip, and exact duplicate detection independent of choice order.
- Mathematical gate: independently recompute the answer from the stem; evaluate every choice under the rule; require exactly one correct choice. Fractions/percentages require semantic equality checks. Classification items may deliberately have equivalent wrong values, but still exactly one qualifying correct choice.
- Check sequence rules across all supplied terms, not just the last step. For diagrams, check labels, geometry, rendering, and every offered relationship. For approximate answers, state rounding explicitly.
- Review plausible distractors and alternate interpretations. Automated arithmetic cannot prove arbitrary natural-language questions unambiguous.
- Verify answer-position balance, near-duplicate families, category coverage, and no repeated IDs within sessions. The current bank also exercises ten bursts without repeats.

**Implementation boundary:** `bank_pipeline.py` is a generic structural/sampling gate, not a universal math solver. Each new batch needs executable, content-specific independent checks and a checksum-bound math receipt. `check-current-bank.py` issues a receipt only after the existing 100-item arithmetic tests pass. Do not reuse that receipt or its oracles for a different batch. New item types require new validators. The receipt is a local audit artifact, not a cryptographic third-party attestation.

Receipt format: `bankHash`, `status: "passed"`, all `checkedIds`, plus the test command and method. Compute the hash with `bank_pipeline.bank_hash`. A failed or missing check blocks acceptance. Never fill a receipt by simply copying the answer key into an oracle.

## 3. Calibrate every item against references

Use the publisher for category scope and Gables Tutoring’s three linked tests with their correctly paired answer guides as the preferred calibration source. The underlying publications include two authors; use other public examples as secondary checks. Follow the canonical document’s source register and inspect both prompts and solutions. Inspect actual prompts; do not rely only on search snippets. Record URLs, page/heading locators, limits, and a short per-item assessment. Do not equate third-party practice items with secure official exam items.

For each item record: `id`, `questionHash`, `format`, `alignment` (close/partial/supplemental), `risk` (1–4), current/recommended difficulty, `note`, reference IDs, and `disposition` (retain_for_skill_practice/reject). Audit JSON includes `bankHash`, `sources`, and `items` covering every ID. A changed question invalidates the old audit and math receipt.

Difficulty rubric (editorial, not empirical):

- **1:** Familiar one-step operation or explicit short rule; minimal translation.
- **2:** Pattern inference, two-step manipulation, or comparing unlike representations.
- **3:** Interleaved/combined rules or meaningfully multi-step reasoning, not merely large numbers or unfamiliar symbols.

Flag when a question gives away a rule it is meant to test, when a purported hard item is routine substitution, or when an important format is absent. Keep a revision backlog. Accuracy and time from later practice can refine labels; do not infer HSPT percentiles.

The current audit flags missing figure-based comparison and relational answer formats. Sample approval can accept the bank **for skill practice** while acknowledging those limitations. It cannot certify a full-test simulation.

## 4. Generate a fixed 20-item sample per 100

The executable sampler uses:

1. Proportional skill quotas, minimum one per present skill.
2. Coverage of available difficulty levels and at least one geometric comparison where present.
3. A high-risk item within each skill.
4. Seeded picks for remaining slots, preferring distinct template families.

The seed derives from the full bank revision and policy version. Rerunning the same content gives the same sample; reordering the input does not change it. Changed content changes the revision and requires fresh checks. No easy-item substitutions or discretionary cherry-picking. For 200 questions, there are two 100-item groups and 40 reviews. The current sample is exactly 20, with all six skills, all three difficulty levels, and a geometry item.

The tool produces a questions-first Markdown packet with a separate answer/explanation section, a sample manifest, and `decisions.json`. Existing reviewer decisions are never overwritten on rerun. A fresh template is emitted separately.

## 5. Human review: solve, then inspect

For each of the 20, the reviewer solves before checking the answer. Check mathematical correctness, unique defensible answer, clear wording, realistic difficulty, explanation, and tip. Record approve/revise/reject with notes, reviewer name, and date. A parent can review usability and clarity; a math educator is helpful for doubtful content. Nobody needs to review all 100 as the default workflow.

- **No defects:** mark all 20 approved and acknowledge the calibration limitations.
- **Typo or clarity issue:** repair it, rerun checks, and re-review the affected content and regenerated sample. Do not silently carry an approval across changed wording or choices.
- **Wrong key, ambiguity, faulty explanation, or diagram error:** block the batch. Inspect every item sharing the affected family/rule, fix it, and add regression checks. After repair, regenerate the fixed sample and review it. Expand only the affected family initially.
- **Multiple unrelated defects:** reject or rebuild the batch. A larger human review may then be necessary; “20” is the normal checkpoint, not permission to ignore known defects.

A sample can miss isolated defects. This deliberately stratified, risk-weighted sample has no simple binomial confidence claim. After acceptance, continue reacting to reported issues and quarantining faulty items.

## 6. Accept and integrate explicitly

Accepted status is **sample_reviewed_for_skill_practice**. Individually sampled approvals and batch-level acceptance are separate. The other 80 must not be marked individually human-approved. Keep item provenance and review history, archive the accepted revision, and integrate only after the acceptance gate passes. Session snapshots keep past grading reproducible.

The CLI stages reports only. It does not deploy, alter the app bank, or grant official-exam status. Runtime status labels remain pending until integration is explicitly performed.

## Commands

Run from the `app` directory with Node dependencies installed and Python 3 available.

```sh
# Current-bank export, per-item audit, and executable mathematical checks:
python3 scripts/check-current-bank.py

# Prepare the packet and show current gate status:
python3 scripts/bank_pipeline.py content/imports/current-100.json \
  --evidence content/calibration/current-100.math.json \
  --audit content/calibration/current-100.audit.json \
  --output content/review/current-100

# After a human fills decisions.json, require actual acceptance:
python3 scripts/bank_pipeline.py content/imports/current-100.json \
  --evidence content/calibration/current-100.math.json \
  --audit content/calibration/current-100.audit.json \
  --output content/review/current-100 \
  --decisions content/review/current-100/decisions.json --require-accepted

# Exercise the generic gate and sampler:
python3 -m unittest discover -s scripts -p 'test_bank_pipeline.py'
```

For a future bank, supply its own JSON, mathematical receipt, and editorial audit to the same CLI, using a new output folder. `--require-accepted` exits nonzero until all gates and all sampled human decisions pass. On this machine only, set `HSPT_NODE` to the bundled Node executable when invoking the current-bank checker if Node is not on PATH.

## Phase II publication boundary

Use `scripts/content-release.mjs` after acceptance. A browser never imports an authoring directory automatically. The publisher requires checksum-bound mathematical, item-level editorial, visual and overlap evidence plus the approved sample manifest/decisions. It preserves separate batch acceptance and individual-review metadata, emits complete immutable releases, and refuses collisions without explicit revisions. See [CONTENT_PUBLISHING.md](../CONTENT_PUBLISHING.md) for exact v2 input files and build/validate/preview/publish/rollback commands. The old `bank_pipeline.py` receipts alone do not meet this release gate.
