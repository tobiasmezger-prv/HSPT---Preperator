# Product Requirements Document: HSPT Practice
**Version:** 2.6 — Phase IV exam pacing and reviewed source-bank imports  
**Platform:** iPad-first responsive web application (Safari; landscape optimized)  
**Primary user:** One middle-school student preparing for the HSPT  
**Initial build:** Phase I — Quantitative Skills prototype  
**Status:** App 0.3.0 has 100 questions per section (500 total), ten-question/five-minute section previews, and a 50-question/25-minute full-test preview. Phase IV is the next planned implementation: correct exam pacing and full-length presets, plus reviewed imports from the Gables and Barron’s Markdown sources. Physical iPad and production checks remain required. See [implementation status](app/PHASE_III_PREVIEW.md).

This is the working overall PRD. It consolidates the original Phase I requirements, the Phase III plan, and the Phase IV requirements in section 12. Phase IV supersedes earlier proposed ten-question bursts and carries forward the unimplemented full-length requirements from Phase III. The synced original under `sources/` remains a read-only historical reference. The content-review policy follows [QUESTION_BANK_CREATION_PROCESS.md](QUESTION_BANK_CREATION_PROCESS.md).

## 1. Product vision
Build a calm, paper-like HSPT practice experience that trains both accuracy and speed. A student should be able to sit down with an iPad, launch a timed practice burst, answer questions in any order on a familiar question-and-answer-sheet layout, and receive useful explanations and actionable performance feedback.

The long-term product supports all five HSPT sections, full-length and section-specific tests, an effectively unlimited *validated* question library, progress analytics, and adaptive five-minute practice for recurring weaknesses. Phase I deliberately implements only Quantitative Skills, using a curated question bank rather than live AI generation.

**Product principles:** (1) Authentic paper-test feel, (2) fast to start and easy to navigate, (3) accurate questions before volume, (4) speed and accuracy measured separately, (5) student privacy and minimal distraction.

## 2. Scope and phased delivery
| Capability | Phase III baseline (app 0.3.0) | Phase IV — next | Later |
|---|---|---|---|
| Platform | iPad-first browser/PWA, local progress | Preserve Safari, offline, backup, and resume behavior | Native app only if justified |
| Sections | All five core sections | All five with correct pacing and full-length modes | Optional school tests if justified |
| Bursts | Up to ten questions in five minutes | Section-specific counts derived from exam pace | Adaptive practice |
| Section tests | Ten-question, five-minute previews | 60/52/62/64/60 questions with the matching section deadlines | Accommodation presets |
| Full test | 50-question, 25-minute preview | 298 questions; 143 timed minutes | — |
| Bank | 100 questions per section, 500 total | Review and import all Gables/Barron’s source questions, preserving the existing bank | Expanded validated supply |
| Progress | Browser-local sessions and exposure | Preserve history; distinguish source practice and exam modes | Final Phase V: email-passcode accounts and sync |
| Delivery | GitHub-ready source package | GitHub → Vercel app/content release, verified on iPad | — |

**Scope reassignment:** Section 11 retains the earlier two-milestone Phase III plan as historical requirements. The implemented baseline is app 0.3.0, not completion of every item in that plan. Correct burst pacing, full sections, and the full 298-question exam are now explicitly Phase IV work, governed by section 12. This reassignment does not waive content or release checks.

**Not in Phase I:** live LLM question generation, official HSPT copyrighted content, cloud sync, payment, leaderboards, social features, full-length exam simulation, parental monitoring, or inferred standardized-test scores.

## 3. Users and primary journeys
**Student:** launches a practice burst in two taps; can answer questions in any order, change answers, flag and revisit items, and review explanations afterward. Can hide the timer without stopping it.

**Parent:** can see recent practice history and understand whether mistakes arise from knowledge gaps, slow solving, or unanswered items. No separate parent account in Phase I.

**Phase I flow:** Home → choose Quantitative Skills → choose Mixed or a skill focus → start 10-question/5-minute burst → paper-style test → submit or auto-submit at time expiry → score/review → history.

**Phase IV section flow:** Home → choose any of five sections → choose **5-minute burst** or **Full-section practice** → confirm count/timing → test → results and explanations → section/mode history. Phase IV removes the untimed option for new practice; bursts default to five minutes.

**Phase IV exam flow:** Home → full five-section practice exam → section instructions → timed section → transition/break → next section → final results and review.

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

**Phase IV:** Correct section-specific burst counts, full-section timing/counts, and the complete 298-question test; review and integrate all questions from the Gables and Barron’s Markdown sources. Detailed requirements are in section 12.

**Deferred enhancements:** Controlled AI-assisted generation, adaptive recommendations, and richer visualizations remain future work and are not part of Phase IV. AI must not directly publish unverified items.

**Phase V — final planned phase:** Student email accounts using emailed one-time passcodes, with account-scoped online history and cross-device repeat protection. Keep local-only practice available. Do not store student passwords; use managed authentication, expiring single-use codes, resend/attempt limits, and a configured email delivery service. Import local history explicitly and idempotently; isolate account data at sign-out and synchronize offline uploads without duplicate sessions. Cross-device repeat guarantees require connectivity. Accounts and cloud progress are outside Phase IV.

### Current implementation baseline

The inspected GitHub-ready package is `output/github/HSPT-Phase-III-v0.3.0`, with content release `all-sections-v0002`. It contains 100 questions in each of the five sections. Its session logic still selects ten questions per section and assigns five-minute deadlines; a full-test preview contains 50 questions. These are separate facts: expanded bank volume does not imply implemented exam presets. The intended GitHub repository is `tobiasmezger-prv/HSPT---Preperator`; confirm the connected Vercel project and production address before release. Do not infer a deployed version from a local package.

## 11. Earlier Phase III requirements and delivery

**Historical plan:** Full-length requirements not implemented in app 0.3.0 are carried into Phase IV. Where timing, burst counts, source-content policy, or scope conflict, section 12 takes precedence.

**Outcome:** Full-section practice, then a five-section app and broader reviewed question-and-answer bank, ending with a GitHub-to-Vercel release.

### 11.1 Verified exam structure

**Thirty minutes is correct for Quantitative Skills only.** The app uses one Verbal preset: 60 questions in 18 minutes. This table is aligned with the Phase IV requirements in section 12.

| Section | Questions | Time limit |
|---|---:|---:|
| Verbal Skills | 60 | 18 minutes |
| Quantitative Skills | 52 | 30 minutes |
| Reading | 62 | 25 minutes |
| Mathematics | 64 | 45 minutes |
| Language | 60 | 25 minutes |
| **Total** | **298** | **143 minutes (2 hours 23 minutes)** |

Section scope and counts: [STS interpretive manual](https://www.ststesting.com/hp_int_sts.pdf). Timing reference for the chosen preset: [STS E-Score administration manual](https://adwcatholicschools.org/wp-content/uploads/_pda/2018/08/HSPT-EScore-User-Manual.pdf). The supplied Barron’s sample also uses 18 minutes for Verbal. This is the app’s selected practice configuration; do not add alternative Verbal profiles or a profile selector.

The arithmetic is **18 + 30 + 25 + 45 + 25 = 143 minutes**. Label the complete exam **“2 hours 23 minutes of timed questions, plus breaks.”** Instructions and breaks are additional; actual school appointment duration depends on local administration. Do not model the test as five 30-minute sections or assume a universal break schedule. Optional school-specific tests remain outside this phase.

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

- Add a five-section home/setup flow. **Every section must offer both a 5-minute burst and full-section practice.** Present these as two clearly labeled choices after selecting a section; neither option is optional or limited to Quantitative Skills. Phase IV removes the untimed option for new practice; bursts default to five minutes.
- Every burst has a five-minute deadline. Proposed burst question count: 10, explicitly labeled practice pacing rather than official exam pacing; Reading passage-group handling is specified below. Full-section practice uses the verified count and time limit for the selected section.

| Section | Required burst option | Required full-section option |
|---|---|---|
| Verbal Skills | 5 minutes | 60 questions · 18 minutes |
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
- Reveal answers after the entire exam is completed. Phase IV supersedes early-end behavior: intentionally aborting an exam produces no scored results and does not count toward statistics (see 12.2.1).
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

## 12. Phase IV — Correct exam pacing and reviewed source imports

### 12.1 Outcomes and boundaries

1. Every section offers a five-minute burst with an appropriate section-specific question count.
2. Full-section practice uses the actual section count and time allocation; the full test combines all five sections with independent clocks and 298 questions.
3. Inventory, review, and import all questions from both source collections into the test bank, including their passages, figures, answer keys, and explanations where available.
4. Preserve the current 500-item bank, stable IDs, progress, repeat protection, offline behavior, and existing session snapshots. Do not replace the bank with the imports or silently reset local history.

This is a PRD update, not evidence that these features or imports have been implemented, reviewed, uploaded, or deployed. Accounts, cloud progress, live AI generation, adaptive practice, and standardized-score predictions are not in this phase.

### 12.2 Shared timing and count configuration

Create one versioned preset source used by selection, session creation, setup labels, countdowns, transitions, results, and tests. Remove hard-coded ten-question/five-minute assumptions from full-section and exam code. A burst always has a five-minute deadline; full-section deadlines depend on the selected section.

| Section | Full-section questions | Section minutes | Average seconds/question | Five-minute burst target |
|---|---:|---:|---:|---:|
| Verbal Skills | 60 | 18 | 18.0 | 17 |
| Quantitative Skills | 52 | 30 | 34.6 | 9 |
| Reading | 62 | 25 | 24.2 | 12 |
| Mathematics | 64 | 45 | 42.2 | 7 |
| Language | 60 | 25 | 25.0 | 12 |

**Calculation:** average seconds per item = section minutes × 60 ÷ section questions. Burst target = round(section questions × 5 ÷ section minutes), using nearest-integer rounding. Whole questions make this an approximation; do not describe rounded bursts as mathematically identical to exam pace. Reading time includes reading the passages.

**Verbal preset:** Use **60 questions in 18 minutes**, matching the supplied Barron’s sample and the 18-minute instructions in the [STS E-Score administration manual, printed page 12 / PDF page 14](https://adwcatholicschools.org/wp-content/uploads/_pda/2018/08/HSPT-EScore-User-Manual.pdf). The user has selected this single configuration for the app. Do not implement a second Verbal timing option or a profile picker.

- Full-test total: **298 questions / 143 timed minutes (2h 23m)**. Breaks and instructions are additional.
- Persist preset ID/version, actual question count, duration, section, and mode in new sessions. Preserve earlier preview sessions as previews with their original deadlines and counts.
- Remove the unlimited/untimed option from all new-practice setup screens. Bursts default to a five-minute timer; full sections and full tests retain their configured exam deadlines. Hiding the timer never pauses it. Preserve legacy untimed session history, backups, and any already-started untimed session without converting or deleting them.

### 12.2.1 UX simplifications

- **Available-question labels:** On the section/question-bank selection screen, use “100 questions available” instead of “100 questions.” Derive the number from the installed eligible bank for that section; do not hard-code 100. Use singular wording for one question. This label describes the section’s available bank, not the size of the next burst or the number never seen; show cooldown-filtered availability separately in setup when it affects selection.
- **Timed practice by default:** Remove the unlimited/untimed practice option, entry points, and mode selector for new practice. A burst starts with the five-minute timer by default. Full-section and full-test modes still use their correct section-specific limits; this simplification does not turn them into five-minute tests. Timer visibility can still be toggled without pausing the clock.
- **H logo navigation:** The H logo and adjacent app-name link take the student to the Practice home screen. During an active burst, full section, or full test (including between-section breaks), clicking either aborts the active attempt before returning home. Use an accessible label that communicates “Abort test and return home” while a test is active; otherwise use “Home.”
- **Explicit abort control:** Once a test starts, show a clearly visible “Abort test” button on every question and between-section break screen, with a comfortable touch target. It performs the same action as the H logo: end the attempt and return home without requiring submission. Aborting a full test discards the entire attempt from statistics, including any sections already completed within it.
- **Aborted attempts do not count:** Persist a terminal aborted status and abort timestamp, stop its timers, release its active-session lock, and remove its Resume option. Do not submit, score, show a results screen, or reveal answer keys as part of aborting. Exclude the entire attempt from scores, accuracy, question/section completion totals, practice time, skill trends, streaks, and all progress statistics and their denominators. Do not treat unanswered items as incorrect or create a zero score. If retained in history, label it “Aborted” with no score and keep it separate from completed attempts.
- **Persistence and interruption:** Persist abort consistently so another tab, delayed save, timer callback, reload, or backup restore cannot revive or count the attempt. Keep recorded question exposure separate from performance statistics to prevent immediate repeats; an aborted attempt does not earn completed-session cooldown credit. Refreshing, backgrounding Safari, or closing the browser without explicitly aborting retains the existing resume behavior and original deadlines. Apply the existing save-failure warning if the abort cannot be persisted.
- **Compatibility:** Removal of new untimed practice does not invalidate older saved sessions or backups. Preserve their original behavior and labels as historical/legacy practice.

### 12.3 Burst selection, full sections, and exam behavior

**Five-minute bursts**
- Use the targets above for every new burst, including skill-focused practice and results-page practice actions. Prefer unseen questions, then respect the existing cooldown; review explicitly permits earlier repeats.
- Reading must preserve coherent passage groups and appropriate vocabulary items. Target 12 questions. Prefer an exact fit using complete groups plus vocabulary; if a coherent set cannot hit the target, offer the largest suitable set below it, disclose its count and that its pace differs, and require the shorter-set choice. Never cut a passage’s dependent questions arbitrarily merely to meet a count.
- If eligible content is insufficient in any section, offer a clearly labeled shorter burst, explicit review, or another focus. Never silently repeat an item or extend the five-minute timer.

**Full-section practice**
- Assemble exactly 60 Verbal, 52 Quantitative, 62 Reading, 64 Mathematics, or 60 Language questions, using the section’s configured time limit. Selection must meet documented coverage and content eligibility, not only count.
- Full sections use a representative mixed selection. Skill filtering belongs to burst practice. Use complete Reading groups, include required figures, and avoid duplicate IDs and near-identical variants where feasible.
- If a full section cannot be assembled, explain what is missing. Offer explicit review when exposure limits are the issue; do not silently substitute a short preview for a full section.
- Preserve answer-sheet navigation, flags, corrections, and question jumps across long lists. Record outcomes and review all errors and omissions without implying an official scaled score.

**Full practice test**
- Use Verbal → Quantitative → Reading → Mathematics → Language, with the same verified full-section presets. Persist the complete 298-question form and snapshots before starting; reserve it transactionally to prevent competing tabs from creating overlapping fresh sessions.
- Start only the current section’s clock. Lock a submitted/expired section; unused time never transfers. Returning after expiry finalizes that section once and does not automatically start the next.
- Between-section breaks remain an explicit practice setting, stored separately from timed work. Do not present a universal official break schedule. Display timed total and optional break duration separately.
- Resume retains the current section, original deadline, completed parts, and break state. Account for clock expiry while Safari is backgrounded and reject late answers.
- Reveal keys and explanations only after completing the exam. Intentional early exit uses the abort behavior in 12.2.1: no submission, no scored results, and no contribution from any part of that exam to progress statistics.
- Completed results show per-section scores and total correct out of 298; history distinguishes bursts, full sections, full exams, legacy untimed work, and older preview sessions. Exclude breaks from reported test-working time.

### 12.4 Gables and Barron’s source-bank imports

**Source scope — all questions, not just calibration examples**

| Source | Working reference | Expected raw inventory |
|---|---|---:|
| Gabel/Gables collection | `output/markdown/HSPT_ALL_SIX_PDFS.md` (use the identical synced `sources/` copy when available), including embedded scans and all three test/guide pairs | 894 questions (three 298-question tests), subject to inventory verification |
| Barron’s Practice Test 1 | `output/HSPT Prep Barrons/HSPT Prep Barrons.md`, its embedded images, and supplied PDF as needed | 298 questions, numbered 1–298 |
| Total new source inventory | Before duplicate resolution or review exclusions | 1,192 questions |

Inventory every source question. The target is to make every eligible, reviewed item available in the bank. With the existing 500 items, the arithmetic upper bound is 1,692 items; this is not a promise of that many distinct accepted questions. Reconcile duplicates, missing material, and blocked items explicitly rather than inventing replacements or silently dropping them.

Gables is a collection label, not necessarily the original publisher. Preserve the actual test/book identity for each of its three forms. Do not edit the synced source files. Store converted drafts, review evidence, and acceptance records outside `sources/`.

**Use the existing Phase III framework:** Import the two Markdown collections into the current five section banks using the existing staging, item schema, review packets, acceptance records, immutable releases, and shared manifest/index. Extend that pipeline only where source formats or the simplified sample policy require it; do not create a parallel question-bank system, replace the existing banks, or introduce a database service. Both Markdown files contain embedded page images; use those images for transcription checks.

**Sampling approves the full checked import:** The 20 questions per section are a human-review sample, not the number to import. After the user approves the five samples and correctness/consistency checks pass for every source question, add **all questions from both Markdown collections** to their respective section banks, including the unsampled questions. Sample approval applies to the full checked section import; individual human-review metadata applies only to sampled items. Resolve or correct failed items before accepting the full import. Any item that cannot be resolved must be explicitly reported as blocked, and duplicates linked to existing canonical questions rather than added twice. Do not silently limit publication to the 100 sampled questions or describe a partial import as complete.

**Simplified source-import review workflow**
1. **Inventory and provenance:** Record source file checksum, original publisher/test, section, source question number, page locator, passage/figure references, and source key. Record permitted use/distribution before including third-party content in a public GitHub/Vercel release; unresolved items can be staged and reviewed but remain outside that release. Possessing a Markdown transcription does not establish redistribution permission.
2. **Transcribe against scans:** OCR is a starting point. Check every imported stem, choice, key, and essential formatting against the source images. Verify fractions, exponents, inequalities, underlining, passage line/paragraph references, diagram labels, and answer-key row alignment. Preserve intentional spelling/grammar mistakes in Language questions. Never use a whole page image containing answers as the student-facing question asset; extract only the required figure/passage content.
3. **Normalize without losing source fidelity:** Map items to section-specific skills/formats, stable IDs/revisions, original question numbers, provisional difficulty, template/variant families, and versioned passage/asset references. Imported questions remain distinguishable from original authored items. Support actual source choice counts, including three-choice questions; update validation, answer-sheet rendering, scoring, and backups instead of inventing a fourth distractor.
4. **Check every item:** Run structural validation, duplicate/near-duplicate comparisons against both sources and the live bank, independently recompute math answers, and verify source keys and explanations. For verbal/language/reading, check logical validity, conventions, ambiguity, and passage evidence. A published source key is evidence, not automatic proof of correctness. If a guide is missing, author and review an explanation; do not invent a source attribution.
5. **Provide 20 calibration/review questions per section:** After checking every candidate item, give the user five reproducible review packets: Verbal, Quantitative, Reading, Mathematics, and Language, each containing exactly 20 questions (100 total for this combined source-import delivery). “Calibration” here means the user’s review sample, not another comparison against Gables. Follow the packet format and sampling principles in `QUESTION_BANK_CREATION_PROCESS.md`: questions first, separate answer key and explanations afterward, skill/difficulty/format coverage, risk-based selection, and no cherry-picking. Represent both Barron’s and Gables and, where available, all three Gables forms within each section’s sample. Include complete Reading passages and required figures. Include source locators, stable IDs, a revision-bound sample manifest, and approve/revise/reject fields with notes, reviewer, and date. If fewer than 20 eligible items exist in a section, show all and report the shortfall; never fabricate or duplicate items to fill the packet.
6. **Repair and acceptance:** The user reviews these sample packets to approve the full checked source import for each section, not merely the 20 sampled questions. After sample approval and successful all-item checks, accept all checked questions in that section for integration, including unsampled items. Independently inspect all flagged items in addition to the normal sample, and surface unresolved issues separately. A wrong key, ambiguous wording, broken diagram, or unsupported inference blocks affected content; inspect the relevant family/source region and revalidate corrected revisions. Expand human review only when defects warrant it, rather than automatically multiplying packets by every 100 source questions. Bind decisions and evidence to content hashes; changed questions require fresh relevant checks and review. Record the scope of acceptance (burst/full-section). Unsampled items remain checked but not individually human-approved. Adapt the existing acceptance gate to this explicit source-import policy; never fabricate per-100 approvals to satisfy an older gate.
7. **Reconcile and append:** Produce a report for all 1,192 expected source entries: accepted/imported, duplicate linked to a canonical item, or blocked with a reason. Preserve original source/test mappings after deduplication. After sample approval and all-item checks, every accepted new source question—sampled or unsampled—receives a unique stable ID and is added to its existing section bank alongside the current questions. The 20-question sample is never an import cap. For each section, report previous count, added unique count, duplicate count, blocked count, and resulting total. Re-importing the same source must not add duplicates. Preserve existing IDs, revisions, acceptance records, exposure, and historical snapshots.
8. **Respect known prior exposure:** The project notes that the student has already completed the three Gables tests. Preserve that provenance and offer a clearly labeled source-review path; do not automatically describe imported Gables items as novel to this student. Allow the parent to mark source forms previously practiced without fabricating answer results or exact encounter dates. Normal question-ID exposure and cooldown tracking continues for app attempts.
9. **Update the overall index and publish:** Build new immutable cumulative section bank/asset releases containing the existing questions plus accepted additions. Update the existing shared manifest/index with every section’s correct release reference, question count, schema/version, checksum, and required asset references; derive the overall total from the section counts. Validate index-to-bank counts, unique IDs, references, and checksums together. Publish through the existing GitHub → Vercel workflow. Question-only commits still trigger a website build/deployment. Validate all manifest targets and assets before production activation; browser updates are atomic and never replace an active test’s content. Keep source scans, raw transcriptions, and unresolved imports outside the public release unless explicitly appropriate and permitted.

**Source-import exceptions to the creation process:** `QUESTION_BANK_CREATION_PROCESS.md` remains the framework for checks, sample presentation, decisions, and integration. For these two named Markdown collections only, use the simplified source-import track: import the existing source questions instead of authoring replacements; skip the full Gables difficulty/style calibration comparison for both collections (Gables would otherwise be calibrated against itself); and provide 20 user-review questions per section for the combined import, rather than 20 per 100 source items. Record that comparison as not applicable under this policy, not as a passed calibration. This exemption does not waive scan fidelity, independent answer/explanation checking, consistency, visual checks, duplicate detection, known-source-defect review, or the user’s sample review. Source items are intentionally recognizable imports and must retain provenance rather than being rejected merely for matching their own source. Newly authored questions retain the existing originality and full calibration requirements. Before implementation, document this source-import track in the writable creation-process document and align the existing validators and acceptance gate; synced references remain read-only.

**Ongoing additions are cumulative:** All future question additions, including authored batches and further reviewed source imports, append to the appropriate existing section banks and update the same overall manifest/index. They do not replace a section with only the latest batch or reset the overall index. New releases are complete cumulative snapshots, even when only one section changes; unchanged sections retain valid existing references. Corrections and retirements are explicit separate operations under the existing revision rules, never a side effect of adding questions. Historical releases and active-session snapshots remain intact, and browser activation stays atomic.

### 12.5 Implementation sequence and acceptance criteria

**Milestone A — Presets and pacing:** Implement versioned section presets, rounded burst targets, setup labels, the UX simplifications in 12.2.1, and compatible session migration. Verify 17, 9, 12, 7, and 12-question burst targets and the Reading exception behavior.

**Milestone B — Real-length modes:** Implement all five full sections and the 298-question exam using shared presets, independent section clocks, persisted transitions, abort handling, and long-list/passage navigation. Preserve old preview sessions unchanged.

**Milestone C — Source imports:** Extend the content procedure/schema/validators, inventory all named source questions, transcribe and check them, provide the five 20-question user-review packets, record decisions under the simplified source-import policy, reconcile every item, and append only accepted eligible additions to the existing section banks with an updated overall index. Imports must not bypass the bank’s acceptance gate.

**Milestone D — Verification and delivery:** Run automated configuration, selection, timing, scoring, migration, import, passage/asset, bank-update, and backup checks. Verify on actual iPad Safari, then package and release through the existing GitHub/Vercel destinations with version identifiers and rollback instructions.

Phase IV acceptance requires:
1. Setup and runtime agree on the actual count and deadline for every section/mode, including the single 18-minute Verbal preset. Burst limits remain five minutes; full sections use the table in 12.2.
2. Completed full exams contain exactly 298 unique question IDs, with 143 timed minutes. Tests cover section-boundary locks, timeout after backgrounding, concurrent tabs, late answers, resume, breaks, and aborting.
3. All source questions are accounted for in an import manifest; accepted items are selectable with correct provenance, choices, keys, explanations, and assets. Every blocked or duplicate item has an explicit disposition; remaining blockers are reported rather than calling the entire import complete. Deliver five reproducible 20-question review packets (100 total), with separate keys/explanations and recorded user decisions; all imported items receive correctness and consistency checks, with the Gables comparison explicitly exempted for this source-import track. After sample approval and all-item checks, verify that all accepted source questions, including unsampled questions, are present in the banks; importing only the 100 sample questions does not satisfy this requirement.
4. Reading form assembly preserves complete passages and meaningful references. Math/visual questions render accurately; three-choice source items work without fabricated choices. New bank volume and imported-source exposure are reflected honestly in setup.
5. Existing 500-item content, saved sessions, original deadlines, IDs/revisions, exposure, and backups survive the update. For additions, verify each resulting section bank contains its previous items plus accepted unique additions, the overall manifest/index matches every section and aggregate count, and repeating an import adds no duplicates. Offline use includes all needed passages and figures; a failed release download leaves the prior bank usable.
6. Selection displays the actual “N questions available” label; no new untimed/unlimited entry point remains. The H logo returns home from every screen and aborts any active attempt. Verify both the logo and visible Abort test button during bursts, full sections, full exams, and breaks: no submission is required, no Resume remains, a new test can start, and all performance statistics remain unchanged (including previously completed sections of an aborted exam). Test competing tabs, delayed saves, timer callbacks, reload, and backup restore so an aborted attempt cannot be revived or counted. Verify ordinary browser interruption still preserves resume state and deadlines, with expiry finalized only once. Verify legacy untimed backups still import and their sessions remain readable.
7. GitHub/Vercel release checks record the app version, bank release/checksums, production URL, successful smoke test, and rollback path. Completion claims distinguish local automated tests, actual-device checks, content review, and production verification.

## 13. Implementation handoff

Use this working PRD and the current app 0.3.0 as the baseline. **Implement Phase IV next when build work is requested**, following section 12; do not restart Phase III or assume its earlier full-length requirements are already implemented. First inspect the actual banks, runtime selection/timers, source Markdown/images, and review process. Preserve existing content and student history. Implement shared timing/count presets, correct bursts and full-length tests, then the reviewed Gables/Barron’s import workflow. Do not claim unchecked imports are accepted, deploy unresolved content, or add accounts/AI generation in this phase. Final Phase V retains student email-passcode accounts and cross-device history. Updating this PRD alone does not authorize an immediate deployment.
