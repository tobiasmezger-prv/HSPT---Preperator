# Additional HSPT banks — draft v1

Date: 2026-09-27. Scope: 100 original drafts each for Verbal Skills, Reading, Mathematics and Language. These are skill-practice drafts, not accepted exam forms. Quantitative content is unchanged.

This section-specific extension applies the root QUESTION_BANK_CREATION_PROCESS.md. It does not supersede its acceptance gates. Source documents remain read-only.

## Coverage planned before authoring

- Verbal: 25 synonyms, 25 antonyms, 20 analogies, 15 classifications, 15 logical reasoning.
- Reading: 16 original passages with 6 or 7 questions each, 100 total; main idea/purpose, details, inference, vocabulary in context, structure and literary interpretation. Twelve six-question groups and four seven-question groups permit 62 questions without splitting a passage group (eight six-question and two seven-question groups). Difficulty and passage length require further calibration before timed-section use.
- Mathematics: 100 items across number concepts/computation, ratios/percent, measurement, geometry, algebra, statistics/probability. Each answer receives an executable exact-number check; this does not establish that the expression correctly models the stem.
- Language: grammar, usage, punctuation, capitalization, spelling and composition; use explicit standard written American English conventions and avoid disputed stylistic preferences.

All allocations are editorial choices, not publisher percentages. Difficulty is provisional. No live AI generation, release, GitHub push or deployment is part of this batch.

## Schema and staged loader

Use a common draft schema, one section file per subject and one shared passage file. Each item includes ID/revision, skill, format, difficulty, family, four choices, key/explanation/tip, authorship provenance, calibration reference, and pending review status. The staged loader checks checksums and passage dependencies before returning any batch. This is an authoring foundation; the app's production loader still requires Phase III integration and must not ingest these drafts.

## Subject-specific review

Verbal: check word sense, part of speech, analogy direction, alternative categories and validity of every logical conclusion. Reading: preserve full original passage, anchor every answer in paragraph evidence, and reject inferences that require outside knowledge. Mathematics: independently recompute numerical answers and review the translation from stem to arithmetic. Language: identify the governing convention and ensure other answers cannot be defended under standard usage.

Before formal human sampling, complete calibration, semantic/source-overlap, editorial and rendering checks. A provisional 20-item inspection packet can help work begin, but it is not the formal acceptance sample until those prerequisites pass. Its selection must be reproducible and cover skills, difficulty and formats. Never invent human decisions. Exactly 80 human sample decisions will ultimately be needed across these four banks.

## Calibration sources

Publisher scope: https://www.ststesting.com/hp_int_sts.pdf, printed pp. 1–2 (PDF pp. 5–6), accessed 2026-09-27.

Gables register: https://gablestutoring.com/practice-tests/, accessed 2026-09-27. Pairings follow the root process, not filenames:

1. Web Test 1: HSPT-Test-3.pdf / HSPT-TEST-3-Answers.pdf, Catholic High School Entrance Exams For Dummies, printed Test 1. Question sections: PDF pp. 1–5 verbal, 12–20 reading, 21–27 mathematics, 28–34 language.
2. Web Test 2: HSPT-TEST-4-1.pdf / HSPT-TEST-4-Answers.pdf, Peterson's, printed Practice Test 5. Scanned pages require visual inspection; blank text extraction is not evidence of no overlap.
3. Web Test 3: HSPT-TEST-5.pdf / HSPT-TEST-5-Answers.pdf, Catholic High School Entrance Exams For Dummies, printed Test 2. Question sections: PDF pp. 1–5 verbal, 12–21 reading, 22–27 mathematics, 28–33 language.

All six PDFs were opened and extracted for inspection. Extraction of the scanned second pair is incomplete. Initial calibration establishes short verbal formats, passage-based comprehension, computation/application and convention/composition tasks; it is not a complete difficulty census or originality clearance. Some reference logic items use three choices; our four-choice conclusion-selection format is an adaptation for skill practice, not exact form replication. Do not reproduce source stems, passages or explanations. Full source-by-source semantic comparison remains a release gate.
