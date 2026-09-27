# HSPT question-bank creation, calibration, and import process

**Project:** HSPT Practice  
**Version:** 2.0 — Gables calibration added  
**Purpose:** Create original, dependable quantitative practice in batches of 100, with a normal human-review workload of 20 questions per batch.

This is the reusable project instruction. It supersedes the earlier requirement to human-review all 100 questions. Keep source documents under `sources/` read-only. Do not publish new content or label it approved merely because it passes arithmetic tests.

## 1. Non-negotiable principles

- Use Gables Tutoring’s linked HSPT practice tests **and their matching answer explanations** as the preferred calibration reference for this family. The student has already completed these tests.
- Calibrate the reasoning task, presentation, difficulty range, distractor design, and explanation quality. Do not copy stems, answer choices, figures, explanations, or create recognizable reskins by changing only numbers or names.
- Original questions may test the same mathematical concept. Novelty means a fresh problem, not inventing an unfamiliar question format.
- Check every item automatically where a reliable validator exists, then human-review a fixed sample of 20 per 100. Automated checks do not establish natural-language clarity or real-exam difficulty.
- Treat publisher guidance as authoritative for section scope. Treat third-party practice tests as valuable examples, not current official exam forms or infallible answer keys.

## 2. Calibration source register

Start at [Gables Tutoring’s practice-test page](https://gablestutoring.com/practice-tests/). **The webpage labels, PDF filenames, and printed book test numbers differ. Use the pairings below rather than guessing from a filename.**

| Webpage label | Question PDF | Matching answer PDF | Quantitative question location |
|---|---|---|---|
| Test 1 | [HSPT-Test-3.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-Test-3.pdf) | [HSPT-TEST-3-Answers.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-3-Answers.pdf) | Q61–112; PDF pp. 6–11, printed pp. 188–193 |
| Test 2 | [HSPT-TEST-4-1.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-4-1.pdf) | [HSPT-TEST-4-Answers.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-4-Answers.pdf) | Q61–112; PDF pp. 6–11, printed pp. 448–453 |
| Test 3 | [HSPT-TEST-5.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-5.pdf) | [HSPT-TEST-5-Answers.pdf](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-5-Answers.pdf) | Q61–112; PDF pp. 6–11, printed pp. 246–251 |

Page numbers above are one-based. The first and third PDFs identify *Catholic High School Entrance Exams For Dummies*; the middle scanned test identifies Peterson’s. Gables is the hosting/curation source, not necessarily the original author.

For scope, also consult [STS’s HSPT interpretive manual](https://www.ststesting.com/hp_int_sts.pdf), printed page 1. Use other reputable examples to resolve uncertainty, not to overrule a mathematical inconsistency.

Record source URLs, webpage labels, actual document titles, question/page locators, access date, and any exclusions. If a PDF is scanned or uses diagrams, visually inspect the page. OCR or extracted text can lose symbols, superscripts, fractions, shading, or subscripts. Never reconstruct a question from broken extraction and then call it validated.

## 3. What the Gables comparison changes

The quantitative sections and paired guides were inspected for calibration, including visual inspection of the scanned test and selected diagrams. This was not an exhaustive independent certification of all reference answer keys.

For our next revision:

- Preserve short prompts and a range from straightforward to multi-step reasoning. Do not make every question complicated just to imitate test difficulty.
- Expand labeled-quantity comparisons with relational answer choices. Four separate values with “which is largest?” do not cover the whole format.
- Include original figure-based comparisons, shaded fractions, and graph interpretation; text-only area calculations are insufficient substitutes.
- Add selected missing-term, multi-term-output, and mixed-representation sequences. Do not supply the rule when discovering it is the tested skill.
- Include concise verbal manipulation where the student must translate the relationship and finish every requested operation.
- Explanations should justify the answer and identify a likely mistake. Tips should teach a valid shortcut, not merely repeat the calculation.

These are editorial design conclusions, not measured official blueprint percentages or psychometric difficulty estimates.

### Reference exceptions and existing-bank overlap

The source guides are useful but still need verification. In webpage Test 3, Q87, the printed sequence supports an alternating halving/addition rule, while the matching explanation applies subtraction and selects a different option. Treat this as an apparent source inconsistency, not a template to reproduce. Its Q89 also relies on representation to distinguish equal numerical values; our questions must explicitly request the representation if it matters. See the [question PDF, p. 9](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-5.pdf#page=9) and [answer guide, p. 6](https://gablestutoring.com/wp-content/uploads/2020/08/HSPT-TEST-5-Answers.pdf#page=6).

Two existing local items need replacement before a fresh bank is released to this student:

| Local ID | Reference overlap | Required action |
|---|---|---|
| `dev-03` | Webpage Test 1, Q68: same starting doubling sequence, though the requested output length differs | Replace with an independently designed item, not an extended/truncated version. |
| `quant-038` | Webpage Test 3, Q75: same starting fractional progression with an extra term | Replace; extending a familiar sequence is not sufficiently fresh for this student. |

These are identified overlap risks, not a claim that the prior drafts were copied. The mathematical concepts remain usable. The audit does not prove that these are the only possible similarities. Complete the novelty check below for every revised batch.

**Current state:** this process update does not change the app’s 100 questions or mark them approved. The prior automated checks remain mathematical checks, not evidence that these newly identified issues are resolved.

## 4. Plan the batch before writing

Create a batch record with an ID, version, purpose, source register, and proposed distribution. Distinguish **skill practice** from **exam-style practice**.

For an exam-style quantitative bank, cover number series, number manipulation, nongeometric comparison, and geometric/visual comparison. Keep custom-symbol and odd-one-out drills separately labeled as supplemental unless their specific form is supported by calibration evidence. Do not give all existing app skill tags equal exam weight by default.

A starting editorial allocation may be 34 series, 32 manipulation, 18 nongeometric comparisons, and 16 geometric/visual comparisons per 100. This is a proposal for this product, not an official HSPT distribution or a counted Gables blueprint. Change it when justified by a documented reference census and learner needs.

Set a difficulty mix that includes foundation, intermediate, and stretch items. Rate reasoning, not just number size:

| Level | Working definition |
|---|---|
| 1 — Foundation | Familiar operation or short straightforward pattern; little translation. |
| 2 — Intermediate | Infer a pattern, translate a relationship, compare representations, or complete two linked steps. |
| 3 — Stretch | Interleaved/combined rules, several dependencies, or nontrivial visual/relational reasoning. |

Difficulty labels remain provisional until observed student performance supports them. Approximate attention time is not exact solving time. Do not infer HSPT scores or percentiles from this bank.

## 5. Author original questions and solutions

1. Extract a **skill brief** from the reference: reasoning demand, presentation, prerequisite knowledge, likely misconception, and answer format. Record its locator, not its full text.
2. Put the reference aside and author a fresh problem from that brief. Do not generate one altered copy per reference item.
3. Solve the new problem before writing distractors. Write the full derivation and a second check where feasible.
4. Create four distinct choices, with exactly one defensible answer. Map each wrong choice to a plausible mistake, such as stopping early, reversing an operation, or comparing mismatched units.
5. Write a concise original explanation and a valid mental shortcut. Check that the shortcut does not depend on an unstated condition.
6. For sequences, check the rule against every given term and plausible competing simple rules. For multiple requested terms, check the entire answer tuple.
7. For diagrams, author new geometry; specify necessary equalities, angles, scale assumptions, and units. Do not trace source figures. Ensure labels remain readable on iPad and the accessible description preserves the problem without revealing its answer.
8. Review wording for middle-school readability. Keep intentional reasoning demand; remove accidental linguistic ambiguity.

Each item needs: stable ID, section, skill, format subtype, provisional difficulty, template family, stem, four choices, correct choice, explanation, shortcut, provenance, and pending review status. Visual items also need an asset/diagram specification and accessible description. Record calibration references separately from authorship provenance.

## 6. Run the already-seen and originality check

For **every** item, compare against the current app bank and all three Gables quantitative sections:

- Exact and normalized text overlap, disregarding superficial formatting.
- Same sequence prefix, slightly extended/truncated sequence, same relationship structure with the same values, or reordered choices.
- Recognizable problem skeleton plus only a number/name swap.
- Reused figure geometry, arrangement, labels, or shading pattern.
- Copied explanation or distinctive wording.

Automated similarity flags are triage, not an originality verdict. Generic wording and common mathematical operations alone are not copying. A substantive match to a question this student already encountered requires replacement or explicit quarantine; do not simply dismiss it because the correct letter changed.

Keep an overlap log: local ID, reference locator, match reason, resolution, and reviewer/checker. Any unresolved overlap blocks release for this student, even when the item is mathematically correct.

**Implementation limit:** the current import tool does not automatically crawl Gables, compare diagrams, or detect semantic reskins. Until those capabilities exist, document this as an agent-assisted content check. Do not describe an unperformed similarity check as passed.

## 7. Validate all 100 before sampling

Require complete metadata, four valid choices, stable unique IDs, no duplicate items, and a matching explanation and key. Evaluate every choice rather than checking only the declared correct answer.

Use independent arithmetic oracles, exact fractions where appropriate, sequence validators, truth tables for relational choices, and geometry assertions. Any new format needs a suitable validator. Equal numerical choices are unacceptable when the question asks only for a numerical value; if representation is the skill, state the required representation explicitly.

Check family repetition, answer-position balance, skill coverage, and ten-question selection. Ensure the app can render and grade the new formats without revealing answers during practice. Visual QA is mandatory for diagrams and mathematical typography.

Keep separate records for structural checks, mathematical checks, calibration, novelty, visual checks, and human review. Bind results to the content revision. A change to the stem, choices, key, explanation, or diagram requires renewed relevant checks; old receipts must not certify edited content.

Do not use a reference answer guide as the sole oracle. Recompute the result, compare it with the guide, and log disagreement instead of propagating it.

## 8. Human review: 20 per 100

After full-bank checks, generate a fixed sample of exactly 20 for each 100-item batch. Use reproducible skill-stratified selection, difficulty coverage, risk-based picks, and diversity of pattern families. Cover each new answer/visual format. Include geometry when it is present. Do not choose only polished or easy items.

The existing sampler covers skills and difficulty, prioritizes risk, and includes geometry. It does **not** yet guarantee every future renderer or format subtype. Before review, check the manifest against the batch’s format inventory; revise the sampling policy and regenerate if a new format is omitted. Never hand-swap inconvenient questions while retaining the old manifest.

Provide a questions-first packet with a separate key/explanation section. The reviewer solves first, then checks correctness, clarity, uniqueness, difficulty, explanation, tip, and rendering. Record approve/revise/reject, notes, reviewer name, and date.

- With no defects and all other checks complete, accept the batch as **sample-reviewed** for its stated purpose.
- A typo or clarification requires correction and renewed checks/review of affected content.
- A wrong key, ambiguity, invalid tip, diagram error, or source overlap blocks acceptance. Inspect and repair the entire affected family; do not automatically require all 100 to be reviewed.
- Multiple unrelated defects can justify rejecting the batch or expanding review.

Twenty is the normal human checkpoint, not a guarantee of zero defects. Do not call the other 80 individually human-approved or claim a statistical confidence level for this deliberately stratified sample.

## 9. Import and release deliberately

Stage new batches outside the live question bank. Preserve past sessions through immutable question snapshots or versioned content. Integrate only after all required checks are complete and known issues are resolved.

Keep these meanings separate:

- **Draft:** authored, checks incomplete.
- **Automatically checked:** required executable checks passed for this revision.
- **Sample-reviewed:** the required human sample passed; unsampled items are not individually approved.
- **Ready for stated use:** calibration, originality, rendering, review, and app integration checks passed.

The existing CLI acceptance label is `sample_reviewed_for_skill_practice`; it does not certify an exam simulation. Its gate does not yet enforce the new Gables novelty and visual checks. Those documented checks remain mandatory before release. Do not deploy automatically as part of content authoring.

## 10. Required deliverables for every batch

- Versioned original bank with keys, explanations, tips, and any visual assets.
- Source register and compact format/difficulty calibration report.
- Item-level audit and source-overlap log, including resolution of all flags.
- Mathematical and structural check receipts tied to the revision.
- Visual/rendering results, when relevant.
- Reproducible 20-item sample, questions-first packet, and human decisions.
- Final acceptance record stating permitted use and unresolved limitations.

## 11. Existing project commands

From `app/`, with Python 3 and Node dependencies installed:

```sh
# Recheck and export the existing bank. This does not perform the new Gables
# novelty/diagram review; complete and record those separately.
python3 scripts/check-current-bank.py

# Prepare the reproducible sample using its matching receipt and audit.
python3 scripts/bank_pipeline.py content/imports/current-100.json \
  --evidence content/calibration/current-100.math.json \
  --audit content/calibration/current-100.audit.json \
  --output content/review/current-100

# Require sampled human approval after decisions have actually been recorded.
python3 scripts/bank_pipeline.py content/imports/current-100.json \
  --evidence content/calibration/current-100.math.json \
  --audit content/calibration/current-100.audit.json \
  --output content/review/current-100 \
  --decisions content/review/current-100/decisions.json --require-accepted
```

For a new batch, supply its own bank, independent tests/receipt, audit, and output folder. Never reuse another batch’s mathematical oracle or approval record. The current calibration export is bank-specific and is not a substitute for re-reading changed sources.

## Reusable instruction for a future session

> Follow this document to create or import the next 100 original HSPT Quantitative practice questions. Use Gables Tutoring’s linked tests and matching explanations for calibration only; the student has already seen them. Do not copy, lightly reword, or merely change numbers in those questions. Preserve the approved app UX. Plan the format and difficulty mix, author and independently validate all items, check overlap against Gables and the existing bank, inspect new visual formats, and produce a reproducible 20-question human-review sample. Report what was actually checked and keep the batch pending until its required checks and human decisions pass. Do not deploy or claim official-test equivalence.

## First 100: staged Gables revision and updated sample

The `gables-v2` revision is now staged in `app/content/staging/gables-v2/`. It retains and rechecks 47 prior questions and replaces/adds 53. The 20-question review packet is at `app/content/review/gables-v2/REVIEW_20.html` (portable, diagrams included); a Markdown-plus-assets ZIP is alongside it. See the staged `REPORT.md` for the actual checks and remaining gates. The live bank remains unchanged.

The new fixed sampling policy uses **6 series / 6 manipulation / 4 numerical comparison / 4 visual**. Prespecified risk picks include both source-overlap replacements, a missing term, a letter-number output, and all four diagram types. Remaining slots use content-hash-seeded selection with foundation coverage. The manifest verifies all difficulty levels, answer formats and distinct families. This supersedes the old skill-only sampler **for this staged revision**.

From `app/`:

```sh
# Recheck all staged answers; exercise mutation tests that must reject bad content.
python3 scripts/gables_v2/validate.py
python3 scripts/gables_v2/test_validation.py

# Regenerate the identical sample, preserving actual human decisions.
python3 scripts/gables_v2/package_review.py

# Report the content/review gates; this does not approve, integrate or deploy.
python3 scripts/gables_v2/gate.py
python3 scripts/gables_v2/gate.py --require-reviewed
```

`--require-reviewed` intentionally fails until the 20 decisions, reviewer and date are recorded. The packet generator requires matching, separately recorded editorial and visual evidence; it must not re-certify changed questions automatically. `author.py` and `render.py` reproduce this particular authored batch, **not arbitrary future question imports**. For a changed/new batch, repeat the source comparison and visual inspection, update independent mathematical proofs, use a new revision folder, and generate fresh evidence and decisions. Never edit an evidence hash merely to bypass a failed check.

App rendering of the new diagram specifications, ten-question selection across the revised mix, scoring integration, and iPad verification remain release gates. Static diagram inspection and mathematical validation do not substitute for them.

### Integration update

Tobias explicitly approved the gables-v2 sample and authorized integration. The live app now imports this immutable revision; batch status is sample-reviewed (not individual approval of all 100). Diagrams render in practice and results, retired focuses are hidden, and older saved snapshots remain supported. Automated integration checks and production build passed; see `app/content/staging/gables-v2/integration.json`. Manual browser/iPad verification remains pending. No deployment was performed.
