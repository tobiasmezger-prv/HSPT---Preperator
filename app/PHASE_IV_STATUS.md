# Phase IV implementation status

Version **0.4.0** · local release activated September 29, 2026.

## Current status

Phase IV timing, navigation and source-bank integration are implemented in the local build. The active immutable release is `all-sections-v0003`: **1,691 questions**, preserving all 500 existing records and appending 1,191 reviewed source questions. One repeated question is consolidated, retaining both source locators; all 1,192 source positions are reconciled, with zero blocked records.

See the [current bank index](content/QUESTION_BANK_INDEX.md), [full collection and approved samples](content/review/source-import-v1/index.html), and [publication receipt](content/releases/all-sections-v0003.receipt.json). The imported records include explanations, 57 recreated SVG figures and 18 passages. Original synced sources and historical releases remain unchanged. The 100 prior sample approvals and subsequent integration authorization are recorded; source questions are not calibrated against themselves.

Full sections use 60/18, 52/30, 62/25, 64/45 and 60/25 questions/minutes. Five-minute burst targets are 17, 9, 12, 7 and 12. Full tests contain 298 questions over 143 timed minutes. Whole reading-passage groups are retained. Logo and Abort controls end tests without completed-test statistics; progress and exposure history persist locally.

## Verification

68 automated tests passed across 14 files. Accepted-release validation, TypeScript compilation and the production/PWA build passed. Expanded-bank tests cover exact section/burst counts, passage groups, progress preservation, original-record parity and repeat prevention. Prior repair verification remains documented in the historical record below.

A fresh browser visual check was blocked because browser security-policy verification was unavailable. Actual iPad Safari, deployed offline updates and production acceptance remain outstanding. This release is active locally and packaged for handoff; no GitHub push or Vercel deployment occurred.

## Historical implementation record

The dated notes below describe earlier stages. References to 500 live questions, empty staging or pending import are superseded by the current status above.

### Initial Phase IV implementation

Version: 0.4.0-dev.1 · local implementation, 2026-09-28

## Implemented

- Shared, versioned presets: Verbal 60/18 minutes, Quantitative 52/30, Reading 62/25, Mathematics 64/45, Language 60/25. Five-minute burst targets: 17, 9, 12, 7, 12. Full tests: 298 questions and 143 timed minutes.
- Full tests reserve all sections atomically; independent clocks start only when the student starts each section. Breaks retain state. Late answer saves cannot alter an expired section. Historical preview/untimed snapshots retain their old counts and deadlines.
- Reading selection preserves complete passage groups and finds an exact count where possible; otherwise bursts require explicit shorter-set consent. Full sections cannot silently become shorter sets.
- Dynamic “N questions available” labels. No new untimed-practice option. H logo and visible Abort test controls return home without submission.
- Terminal abort persistence, cross-tab/stale-save protection, exclusion from completed-practice statistics, no cooldown completion credit, retained exposure, and backup support. Entire aborted full tests are excluded, including previously submitted sections.
- Three-choice questions render and validate without a fabricated fourth option. Source figure images have a validated inline image format.
- Existing publication pipeline supports the source-import policy: all-item checks, 20 user-reviewed samples per section, approval of all checked questions including unsampled items, immutable cumulative release, and validated section counts in the overall index. Original bank releases remain unchanged.
- Writable question-creation and publishing documentation updated with the source-import exception.

## Source work staged — not complete

`content/staging/source-import-v1/inventory.json` accounts for all 1,192 source positions (894 Gables + 298 Barron’s). Source hashes and question/page locators are recorded, with Gables keys and known exceptions from the prior audit. The Gables Markdown hash matches that audit’s reconciled source. Barron’s raw numbered transcriptions and Gables page transcriptions are retained for conversion.

The **live bank remains500 questions**. The staged bank.json is empty. A detailed source review and five20-question source-content packets are now delivered in [the review folder](../output/review/barrons-gables-2026-09-28/index.html). All298 Barron’s items have recorded answer reasoning; the894-item Gables audit was hash-reconciled and75 sampled Gables questions freshly rechecked. The historical findings are retained; the September 29 repair pass below resolves the 211 flagged collection records.

These are source-content packets, not release-ready normalized-bank packets. The prior manual sample review is approved and the 211 flagged repairs are complete. Final release-format conversion, remaining full-bank checks and semantic deduplication remain before publication. Existing all-item checks and publisher gates were not bypassed. After those steps, append all accepted unique source questions, not only the100 samples. Source-practiced marking and final source-format coverage checks also remain.

## Verification

- 64 automated tests passed across 13 test files, including new preset/count, passage-fit, abort, stale-save, late-answer, backup, three-choice, source-approval and index checks.
- TypeScript compilation passed; Vite production build and service-worker generation passed.
- Existing accepted 500-question release and historical release checks passed.
- In-app browser: full-test setup shows all five correct counts/times; first section starts with 60 questions/18 minutes; next-section break shows 52/30; next clock starts only on Continue; logo and Abort button return home without Resume or new completed-history entries. Earlier history remains visible.
- Actual physical iPad Safari, offline production update, GitHub/Vercel deployment and the completed source import have **not** been verified or released. This is not final Phase IV acceptance.


## Full source formatting revision — 2026-09-29

The earlier scanned-page packets have been replaced. [The full collection](../output/question-bank/source-formatted-v1/index.html) now contains all 1,192 individual question records, 57 recreated SVG diagrams, and 18 shared reading passages. The five 20-question review packets render those same records. No scanned pages are embedded in these deliverables.

The initial formatted draft carried 211 known-issue/incomplete-source flags. Those findings are historical and are resolved in the repair pass below. Manual review has been approved; no publication was performed. Live bank remains 500; staging bank.json remains empty. Coverage, nonempty choices, passage links, figure references, and unchanged source hashes passed mechanical checks. Browser visual verification was blocked by unavailable admin-policy verification. See the [conversion report](../output/question-bank/source-formatted-v1/README.md).


## Flagged-question repairs complete — 2026-09-29

User approved all prior manual-review items and authorized repair of the 211 flagged questions. **All 211 have recorded resolutions:** 151 content/answer corrections, 51 verified existing repairs or corrected explanations, and nine false-positive source-gap flags. Sixteen related items were also updated as part of seven corrected passages and their 70 dependent questions. All 1,192 source positions are preserved.

The full collection and all five 20-question sample packets now use the repaired records. Editorial adaptations are explicit, original sources are unchanged, and the baseline plus per-item before/after history are preserved. No self-calibration against Gables was added.

99 targeted checks passed, including 47 exact numeric comparisons against displayed answer choices, competing-answer/identity checks, source hashes, record coverage, all passage links, SVG assets, and sample parity. The seven figures used by repaired items were visually checked. These checks address the flagged repairs and do not substitute for remaining full-bank publication checks or difficulty calibration.

See [the repair report](../output/question-bank/source-formatted-v1/repair-2026-09-29/REPORT.md) and [searchable before/after comparison](../output/question-bank/source-formatted-v1/repair-2026-09-29/index.html). The live bank remains 500; staged bank.json remains empty. The source import has not been published.


## Horizontal logo integrated — 2026-09-29

The approved HSPT Preparator horizontal wordmark is included in `public/branding/hspt-preparator-horizontal.png` and the shared home/setup/progress/settings/break header. Responsive sizing keeps the wordmark compact; the original home/abort handler and accessible navigation label are retained. The small H control in the timed-test toolbar remains to preserve question/timer space. The production build includes and precaches the PNG for offline use.

Validation: all 64 tests passed, TypeScript and production/PWA build passed, and the copied production asset and offline precache entry were verified. Browser visual verification was blocked because the browser security-policy check was unavailable. This local integration has not been deployed.


### Logo palette matched — 2026-09-29

The horizontal wordmark now uses the app’s primary green (`#234d46`) for HSPT and headline color (`#253731`) for Preparator. A CSS alpha mask preserves the approved lettering and transparent artwork while applying exact interface colors. The local preview updates automatically. Production build and all 64 tests passed.

HSPT lettering subsequently changed to Georgia, matching the main headline’s serif family, weight, and letter spacing at logo size, per user preference. Preparator retains its original graffiti artwork, isolated with the same alpha mask.
