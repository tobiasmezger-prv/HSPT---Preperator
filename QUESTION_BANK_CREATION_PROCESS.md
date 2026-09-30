# HSPT question-bank creation, calibration, and import process

**Project:** HSPT Practice  
**Version:** 3.1 — Phase IV source-import sampling exception  
**Purpose:** Create original, dependable practice for all five HSPT sections in batches of 100, using full-set source calibration and independent answer review of every authored question. The normal human-review checkpoint remains 20 questions per batch.

This is the reusable project instruction. It supersedes the earlier requirement to human-review all 100 questions. Keep source documents under `sources/` read-only. Do not publish new content or label it approved merely because it passes arithmetic tests.

## 1. Non-negotiable principles

- Use the project source [HSPT_ALL_SIX_PDFS.md](sources/HSPT_ALL_SIX_PDFS.md), containing all three complete Gables tests and matching answer guides, as the primary calibration reference. Calibrate against **all 894 source questions across all five sections and all six documents (156 pages)**, not a selected sample. The student has already completed these tests.
- Calibrate the reasoning task, presentation, difficulty range, distractor design, and explanation quality. Do not copy stems, answer choices, figures, explanations, or create recognizable reskins by changing only numbers or names.
- Original questions may test the same mathematical, verbal, reading or language concept. Novelty means a fresh problem, not inventing an unfamiliar question format.
- Check every item automatically where a reliable validator exists, then human-review a fixed sample of 20 per 100. Automated checks do not establish natural-language clarity or real-exam difficulty.
- Treat publisher guidance as authoritative for section scope. Treat third-party practice tests as valuable examples, not current official exam forms or infallible answer keys.

## 2. Calibration source register

Use [the combined Gables Markdown file under project sources](sources/HSPT_ALL_SIX_PDFS.md), **not the website as the normal starting point**. Treat this file as read-only reference material. Its embedded original page images are part of the calibration source, alongside the searchable transcriptions.

**Local sync note (2026-09-27):** the user added the file to project sources, but it was not yet visible in this local mirror when this instruction was updated. Until it syncs, the identical generated artifact is available at [output/markdown/HSPT_ALL_SIX_PDFS.md](output/markdown/HSPT_ALL_SIX_PDFS.md). Prefer the `sources/` copy once available. If its synced filename differs, locate it by title and the six-document contents below and record the actual path. Do not silently substitute a website sample or claim to have read an unavailable source.

### Document identities and full coverage

The source retains the Gables Test 1/2/3 labels, original filenames, document headings and one-based PDF page markers. These labels differ from the printed book test numbers.

| Source label | Question document | Matching answer document | Pages, questions + answers |
|---|---|---|---:|
| Test 1 | HSPT-Test-3.pdf | HSPT-TEST-3-Answers.pdf | 34 + 20 |
| Test 2 | HSPT-TEST-4-1.pdf | HSPT-TEST-4-Answers.pdf | 31 + 18 |
| Test 3 | HSPT-TEST-5.pdf | HSPT-TEST-5-Answers.pdf | 33 + 20 |

The first and third pairs identify *Catholic High School Entrance Exams For Dummies*, printed Tests 1 and 2; the middle pair identifies Peterson’s Practice Test 5. Gables hosted the references, but is not necessarily their author. Website URLs may be retained as historical provenance, not substituted for the project source.

| Section | Question numbers in each test | Items across all three tests |
|---|---|---:|
| Verbal Skills | 1–60 | 180 |
| Quantitative Skills | 61–112 | 156 |
| Reading | 113–174 | 186 |
| Mathematics | 175–238 | 192 |
| Language | 239–298 | 180 |
| **Total** | **298 per test** | **894** |

Record the actual Markdown path, content hash, document identity, PDF page heading and question number for each reference. Bind the coverage ledger and calibration findings to that source revision. Inspect every question, all choices, each passage/figure and its matching explanation. Include all answer-guide pages, not only summary key tables. Coverage may be reused from a documented full review only when its source hash matches; reconcile and re-review changed or previously unresolved material. Never relabel partial or sampled coverage as full calibration.

For official section scope, retain STS publisher guidance as the authority; the [STS interpretive manual](https://www.ststesting.com/hp_int_sts.pdf) is a supplemental scope reference, not a substitute for the complete project Gables corpus. The three practice forms do not establish the current official blueprint or measured difficulty.

### Embedded images, OCR and source defects

The Markdown includes page images in expandable HTML blocks with embedded image data. Use them to inspect diagrams, fractions, superscripts, shading and other notation that transcription may lose. If a reader cannot display them, decode the embedded images into temporary working files and inspect those. Do not treat a text search or an unread image as visual review.

Some words and variables are absent even in the original second test. The Markdown preserves published errors and flags known problems; it is not a corrected key. Record missing, ambiguous or contradictory material as an exception. Never invent missing text or use a suspect published answer as the sole oracle. Separate complete inspection from successful verification: every source position must be accounted for, but an unreadable position cannot be marked verified.

## 3. Full-set calibration and known findings

The [full audit](app/content/audits/gables-full-2026-09-27/REPORT.md) covers all three tests and answer guides, all five sections, 894 source positions and 500 local questions. Consult its [source coverage](app/content/audits/gables-full-2026-09-27/source-coverage.json), [exceptions](app/content/audits/gables-full-2026-09-27/source-exceptions.json) and [local item audit](app/content/audits/gables-full-2026-09-27/local-item-audit.json). This historical audit was tied to the original PDF hashes; record the matching Markdown hash and reconcile its document/page contents before reusing that evidence for a new batch. It is not human acceptance or infallible certification.

For each new batch, use the complete corpus to establish the format, reasoning, distractor and explanation requirements, then compare every authored item with all relevant source items and the other local banks. Do not calibrate a section from a few representative pages or the 20-question human sample. Maintain a complete corpus ledger across all five sections even when authoring only one section.

| Section | Full-set calibration requirements |
|---|---|
| Verbal | Cover synonym/antonym distinctions, analogy direction, classifications and logical entailment. Check word sense and all plausible alternatives; avoid source-exposed targets and recognizable logic reskins. |
| Quantitative | Cover series, manipulation, numerical relationships and visual/geometric comparison. Include missing terms, multi-term outputs and mixed representations where supported. Check every supplied term and every relational option. |
| Reading | Each reference form has 40 comprehension and 22 standalone vocabulary items. Include a suitable mix of passage genres, lengths, inference, purpose, evidence and vocabulary. All-passage questions with uniformly short texts do not cover the observed format. Preserve complete passage groups in test assembly. |
| Mathematics | Include computation, concepts, application and original figure-based tasks. Text-only geometry is insufficient to cover the reference presentation. Independently solve every problem, checking units, assumptions and all choices. |
| Language | Each reference form has 40 sentence-error items, 10 spelling and 10 composition items. Include genuine no-error options and paragraph editing. Check standard written usage without reproducing overly rigid or incorrect source-guide rules. |

These source counts inform editorial design; they are not mandated percentages for every 100-item skill bank. Document any deliberate departure and label its permitted use accurately. Difficulty labels remain provisional until supported by student performance.

Known findings include wrong or conflicting source keys, multiple valid choices, missing printed content and overgeneralized explanations. For example, Test 3 Q87 has a sequence/key disagreement, Q89 has equal numerical options, and Test 2 Q162 has a vocabulary-key disagreement. Use the exception ledger for their locators and reasoning rather than copying those defects into new content.

The local audit also identified repeated items across sections, familiar vocabulary targets, an incorrect explanation position after choice shuffling, and a contradictory reading passage. Corrections are recorded in [additional-v2 changes](app/content/staging/additional-v2/changes.json). Reading-format coverage, Mathematics figures, Language error-detection coverage and distractor quality still need improvement before the new banks can be called representative full-test practice. This process update does not itself approve content or alter the live bank.

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

For **every** authored item in every section, compare against all existing local banks and the **complete three-test corpus in the project Gables Markdown source**, including passages, choices, figures and guides. Use the full relevant section and cross-section material, not a reference sample:

- Exact and normalized text overlap, disregarding superficial formatting.
- Same sequence prefix, slightly extended/truncated sequence, same relationship structure with the same values, or reordered choices.
- Recognizable problem skeleton plus only a number/name swap.
- Reused figure geometry, arrangement, labels, or shading pattern.
- Copied explanation or distinctive wording.
- Reused vocabulary/spelling targets, passage scenarios, analogy pairs, logic structures, grammatical traps or composition tasks already encountered by this student.
- Duplicates or recognizable reskins across local sections, even when each bank independently contains 100 unique IDs.

Automated similarity flags are triage, not an originality verdict. Generic wording and common mathematical operations alone are not copying. A substantive match to a question this student already encountered requires replacement or explicit quarantine; do not simply dismiss it because the correct letter changed.

Keep an overlap log: local ID, reference locator, match reason, resolution, and reviewer/checker. Any unresolved overlap blocks release for this student, even when the item is mathematically correct.

**Implementation limit:** the current import tool does not automatically read and verify the full project Markdown corpus, compare diagrams, or detect semantic reskins. Until those capabilities exist, document this as an agent-assisted content check. Do not describe an unperformed similarity check as passed.

## 7. Independently validate all 100 before human sampling

Require complete metadata, four valid choices, stable unique IDs, no duplicate items, and a matching explanation and key. Evaluate every choice rather than checking only the declared correct answer.

Use independent arithmetic oracles, exact fractions where appropriate, sequence validators, truth tables for relational choices, and geometry assertions. Any new format needs a suitable validator. Equal numerical choices are unacceptable when the question asks only for a numerical value; if representation is the skill, state the required representation explicitly.

Check family repetition, answer-position balance, skill coverage, and ten-question selection. Ensure the app can render and grade the new formats without revealing answers during practice. Visual QA is mandatory for diagrams and mathematical typography.

Keep separate records for structural checks, mathematical checks, calibration, novelty, visual checks, and human review. Bind results to the content revision. A change to the stem, choices, key, explanation, or diagram requires renewed relevant checks; old receipts must not certify edited content.

Independently check **every answer and explanation in every section**, not only numerical items. Use domain knowledge and reasoning as well as the source comparison:

- Verbal: establish the intended word sense, relationship or logical entailment, and reject every distractor on a defensible basis.
- Reading: read the entire passage; identify the supporting evidence and distinguish supported inference from outside knowledge. Review passage accuracy and consistency separately from passage-based answer correctness.
- Quantitative and Mathematics: solve from the stem before consulting the authored key; cross-check with reliable numerical or logical validators and inspect all diagrams.
- Language: identify the governing grammar, usage, punctuation, spelling or composition convention; check whether another option is valid under standard written English.

Check tips and explanations for false general rules and stale references to shuffled choice positions. Do not use a reference answer guide as the sole oracle. Independently derive the result, compare it with the guide, and log disagreement instead of propagating it. Where no reliable executable validator exists, record an actual item-level semantic review rather than an automatic pass. Renew checks for every question depending on an edited reading passage.

## 8. Human review: 20 per 100

**This is a human acceptance sample only. It does not reduce the full 894-question source-calibration requirement or the independent review of all 100 authored questions.**

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
- Source register identifying the project Gables Markdown path/hash, all six document identities, and page/question locators.
- Full-corpus coverage ledger for all 894 positions and matching guides, with inspected/verified/exception status kept distinct; a section-by-section format/difficulty calibration report and justified deviations.
- Item-level audit and source-overlap log, including resolution of all flags.
- Independent answer and explanation review for all 100 items in every section, plus mathematical/logical and structural receipts where applicable, tied to the revision and passage dependencies.
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

> Follow this document to create or import the next 100 original questions for the requested HSPT section. Use `sources/HSPT_ALL_SIX_PDFS.md` as the primary calibration reference, locating its actual synced filename if necessary. Calibrate against all three complete tests and all three matching answer guides: 156 pages, 894 questions across all five sections, including embedded figures and full passages. Do not substitute a source sample or website excerpts. The student has already seen these questions, so do not copy, lightly reword, or merely change names or numbers. Preserve the approved app UX. Plan the section-specific mix, independently check every authored answer, explanation and tip, compare every item against the full corpus and all local banks, inspect visual formats, and record source exceptions honestly. Only after full-bank checks, produce a reproducible 20-question human acceptance sample per 100. This human sample is separate from full-set calibration. Bind evidence to source/content revisions, keep unresolved content pending, and do not deploy or claim official-test equivalence.

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

### Additional-bank integration update — September 27, 2026

Tobias approved the additional-v3 review packets and authorized integration in the project conversation. The active `all-sections-v0002` release combines the unchanged 100 Quantitative questions with 100 each for Verbal, Reading, Mathematics and Language. The approval is preserved at `app/content/review/additional-v3/decisions.json`, separately from historical pending draft templates. Only the fixed 20 per section are individually approved. The import preserves reviewed question content, embeds original figures and numbered passage paragraphs, and retains authored revision provenance. Acceptance permits skill practice and shortened previews; full-length exam presets, empirical difficulty/timing and actual iPad Safari checks remain outstanding. See `app/PHASE_III_PREVIEW.md` and `app/CONTENT_PUBLISHING.md` for current integration and release details.

## 11. Phase IV source-import track — Barron’s and Gables

This explicit exception implements PRD §12.4 for the two existing Markdown collections. Continue to use the Phase III staging, question format, evidence, review packets, cumulative releases, and shared index. The original-authorship rules above still apply to newly authored material.

1. Inventory all 894 Gables and 298 Barron’s source positions, keeping source hashes, form/question/page locators, passages, figures, original keys, and known exceptions. Preserve the source Markdown files.
2. Normalize the full inventory and check every question against its scan. Independently verify every answer and explanation, logical consistency, choice uniqueness, passage evidence, and visual accuracy. Fix source errors with a recorded explanation; quarantine unresolved items. The existing Gables audit may be reused only where its source hash and scope match. Inventory or structural validation alone is not correctness review.
3. Skip the additional Gables style/difficulty calibration comparison for these named source imports: record `not_applicable_source_import`. Do not reject an imported item merely because it matches its own source. Still reconcile duplicates against both collections and the existing bank.
4. After all-item checks, provide exactly **20 sampled questions in each of five sections (100 total)** for this combined import. Use reproducible selection covering source forms, skills, difficulty, formats, and risks. Follow §8’s questions-first layout with separate keys/explanations, complete passages/figures, and approve/revise/reject decisions. This source-import policy replaces 20-per-100 sampling only for this named combined delivery.
5. User approval of the samples approves the **full checked import**. Append all accepted questions, including unsampled questions, to the existing section banks. Do not publish only the sampled 100. Keep sample approval and individual review distinct. Recheck changed content; never manufacture user approvals.
6. Build a new cumulative release through the existing publisher. Preserve existing IDs and historical snapshots. Update the shared manifest’s section counts and overall count; repeated imports must not duplicate questions. Corrections/retirements require separate explicit operations.

Implementation: `app/scripts/stage-source-import.py` creates the inventory once; `prepare-source-review.mjs` prepares packets only after all-item checks; `accepted-source.mjs` enforces checks, samples, decisions and reconciliation inside `content-release.mjs`. Record distribution eligibility before publishing source material. See `app/PHASE_IV_STATUS.md` for actual completion status.
