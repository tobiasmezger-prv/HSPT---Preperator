# Product Requirements Document: HSPT Practice
**Version:** 2.0 — consolidated Phase III planning  
**Platform:** iPad-first responsive web application (Safari; landscape optimized)  
**Primary user:** One middle-school student preparing for the HSPT  
**Initial build:** Phase I — Quantitative Skills prototype  
**Status:** Phase III app 0.3.0 integrates 500 sample-reviewed questions across all five sections. Shortened previews work; full-length presets/exam, physical iPad checks and production release remain pending. See [implementation status](app/PHASE_III_PREVIEW.md).

This is the working overall PRD. It consolidates the original Phase I requirements and the Phase III plan, including subsequent timing verification and the required burst/full-section options. The synced original under `sources/` remains a read-only historical reference. The content-review policy follows [QUESTION_BANK_CREATION_PROCESS.md](QUESTION_BANK_CREATION_PROCESS.md).

## 1. Product vision
Build a calm, paper-like HSPT practice experience that trains both accuracy and speed. A student should be able to sit down with an iPad, launch a timed practice burst, answer questions in any order on a familiar question-and-answer-sheet layout, and receive useful explanations and actionable performance feedback.

The long-term product supports all five HSPT sections, full-length and section-specific tests, an effectively unlimited *validated* question library, progress analytics, and adaptive five-minute practice for recurring weaknesses. Phase I deliberately implements only Quantitative Skills, using a curated question bank rather than live AI generation.

**Product principles:** (1) Authentic paper-test feel, (2) fast to start and easy to navigate, (3) accurate questions before volume, (4) speed and accuracy measured separately, (5) student privacy and minimal distraction.

## 2. Scope and phased delivery
| Capability | Phase I baseline | Phase III | Later |
|---|---|---|---|
| Platform | iPad Safari responsive PWA | Preserve iPad, offline, and local-first behavior | Native app only if justified |
| Sections | Quantitative Skills | All five core HSPT sections | Optional school tests if justified |
| Modes | 10-question, 5-minute burst; untimed | **5-minute burst and full-section practice for every section**, plus full five-section exam | Custom accommodation presets |
| Test UI | Paper-style questions and answer sheet | Long sections, passages, additional formats | Further refinement |
| Timer | Hideable countdown and auto-submit | Verified section-specific limits and exam transitions | — |
| Results | Score, errors, omissions, explanations | Section/mode-aware results and full-exam summary | Rich longitudinal dashboards |
| Question library | 100 original Quantitative items under the review process | Proposed 100 per section / 500 total, keys and explanations included | Expanded validated supply |
| Analytics | Local history, skill accuracy, approximate attention time | Preserve history and distinguish sections/modes | Adaptive recommendations |
| Targeted practice | Manual skill selection | Section-specific skill practice | Automatically prescribed bursts |
| Accounts | Single local profile | Single local profile, no sign-in | Optional secure sync |
| Delivery | Static-site deployability | App and broader bank on GitHub; verified Vercel production release | — |

**Phase III has exactly two major milestones:** (1) full Quantitative section practice; (2) all five sections, broader bank, and GitHub-to-Vercel release. Full Quantitative practice moves from the earlier Phase II roadmap to Phase III Milestone 1. Detailed requirements and acceptance criteria appear in section 11.

**Not in Phase I:** live LLM question generation, official HSPT copyrighted content, cloud sync, payment, leaderboards, social features, full-length exam simulation, parental monitoring, or inferred standardized-test scores.

## 3. Users and primary journeys
**Student:** launches a practice burst in two taps; can answer questions in any order, change answers, flag and revisit items, and review explanations afterward. Can hide the timer without stopping it.

**Parent:** can see recent practice history and understand whether mistakes arise from knowledge gaps, slow solving, or unanswered items. No separate parent account in Phase I.

**Phase I flow:** Home → choose Quantitative Skills → choose Mixed or a skill focus → start 10-question/5-minute burst → paper-style test → submit or auto-submit at time expiry → score/review → history.

**Phase III section flow:** Home → choose any of five sections → choose **5-minute burst** or **Full-section practice** → confirm count/timing → test → results and explanations → section/mode history. Untimed practice remains an additional option.

**Phase III exam flow:** Home → full five-section practice exam → section instructions → timed section → transition/break → next section → final results and review.

## 4. Phase I functional requirements

### 4.1 Home and setup
- Primary CTA: **Start 5-minute Quantitative burst** (10 questions).
- Secondary actions: **Choose a skill**, **Untimed practice**, **History**.
- Mixed bursts draw across supported skill tags. Skill-focused bursts select from one category; if fewer than 10 suitable unseen questions remain, permit previously seen questions and label this in setup.
- Display a concise pre-test summary: question count, time limit, timer visibility, and mode.
- Allow timer to start visible or hidden; student can toggle during the test.
- Persist preferences on device.

### 4.2 Paper-style testing interface
- Optimize for iPad Safari landscape. Questions occupy approximately 65% of available width on the left; answer sheet occupies approximately 35% on the right.
- Left: all ten numbered questions in a vertically scrollable continuous paper-like list, including A–D answer options as text. Right: matching numbered A/B/C/D answer bubbles and flag controls.
- Answer selection happens on the **right**; left-side options remain visible for reference. Show the selected answer clearly on the answer sheet.
- Support answering in any order, changing an answer, clearing an answer, flagging/unflagging, and tapping an answer-sheet row to jump to its corresponding question.
- Keep the answer sheet usable as the left question pane scrolls; on tablets, independent pane scrolling is acceptable **only if** tapping a question/answer row reliably aligns or highlights the matching item. Prefer a synchronized layout if it remains legible and smooth on real iPad hardware.
- Show answered count (e.g., 6/10), persistent Submit button, and optional countdown in a compact header. Submit confirmation must show unanswered count; allow return to test while time remains.
- On narrower portrait screens, preserve function with a responsive stacked or toggleable Questions / Answer Sheet view. Do not require landscape lock.
- Large touch targets (at least ~44×44 CSS pixels), clear focus states, sufficient contrast, VoiceOver-friendly labels, and no horizontal overflow.
- Save answers and elapsed-time state automatically after every interaction and on page visibility changes. If Safari refreshes, restore an unfinished session with a clear Resume option.

### 4.3 Timing and completion
- Default timed burst: **5:00 for 10 questions**. Countdown uses elapsed wall-clock time anchored to a persisted start/deadline timestamp, not a fragile decrementing interval.
- Timer visibility toggle hides the display but does not pause the countdown.
- At zero: play a brief, non-startling sound when the browser permits audio, display a visible **Time is up** message, and automatically submit. Because mobile Safari may restrict audio or mute the device, visible completion must always work; unlock audio on a user gesture at session start when feasible.
- Manual early submission is allowed after confirmation. Prevent duplicate submissions.
- Capture session duration and per-question timing as **approximate active attention time** (time a question is in view/selected), not a claim to measure actual thinking time. Label it as approximate in analytics.
- Untimed mode has no automatic deadline and may show elapsed time.

### 4.4 Question bank and selection
- Ship with **100 original Quantitative Skills questions accepted under the documented batch-review process**. Do not present AI drafts as verified. If 100 validated items are not available when UI development begins, use a smaller clearly labeled development fixture and block release until the 100-item acceptance criterion is met.
- Initial practice tags (historical baseline; use the current calibrated format mix for full-section practice): number sequences (additive/increasing differences and multiplicative), numerical comparisons (fractions/decimals/percentages), number manipulation, nonverbal or symbolic numerical patterns, and odd-one-out reasoning. Tune the exact distribution against reputable HSPT prep references before release; these are *practice categories*, not a claim of official exam blueprint weights.
- Use the current calibrated Quantitative mix: sequences, number manipulation, nongeometric comparisons, and geometric/visual comparisons. Symbolic and odd-one-out drills are supplemental unless supported by calibration evidence. Avoid repeating near-identical templates within one burst.
- Each question contains exactly one defensible correct answer and four distinct choices, plus an explanation and (where meaningful) a fastest-method tip.
- Validate schema, answer key, choice uniqueness, and mathematical correctness. Parameterized generators may produce future variants, but every variant must pass the same validation before entering the released bank.
- Track previously encountered question IDs and prefer unseen questions when possible. Never promise literal infinity: the long-term goal is an effectively unlimited *quality-controlled* supply.

### 4.5 Results and review
- Show score as **correct / total**, percentage, attempted, incorrect, and unanswered. Clearly distinguish incorrect from unanswered.
- Review screen lists **all incorrect and unanswered questions first**, then offers access to all questions.
- Each reviewed item shows the original stem and choices, student's selection (or Unanswered), correct answer, concise reasoning, and a mental shortcut where appropriate.
- Display total session time and optional approximate time by skill; do not assign exact per-question solving times based only on scroll position.
- Provide **Practice this skill** action to launch a new 5-minute burst filtered to the question's skill category.
- Never reveal correct answers or explanations during a timed test.

### 4.6 Progress and storage
- Persist locally: settings, question exposure history, session summaries, responses, flags, and approximate time observations. Use IndexedDB for session data; localStorage may hold small preferences.
- History shows date, mode, score, questions attempted, and time used. Simple per-skill accuracy over completed sessions is sufficient for Phase I.
- Avoid diagnostic claims from tiny samples. Display sample sizes and neutral observations rather than labeling a skill a weakness after one error.
- Include a **Reset local data** action behind confirmation. No analytics trackers, advertising, account creation, or external transmission of a child's practice data in Phase I.

## 5. Data model

### 5.1 Phase I conceptual baseline

These types describe the original prototype, not the current implementation or final Phase III schema. In particular, the original `approved` label must not imply individual human review of every item; use explicit batch and individual review records as described below.
```ts
type Skill =
  | 'sequence_additive'
  | 'sequence_multiplicative'
  | 'numeric_comparison'
  | 'number_manipulation'
  | 'symbolic_pattern'
  | 'odd_one_out';

type Choice = { id: 'A' | 'B' | 'C' | 'D'; text: string };

type Question = {
  id: string;
  section: 'quantitative';
  skill: Skill;
  difficulty: 1 | 2 | 3;
  stem: string;
  choices: [Choice, Choice, Choice, Choice];
  correctChoiceId: Choice['id'];
  explanation: string;
  shortcut?: string;
  sourceType: 'original_reviewed' | 'validated_template';
  reviewStatus: 'approved';
  templateFamily?: string;
};

type Response = {
  questionId: string;
  selectedChoiceId: Choice['id'] | null;
  flagged: boolean;
  approximateActiveMs?: number;
};

type Session = {
  id: string;
  mode: 'timed_burst' | 'untimed';
  skillFilter: Skill | 'mixed';
  questionIds: string[];
  responses: Record<string, Response>;
  startedAt: string;
  deadlineAt?: string;
  completedAt?: string;
  status: 'in_progress' | 'submitted' | 'expired';
};
```
Keep questions separate from sessions so an existing test remains reproducible if the question bank later changes; snapshot question content or version the bank for completed sessions.

### 5.2 Phase III extensions

- Required section identity: `verbal`, `quantitative`, `reading`, `mathematics`, or `language`; validate skills and formats against the section.
- Session mode: five-minute burst, full section, or untimed. Persist question count, configured duration, configuration version, deadline, bank release, and immutable content/answer-guide snapshots.
- Exam record: ordered section sessions, active section, transition/break state, and completion or early-end state. Store each started section's deadline independently.
- Passage record: stable ID/revision, original text, provenance, and associated questions; preserve passage snapshots and exposure history.
- Content acceptance: distinguish batch sample-review status, individual review decisions, and permitted use (skill practice versus full-section practice). Preserve revision-bound validation evidence.
- Migrate legacy sessions without rewriting their question content, answer keys, deadlines, or scores. New types must support existing backups and history.

## 6. UX and visual direction
- Quiet, readable, paper-inspired layout: warm white question pane, subtle separators, dark text, restrained accent color, large legible question numbers.
- Landscape-first at common iPad viewport sizes; no tiny desktop-style controls.
- Answer bubbles should feel like a physical answer sheet, with a strong visual selected state and no accidental double taps.
- Minimize animation and sound except for the requested end-of-time cue.
- No gamified streak pressure in Phase I. Favor clear progress and encouragement tied to evidence.

## 7. Architecture and engineering guidance
**Suggested stack:** React + TypeScript + Vite; CSS modules or a simple component styling system; IndexedDB via a small typed wrapper (e.g., Dexie); Vitest and React Testing Library for unit/component tests; Playwright for end-to-end browser tests. Configure as a PWA with installable manifest and cache essential static assets and the approved question bank for offline practice.

- Client-only Phase I: no backend, authentication, AI API keys, or external database required.
- Separate modules for question selection, test-session state, timer/deadline, scoring, persistence, analytics, and UI.
- Make scoring a pure deterministic function. Store deadline timestamps so backgrounding Safari does not extend a timed test.
- Bundle an approved question JSON file; validate it at build time with a schema validator and independent answer checks where possible.
- Use semantic HTML and accessible form controls. Test with touch and VoiceOver.
- Add minimal error handling and a friendly recovery path if storage is unavailable.

**Phase I suggested repository structure** (Phase III content organization is specified in section 7.1.)
```text
src/
  app/
  components/{QuestionPaper,AnswerSheet,Timer,QuestionNavigator}/
  pages/{Home,Setup,Test,Results,History}/
  domain/{questions,selection,session,scoring,analytics}/
  storage/
  data/questions.quantitative.approved.json
  styles/
tests/{unit,e2e}/
scripts/validate-question-bank.ts
```

### 7.1 Phase III question-bank organization

**Use separate versioned question files for each HSPT section, with one shared manifest/index and one shared app data-access layer.** Here, “category” means one of the five sections, not an individual skill. Start with 100 eligible questions per section as the initial planning target; keep skills and difficulty as fields within each section file rather than creating a file per skill.

Illustrative published release layout:

```text
content/
  manifest.json
  releases/<release-id>/
    verbal.json
    quantitative.json
    reading.json
    mathematics.json
    language.json
    reading-passages.json
    assets/
```

- Each section file contains its questions, correct answers, explanations, and metadata under the same versioned schema. IDs are globally unique; each item explicitly carries its section, skill, difficulty, and content revision. Keep each question and its answer guide together as the source of truth; any separate runtime answer lookup is generated and validated from that content.
- Store shared Reading passages once in `reading-passages.json`; questions reference stable passage IDs/revisions. Validate all references and include complete passages in saved-session snapshots.
- The shared manifest identifies the schema version and release ID. For each section it records the immutable file URL/path, section version, question count, and checksum, plus the versioned passage/asset dependencies and their checksums. Generate counts/checksums from the validated files rather than maintaining them by hand.
- Author, validate, review, and revise each section independently. Keep drafts and review evidence outside the published runtime files. A release may update one section while referencing unchanged, already accepted versions of the others; every published manifest must describe a complete compatible release.
- The app reads the manifest through a common loader and imports validated content into its existing IndexedDB storage, indexed by section and skill. Separate files do not require separate databases or separate selection/scoring implementations. Select a burst or full section from the requested section; assemble a full exam across all five.
- Validate schema compatibility, unique IDs, declared section/count, keys/explanations, checksums, and dependencies before activating an update. Stage the complete release and switch the active release atomically; on failure retain the prior valid release. Cache all five sections and their dependencies for offline full-exam use, while keeping active-session snapshots unchanged.
- Build the shared schema, manifest format, validators, and loader first using the existing Quantitative bank and small development fixtures for new formats. Then author and review the new 100-question section batches. Fixtures do not count toward release inventory.

This is the Phase III storage decision. Do not maintain a second hand-edited monolithic bank alongside the section files; any combined in-memory view or generated runtime index derives from the section files and manifest.

## 8. Acceptance criteria / definition of done for Phase I
1. On an actual iPad in Safari landscape, a student can launch a 10-question timed burst in two taps from Home.
2. All ten questions and corresponding answer-sheet rows are available without sequential navigation. The student can answer, revise, clear, flag, and jump to any question.
3. The countdown can be shown/hidden; it expires after five real minutes even if Safari is backgrounded. A visible timeout always appears and an audible cue plays when device/browser settings permit.
4. Early submission requires confirmation and indicates unanswered count. Timeout auto-submits once, with no loss of recorded answers.
5. Results calculate correct, incorrect, and unanswered counts accurately and show a valid explanation for every incorrect or unanswered item.
6. Session progress survives a refresh. Completed sessions appear in local History; local data can be reset.
7. At least 100 original Quantitative questions pass full-bank checks and the documented fixed human sample of 20 per 100. Accepted batches are sample-reviewed; unsampled items are not individually human-approved. No known ambiguous items or invalid keys may remain in the release bank.
8. A mixed burst avoids duplicate question IDs and prefers unseen questions; a skill-focused burst is available from setup and results.
9. Automated tests cover scoring, question selection, persistence/resume, deadline handling, and review behavior. A real-iPad manual checklist covers scroll alignment, touch targets, portrait fallback, audio restrictions, and Safari backgrounding.
10. The app is deployable as a static site and installable to the iPad home screen. No student data leaves the device.

## 9. Phase I development plan (baseline)
**Sprint 1 — Usable prototype:** Scaffold app and PWA; implement Home, Setup, paper-style Test, answer sheet, flags, timer and a **small development fixture** of clearly labeled reviewed sample questions. Test on iPad before proceeding.

**Sprint 2 — Reliable assessment:** Add deterministic scoring, Results/review, explanations, IndexedDB persistence/resume, and automated tests. Verify timing and refresh behavior.

**Sprint 3 — Content and history:** Populate and independently validate the 100-question approved bank; implement balanced selection, unseen-question preference, skill filters, History and basic per-skill metrics. Complete iPad QA and release checklist.

**Do not implement future-phase AI generation until the Phase I content-validation process and UX are proven.**

## 10. Roadmap and current planning baseline

**Phase II:** The earlier roadmap identified broader reviewed content, richer trends, and targeted speed-versus-accuracy recommendations. This document does not certify their completion. Full Quantitative section practice is now assigned to Phase III Milestone 1; adaptive recommendations remain future work.

**Phase III:** Two milestones defined in section 11. Every core section must offer both a five-minute burst and full-section practice. The phase ends with the app and broader question-and-answer bank versioned on GitHub and verified in Vercel production.

**Phase IV:** Controlled AI-assisted generation behind a validation pipeline, expanded template families, adaptive five-minute practice, optional secure account/sync, and richer progress visualizations. AI must not directly publish unverified items.

### Current implementation baseline

The current app has a five-minute deadline and ten-question selection built into its session logic. Its question types and skill tags are quantitative-specific. The Gables v2 bank is integrated locally; its integration record reports passing automated checks but pending browser/iPad verification and no deployment. These are recorded findings, not newly rerun checks. This workspace is not a Git checkout, and a GitHub remote and Vercel production project have not been established from the local files inspected.


## 11. Phase III requirements and delivery

**Outcome:** Full-section practice, then a five-section app and broader reviewed question-and-answer bank, ending with a GitHub-to-Vercel release.

### 11.1 Verified exam structure

**Thirty minutes is correct for Quantitative Skills only.** Use the following standard section presets:

| Section | Questions | Time limit |
|---|---:|---:|
| Verbal Skills | 60 | 16 minutes |
| Quantitative Skills | 52 | 30 minutes |
| Reading | 62 | 25 minutes |
| Mathematics | 64 | 45 minutes |
| Language | 60 | 25 minutes |
| **Total** | **298** | **141 minutes (2 hours 21 minutes)** |

Section names and counts: [STS interpretive manual, printed pages 1–2](https://www.ststesting.com/hp_int_sts.pdf). Standard time limits: [Archdiocese of Washington HSPT guide](https://adwcatholicschools.org/high-school/placement-tests/about-hspt/). Cross-check: [Huntington section table](https://secureapplication.huntingtonhelps.com/high-school-placement-test). Sources checked September 26, 2026.

The total above excludes instructions and breaks. Do not model the test as five 30-minute sections or assume one universal break schedule. Optional school-specific tests are outside this phase.

#### Timing cross-check

A second online check confirmed the section presets against multiple sources:

- [Archdiocese of Washington](https://adwcatholicschools.org/high-school/placement-tests/about-hspt/) explicitly lists 16 / 30 / 25 / 45 / 25 minutes. It allows three hours for administration, including two short breaks and 30 minutes for distributing/collecting materials.
- [Woodlands Academy's entrance-exam page](https://www.woodlandsacademy.org/exam) independently lists all five matching section limits and question counts.
- [Cardinal Education](https://www.cardinaleducation.com/test-prep/private-school-test-prep/hspt-test-prep/) also lists the same five limits and counts.
- [STS's product listing](https://www.stsme.com/prod/HSPT/) gives an overall completion time of 2.5 hours, without a section-by-section breakdown on that page. Treat this as an overall duration description, not a reason to increase the sum of the individual clocks to 150 minutes.

The arithmetic is **16 + 30 + 25 + 45 + 25 = 141 minutes**. For the app, label the complete exam **“2 hours 21 minutes of timed questions, plus breaks.”** Actual school appointment duration depends on local administration. Keep that separate from the app's section deadlines.

### 11.2 Milestone 1 — Full Quantitative Skills section

**Student outcome:** Choose a short practice burst or complete a 52-question Quantitative Skills section in 30 minutes, then review every answer and explanation.

#### Functional requirements

- Add **Full Quantitative section — 52 questions · 30 minutes** alongside the existing 10-question, five-minute burst and untimed practice.
- Show question count, time limit, and any reused-content notice before starting. Full sections use a mixed exam-style selection; skill filtering remains a practice feature.
- Replace fixed counts and timing with shared mode/section configuration. Persist the selected section, mode, count, duration, and configuration version with each session.
- Preserve free navigation, answer changes, clearing, flags, timer visibility, and unanswered-count confirmation. Make the answer sheet and question jump behavior usable across 52 items on iPad.
- Persist a wall-clock deadline. Refreshing, hiding the timer, locking the device, or backgrounding Safari must not extend it. On returning after expiry, finalize once using the deadline and reject late answers.
- Preserve question and answer-guide snapshots or immutable revisions so bank updates cannot change a saved test or its scoring.
- Show raw score, percentage, correct/incorrect/unanswered counts, time used, and review with explanations. History distinguishes bursts, full sections, and untimed practice; report approximate attention time honestly.

#### Quantitative content work

Audit the existing 100-item bank for full-section use. Prior sample review for skill practice does not establish exam-style coverage. Document the selection mix across sequences, manipulation, numerical comparisons, and geometric comparisons; describe weights as editorial choices, not official proportions.

Select exactly 52 distinct eligible questions, favor unseen content where coverage permits, and avoid near-identical families. Never fill a section by duplicating questions. If fewer than 52 eligible items exist, block the full-section start with a useful message. Previously seen questions may be reused across sessions with disclosure. One hundred items cannot support two completely disjoint 52-question forms; no promise of repeat-free full sections is made.

#### Milestone 1 acceptance

1. A student completes a 52-question section with a 30:00 starting timer and correct results/review.
2. Selection guarantees count, unique IDs, documented coverage, and exclusion of pending or unsuitable content.
3. Tests cover configurable duration/count, background expiry, refresh/resume, late-answer rejection, and single submission; legacy five-minute sessions and history still work.
4. Actual iPad Safari checks cover long-list navigation, diagrams, portrait fallback, audio/visible timeout, and recovery after backgrounding.
5. The content acceptance record explicitly permits full-section practice, with any required revisions reviewed under the existing bank process.

**Deliverables:** Working Quantitative full-section mode, content coverage/acceptance record, automated verification, and iPad QA record. Production deployment is the closing step of Milestone 2.

### 11.3 Milestone 2 — All five sections, broader bank, and release

**Student outcome:** Select any core HSPT section for practice or complete a five-section practice exam, with dependable explanations and a deployed app available on iPad.

#### Section expansion

| Added section | Content scope | App work |
|---|---|---|
| Verbal Skills | Synonyms, antonyms, analogies, classifications, logical reasoning | Section-specific skill filters and explanations |
| Reading | Main idea, detail, inference, literary interpretation, vocabulary in context | Readable shared passages, passage-linked questions, evidence-based explanations |
| Mathematics | Computation and applications across number concepts, measurement, geometry, algebra, statistics | Math notation/diagrams and independently checked solutions |
| Language | Punctuation, capitalization, spelling, grammar, usage, composition | Preserve meaningful formatting and explain applicable conventions |

Scope reference: [STS interpretive manual, printed pages 1–2](https://www.ststesting.com/hp_int_sts.pdf). Keep Mathematics and Quantitative Skills as separate subjects in the interface, bank, and history.

- Add a five-section home/setup flow. **Every section must offer both a 5-minute burst and full-section practice.** Present these as two clearly labeled choices after selecting a section; neither option is optional or limited to Quantitative Skills. Untimed practice remains an additional option.
- Every burst has a five-minute deadline. Proposed burst question count: 10, explicitly labeled practice pacing rather than official exam pacing; Reading passage-group handling is specified below. Full-section practice uses the verified count and time limit for the selected section.

| Section | Required burst option | Required full-section option |
|---|---|---|
| Verbal Skills | 5 minutes | 60 questions · 16 minutes |
| Quantitative Skills | 5 minutes | 52 questions · 30 minutes |
| Reading | 5 minutes | 62 questions · 25 minutes |
| Mathematics | 5 minutes | 64 questions · 45 minutes |
| Language | 5 minutes | 60 questions · 25 minutes |

- Make section mandatory on new questions, with section-specific skills and formats. Preserve legacy quantitative snapshots through a versioned migration.
- Add versioned passage records, passage IDs on dependent questions, and passage text in saved-session snapshots. Keep passage groups together in selection and rendering; enforce the exact section count without orphaning questions. Track passage exposure as well as question exposure.
- For Reading, keep the passage easy to revisit while answering; avoid squeezing passage, questions, and bubbles into three narrow columns. Short practice must use suitable passage groups; if ten items cannot be assembled, show the actual count before starting.
- Make results, skill practice, exposure tracking, backup/restore, and history section-aware. Do not pool unlike section results into misleading skill metrics.

#### Five-section practice exam

Provide a full practice exam within this milestone: Verbal → Quantitative → Reading → Mathematics → Language, using 298 questions and the five individual deadlines above.

- Generate and persist the complete form before starting. Start each section's clock only when the student begins that section.
- Allow navigation only within the active section. On submission or expiry, lock it and show a transition screen. Unused time does not transfer.
- Provide between-section breaks as a clearly labeled practice setting, separate from test time; do not claim a universal official break schedule.
- Save exam progress and active-section deadlines through refresh or browser closure. Returning after expiry closes the active section but does not silently start subsequent sections.
- Reveal answers after the entire exam is completed or explicitly ended. Report unfinished sections separately if the student ends early.
- Show section scores and total correct out of 298 for a completed exam. Do not manufacture official scaled scores, percentiles, or admissions predictions.

#### Broader question-and-answer bank

**Proposed first-release floor: 100 eligible items per section, 500 total**, retaining or revising the existing quantitative bank and adding at least 400 items across the four new subjects. Each section must also satisfy its coverage and form-assembly checks; a count alone is insufficient. Reading includes enough complete passage groups to assemble a coherent 62-question section. This floor supports one complete exam with reuse across later attempts; it does not promise multiple disjoint forms.

Organize these batches as the five separate section files plus shared manifest specified in section 7.1. Complete the common schema and validation foundation before producing the full new banks; review and accept each section batch independently.

Each released item needs a stable ID/revision, section, skill, format, provisional difficulty, family, choices, exactly one defensible key, explanation, and provenance/review status. Add passage references, visual assets, and useful tips as applicable. An answer guide must explain why the key is correct; passage questions must point to supporting text or a justified inference.

Extend `QUESTION_BANK_CREATION_PROCESS.md` for the new subjects before authoring their release batches:

1. Establish section-specific calibration sources and coverage plans. Use third-party practice for calibration only; author original questions, passages, diagrams, and explanations.
2. Validate every item's structure and key/explanation linkage. Independently check numerical solutions; record editorial checks for language, logic, and passage evidence rather than calling those mathematically verified.
3. Check originality, ambiguity, duplicate items, family repetition, answer-position distribution, and rendering. Validate passage completeness and references.
4. Retain the normal fixed human sample of 20 per 100-item batch, stratified by each section's skills, difficulty, and new formats. For Reading, reviewers receive the full passages for sampled questions. Four new 100-item batches imply 80 sampled questions; changes to quantitative content require their own relevant renewed checks.
5. Bind evidence and decisions to the content revision. A wrong key, ambiguity, unsupported inference, or source overlap blocks the affected batch until resolved. Do not invent approvals or label unsampled items individually human-approved.
6. Publish only accepted revisions eligible for their stated practice/full-section use. Keep draft and review artifacts separate from the runtime release.

#### GitHub → Vercel delivery

This is the final workstream of Milestone 2, not a third milestone.

1. Establish the intended GitHub repository and Vercel project at implementation time, reusing existing destinations if available. Record repository URL/visibility, production branch, Vercel project, and production URL. These destinations remain unresolved in this planning draft.
2. Version the app and broader bank together in GitHub: questions, keys, explanations, original passages/assets, release manifests, validators, and review evidence. Keep student session exports, credentials, dependencies, generated build output, and third-party calibration PDFs out of the repository release.
3. Require bank validation, app tests, type checks, and a production build before release. Use the existing React/Vite app; verify Vercel's selected root directory, lockfile/package manager, build command, and output directory against the final repository layout.
4. Deploy the release candidate to a Vercel preview. Test all five full-section presets, the full-exam flow, representative passages/diagrams, scoring, resume, and migration on iPad Safari.
5. Verify actual delivery of all five versioned section files, their answer guides, shared passages/assets, and the shared manifest specified in section 7.1. Extend the existing manifest updater to support this structure. Publish immutable content before activating its manifest, verify checksums, and switch releases only after all required files validate. A missing or incompatible update must leave the prior valid bank usable.
6. Test the installed PWA and offline practice after caching, including required bank files, passages, and diagrams. Updates must not replace an active session's content or deadline. Verify that a returning installation receives the new release without losing history.
7. Push/merge the validated release to the production branch and deploy to Vercel production. Record the Git commit, bank release ID/checksum, and deployment URL; smoke-test the live URL and verify it serves the intended release.
8. Document rollback to the prior app and compatible bank release. Phase III ends only after production verification, not after a local build or repository upload.

#### Milestone 2 acceptance

1. Each of the five sections offers both a working **5-minute burst** and **full-section practice** with its verified question count and time limit. Verify all ten section/mode combinations, including setup labels, deadlines, submission, answers/explanations, and correctly labeled results/history.
2. At least 500 eligible questions are released across the five sections, with complete passage groups, evidence records, and required human sample decisions.
3. The full practice exam enforces section boundaries, correct deadlines, safe resume, and accurate results without leaking answers between sections.
4. Automated checks cover each new content type, form selection, scoring, passage grouping, migrations, bank updates, and exam transitions. Actual iPad QA covers the long Reading layout and all section modes.
5. GitHub contains the reproducible app and broader bank release. Vercel production serves that exact release, with a recorded successful smoke test and rollback path.
6. The released bank has five separate section files and one shared manifest with accurate versions, counts, and checksums; Reading passage references resolve. Verify section/skill filtering, assembly across all five files, offline access, and that an incomplete or invalid update cannot replace the prior working bank or alter a saved session.

### 11.4 Scope boundaries and implementation order

Keep the app single-profile and local-first. Accounts, cloud sync, payments, live AI generation, adaptive recommendations, optional school tests, and official-score prediction remain outside Phase III. Custom accommodation presets can follow later; the initial release uses the standard timings above.

Within Milestone 1: generalize configuration and session state → implement 52-question UX/selection → validate content suitability → verify timing and iPad behavior.

Within Milestone 2: establish the shared section/passage schema, manifest, validators, loader, and content process → verify them with small fixtures → implement renderers and author/review the four new section banks → add the five-section exam → complete integration/iPad verification → release through GitHub to Vercel.

The 100-per-section bank floor and burst question counts are proposed product decisions. Offering both a five-minute burst and full-section practice for every section is a confirmed requirement. Repository/deployment destinations and release owners must be recorded before deployment. Human content review is a real delivery dependency; scheduling should account for the four new review packets and corrections.

## 12. Implementation handoff

Use this consolidated PRD as the working product specification. Inspect the existing app and the question-bank process before making changes. Preserve the existing experience, saved sessions, and accepted content. Implement Phase III in its two milestone order; use the section presets and both required practice modes for every section. Treat proposed bank volume and burst question counts as planning defaults, not verified existing capabilities. Complete real content-review gates and iPad verification before claiming release readiness. Finish with the app and broader bank in GitHub and a verified Vercel production deployment, recording the release identifiers and rollback path.
