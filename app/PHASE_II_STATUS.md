# Phase II implementation status

Local milestones A–D are implemented. This is not a claim that the PRD's external acceptance criteria have passed. The owner requested local implementation and a prepared publishing workflow, with no remote setup/deployment in this turn.

## Implemented

- **A:** IndexedDB v2 migration retains prior sessions and rebuilds exposure. Bank releases are separate from application selection data. Session assignment/exposure and progress imports are transactional. Existing active sessions win concurrent tab starts. Answer/flag writes merge changed fields; completed sessions cannot be reopened by stale writes. Backup export, validation, preview/confirmation, deduplication and separate progress reset are available.
- **B:** Owner build/validate/preview/publish/rollback commands use checksum-bound accepted evidence. Added/revised/retired counts, explicit revision increments, immutable release files and retained rollback targets are enforced. Approved 100-question release `quantitative-v0001` is served locally. Vercel configuration and GitHub validation workflow are prepared.
- **C:** Startup and manual manifest checks, schema/checksum validation, atomically installed bank releases, last-valid-bank fallback and download/error states. PWA app caching and network-only manifest checks. In-progress snapshots remain unchanged. Storage failure offers retry or acknowledged temporary practice.
- **D:** Unseen first, skill/format and difficulty diversity, family/variant diversity, least-recently-seen review ordering, 14-day/five-subsequent-session cooldown, explicit shorter/review alternatives. History includes scores, attempt counts, duration and neutral sample-sized skill summaries.

## Verification

42 automated tests pass, including migration from a fake-indexeddb version-1 store, concurrent starts, stale answer merging, quota rollback during bank installation/session assignment, update/correction/retirement/rollback, corrupted/incompatible/offline downloads, exact saved snapshots, backup deduplication/reset, malformed/conflicting imports, cooldown, immutable owner builds, activation/rollback, and acceptance rejection. TypeScript and production/PWA build pass.

The managed local pnpm runtime required `pnpm_config_verify_deps_before_run=false` to run the build against the existing dependency installation; its automatic dependency-repair prompt was declined by the noninteractive environment. No dependency files were deleted or reinstalled. Fresh CI/deployment setup should use the documented frozen-lockfile install.

## Still pending

- Git repository creation/connection, Vercel project configuration, preview and production deployment: explicitly deferred by owner.
- Real-browser publishing-to-practice exercise, offline PWA navigation and physical iPad Safari checks: pending. Browser automation was blocked because its security-policy check was unavailable; no alternate browser-control route was used.
- An actually accepted expanded bank beyond the existing 100: not invented or falsely approved for a deployment test. Automated tests exercise additions using isolated test data.

Use [CONTENT_PUBLISHING.md](CONTENT_PUBLISHING.md) for owner commands, setup instructions and the manual acceptance checklist. Keep the same stable production origin when deployed; local ports and preview domains have separate student progress.
