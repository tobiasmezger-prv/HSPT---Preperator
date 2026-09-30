# HSPT Practice 0.4.0 — Phase IV

September 29, 2026 (local date) · Content release `all-sections-v0003`

The local build now contains **1,691 questions**. All 500 existing records are preserved, and 1,191 Barron’s/Gables questions are appended. All 1,192 source positions are accounted for: one duplicate is consolidated, with both source references retained. The section and overall indexes are updated.

| Section | Questions available | Full section | Five-minute burst |
|---|---:|---|---:|
| Verbal | 340 | 60 / 18 min | 17 |
| Quantitative | 307 | 52 / 30 min | 9 |
| Reading | 348 | 62 / 25 min | 12 |
| Mathematics | 356 | 64 / 45 min | 7 |
| Language | 340 | 60 / 25 min | 12 |

- Full test: 298 questions and 143 timed minutes, with separate section clocks.
- All 211 flagged source items have recorded resolutions. Final conversion also corrects remaining OCR in explanations and choices; the edit history is retained.
- Imported questions use individual text, 57 recreated SVG diagrams and 18 shared passages. No scanned pages are displayed as questions.
- The previously approved 100 samples and explicit integration authorization are recorded with the accepted batch. Existing full-source review evidence was reconciled; this is not a claim of fresh independent re-solving or psychometric calibration of every item.
- Browser-local progress, historical question snapshots, repeat cooldowns and whole reading-passage groups remain supported.
- Availability labels include “questions available.” New practice defaults to five minutes; full-section/full-test modes have their own timers. Logo and Abort controls end tests without submission or completed-test credit.

Validation: 68 automated tests passed across 14 files; accepted-release validation, TypeScript and production/PWA build passed. Tests cover expanded-bank selection, counts/timers, prior progress, passage groups and repeat prevention. A fresh browser visual check was blocked by unavailable browser security-policy verification. Actual iPad Safari and deployed/offline update behavior remain manual checks.

Activated locally and packaged for handoff; not pushed to GitHub or deployed to Vercel. See the [question bank index](app/content/QUESTION_BANK_INDEX.md).

---

# HSPT Practice 0.3.0 — Phase III content update

September 27, 2026 · Content release `all-sections-v0002`

The four additional sections now use the reviewed 100-question banks instead of development dummy questions. The app has 500 questions total, with the accepted Quantitative bank unchanged.

- Original Mathematics diagrams and Reading passages are included directly.
- Reading selection preserves whole passage groups and numbered paragraphs, with vocabulary mixed into ten-question sets.
- Every section has relevant skill filters, grading, explanations and tips.
- Saved sessions retain their exact questions and guides. Existing progress, backup/restore and repeat cooldowns remain supported.
- The 80 additional sample approvals are recorded from the owner's explicit chat approval, bound to the reviewed files. Unsampled items are accepted as part of the sample-reviewed batch, not individually human-approved.
- The old dummy data is now a historical test fixture only.

Validation: 54 automated tests, release checks, TypeScript and production/PWA build passed. Local browser checks covered section counts, passage rendering, saved-answer resume, results and Mathematics figures.

This version retains 10-question section previews and the 50-question five-section preview. Full-length modes and the 298-question exam remain open PRD work, along with actual iPad Safari, offline/background and deployed production verification. No official score or calibrated difficulty claim is made.

Prepared for GitHub upload; not pushed or deployed by this task.
