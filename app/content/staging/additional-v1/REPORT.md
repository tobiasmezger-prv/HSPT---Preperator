# Four additional HSPT question banks — draft assembly

**400 authored questions: 100 each in Verbal Skills, Reading, Mathematics and Language.** Every question has four choices, a key, explanation, tip, stable ID/revision, skill, format, provisional difficulty and pending-review status. Reading has 16 original passages stored once and linked to their questions.

Open [the review index](review/index.html) to read any complete bank or its fixed 20-question inspection sample. Each packet places questions before its answer guide. Reading packets include complete passages and paragraph evidence. There are 80 sampled questions total, with no recorded approvals.

## Checked for this draft

- Four files each contain exactly 100 questions, with unique IDs and no identical stem/choice/passage combinations.
- Every bank has 25 correct answers at A, B, C and D; the order is deterministically shuffled.
- Shared draft manifest counts, file checksums, passage IDs/revisions and evidence-paragraph references validate.
- All four choices of all 100 Mathematics questions were evaluated numerically with exact fractions. The separate checker recomputes the author-supplied expressions; it does not independently prove that those expressions model the wording correctly. Explanation/key linkage is presence-checked, not semantically certified.
- Twelve six-item Reading groups and four seven-item groups total 100. Eight six-item groups plus two seven-item groups produce 62 questions without splitting a group. This demonstrates count feasibility, not timed-form acceptance.
- Ten focused tests passed, including rejection of wrong mathematical keys, equivalent numerical options, absent/stale passage references, duplicate IDs, stale checksums and executable expressions. Sampling reproducibility and coverage passed.
- Automated overlap triage found no exact normalized stem match against the accepted local Quantitative bank and no 12-word stem matches in the extracted question text of Gables webpage Tests 1 and 3. This is a narrow screening result, NOT originality clearance. It excludes semantic reskins, visual overlap, short/common phrases and full comparison with the scanned Test 2.

Detailed receipts: [validation](validation.json), [exact numerical checks](mathematics-checks.json), [item audit](item-audit.json), [overlap log](overlap-log.json). Results are tied to the draft manifest or section checksum.

## Calibration and limitations

Follow [the batch plan](PLAN.md) and the root question-bank process. The STS manual establishes section scope; Gables examples and their matching explanations provide calibration only. Source passages and items are not incorporated into these banks. Third-party PDFs remain outside the repository content.

Initial source inspection included the publisher's printed pages 1–2; text from the two Dummies test/answer pairs; and visual inspection of scanned Peterson's question PDF pages 1, 12, 20 and 26 and answer PDF pages 1, 9, 13 and 17. Some scanned answer-page words/symbols are absent even in the rendered source; no missing item was reconstructed or treated as a correctness oracle. This is not an exhaustive source census, key certification, or novelty review.

All sections are **draft skill practice**, with the following work remaining before acceptance:

1. Complete item-level editorial checks: key uniqueness, word sense, logic, grammar conventions, plausible distractors, explanation/tip quality, Reading inference support and Mathematics stem-to-expression interpretation. Add explicit distractor-error mappings and resolve any ambiguity.
2. Complete a section-specific source/difficulty census and semantic originality comparison against all three Gables tests, including scanned pages and their paired explanations. Per-item calibration currently points to the shared source plan; additional skill briefs are in calibration-briefs.json. Full source-specific novelty clearance is pending.
3. Improve difficulty and format variety. Reading passages are 155–176 words, and many follow problem/observation/revision structures; longer and more varied texts may be needed for full-section calibration. Correct Reading choices are uniquely longest in 57 of 100 items, a potential cue requiring revision. Language concentrates on selection/correction rather than the reference tests' error-detection/no-error format. Verbal classifications state categories explicitly and are primarily foundational; logic uses four-option conclusion selection rather than the three-option format seen in some references.
4. Mathematics currently has no diagrams. Diagram/graph interpretation should be added and visually validated before claiming exam-style coverage. Numerical checks alone do not make the bank exam-ready.
5. Reading groups have six or seven items, so a whole-group burst cannot contain exactly ten. The PRD permits a disclosed shorter set; the app must support that choice or the bank needs additional reviewed groups. No production selection behavior changed here.
6. Complete browser and iPad rendering checks. Initial in-app browser spot checks covered the index, Reading full-bank opening, and the Mathematics, Language and Verbal sample openings at a narrow viewport. The observed headings and text wrapped without overlap. These are limited spot checks; full-page, screen-reader/iPad and live-app rendering remain separate gates.
7. After full-bank gates pass, issue the **formal** fixed 20-question human review sample per section, with the complete Reading passages. The current 20-item files are reproducible provisional inspection packets, not acceptance evidence. Decisions remain pending. Changes invalidate relevant receipts and selections; never transfer approvals silently.
8. Integrate through a compatible Phase III multi-section schema, loader, renderer and release gate. The staged loader is an authoring tool only. The current published-content validator still accepts Quantitative releases only.

**Publication status: blocked by incomplete content/review/integration gates.** No production bank, active manifest, saved session, GitHub repository or Vercel deployment was changed.

## Reproduce

From the project root:

```sh
python3 app/scripts/additional_banks/build.py
python3 app/scripts/additional_banks/validate.py
python3 -m unittest discover -s app/scripts/additional_banks -p 'test_validation.py'
python3 app/scripts/additional_banks/package_review.py
```

The four authoring modules are the source of the generated section JSON files; do not maintain a separately hand-edited combined bank. The packaging step never overwrites existing human decision files. If a section or its passage dependency changes, compare decision checksums and request fresh review rather than reusing stale decisions. Optional reference text for overlap triage is read from `/private/tmp/hspt-gables`; if unavailable, that source scan is explicitly absent, not passed.
