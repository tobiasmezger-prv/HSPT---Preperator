# Phase III content release — app 0.3.0

## Integrated

- Active immutable bank: `all-sections-v0002`, 500 questions, exactly 100 per section.
- All 400 reviewed additional-v3 questions replace the 40 UI dummy questions. Quantitative's 100 accepted questions are unchanged. Historical dummy snapshots remain readable and labeled; the dummy fixtures now live under tests only.
- Tobias approved the fixed 20-question sample per additional section in the project conversation on September 27, 2026. The new approval receipt binds the exact reviewed files and evidence; original staging files and pending browser decision templates remain historical artifacts, not the active acceptance record.
- Verbal/Language/Mathematics skill filters, answer keys, explanations and tips are supported. Sixteen Mathematics figures are embedded in the bank. All eight Reading passages are embedded with numbered paragraphs in practice and results.
- Mixed Reading sets use a complete eight-question passage group plus two vocabulary items while a group is available. If only vocabulary remains eligible, mixed practice can use vocabulary alone. A comprehension focus selects one whole group, including its other skills, and explicitly offers a shorter eight-question set. A partly exposed group is unavailable until all its questions are eligible, or review is chosen.
- Full-test previews reserve all 50 questions atomically. Existing saved sessions, guides, diagrams, cooldowns, backups and progress are preserved.

## Validation

54 automated tests pass. Release evidence/checksums, unchanged reviewed content, selection/group cooldown, all-section scoring, backup snapshots, concurrent sessions, shortened full-test transitions, and stale approval rejection are covered. TypeScript and the production/PWA build pass.

Local browser checks confirmed five 100-question cards, Reading passage paragraphs, saved answer reload/resume, results, and six original Mathematics diagrams in a geometry set. These checks do not certify actual iPad Safari or deployed/offline behavior.

## Remaining Phase III work

This is a content update to the existing preview, not completion of all PRD milestones. Section previews still contain 10 questions with five-minute timers; the five-section preview has 50 questions and 25 timed minutes plus breaks. Full-length section presets, a 298-question exam and corresponding long-session backup limits are not implemented. Full-length coverage/timing acceptance, physical iPad Safari checks (including offline/background recovery), and GitHub/Vercel production verification remain open.

No remote upload or deployment was performed while preparing this version. See `../GITHUB_UPLOAD.md` for the upload handoff.
