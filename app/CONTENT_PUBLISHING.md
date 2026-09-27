# Publishing accepted questions

Phase II local implementation. GitHub/Vercel setup and production publishing are intentionally pending at the owner's request. There is no student backend, login, or cloud history. Commands below modify local release files; they never upload content or credentials by themselves.

## Files and identity

- `public/content/manifest.json`: current manifest, fetched with network revalidation.
- `public/content/banks/quantitative-v0001.json`: first immutable, complete release of the accepted 100.
- `content/releases/`: proposed manifests and release receipts; keep these for rollback.
- `content/staging/` and `content/review/`: authoring, mathematical/editorial/visual evidence, sample decisions. These are not automatically loaded into practice.
- Browser IndexedDB `hspt-practice`, version 2: sessions, exposures, installed banks, active-release pointer. The version-1 migration preserves existing sessions and rebuilds exposure.

A question's `id` is permanent; `revision` starts at 1. Corrections retain the ID, increment revision, and require new content acceptance. New questions receive new IDs. Batch sample acceptance and individual sample approval are separate fields. The other 80 are explicitly `not_individually_reviewed`.

Historical sessions snapshot questions, keys, diagrams, bank release and revisions. Their scores never switch to a corrected answer from a later release. Legacy Phase I snapshots without guides retain exact-match recovery from the archived bank; that archive is not a selection fallback.

## Build an accepted addition

Run from `app/` using Node 24 and pnpm. No credentials are needed for local operations.

```sh
pnpm install --frozen-lockfile
pnpm content build --release quantitative-v0002 \
  --batch content/staging/NEXT_ACCEPTED_BATCH \
  --review content/review/NEXT_ACCEPTED_BATCH
pnpm content validate --release quantitative-v0002
```

Finish `content/QUESTION_IMPORT_PROCESS.md` and the canonical creation process first. This release tool consumes the checksum-bound v2 evidence format used by `gables-v2`: `bank.json`, `validation.json`, `item-audit.json`, `editorial-review.json`, `visual-review.json`, `overlap-log.json`, and the corresponding review `manifest.json`/`decisions.json`. Full batches of 100 require 20 approved sampled items per hundred. Every item needs mathematical and editorial coverage. Diagram files must match the visual-review hashes. Missing, stale, rejected or unresolved evidence blocks publication. Evidence is owner-controlled review documentation, not cryptographic independent attestation.

For a text-only future batch, still supply `visual-review.json` bound to the batch with an empty `assets` object and an explicit not-applicable inspection note. New formats require both compatible app support and independent validators before acceptance; browser structural checks do not establish mathematical correctness.

`build` combines the batch with the current release, reports added/revised/retired/total counts, writes the immutable complete bank and proposed manifest, and leaves the active manifest unchanged. Unchanged records retain their previous acceptance. Exact duplicate stems/choices/diagrams and ID collisions are rejected. Source-semantic overlap remains part of editorial review.

For corrections and retirements:

```sh
pnpm content build --release quantitative-v0003 \
  --batch content/staging/ACCEPTED_CORRECTIONS \
  --review content/review/ACCEPTED_CORRECTIONS \
  --revise gb2-057 --retire gb2-058
```

The corrected `gb2-057` must explicitly have revision 2 if its published revision was 1, and the changed content must have fresh acceptance evidence. Comma-separated lists are supported. Reusing a release ID/URL is refused. Do not overwrite or delete old immutable bank files.

## Preview and validate

```sh
pnpm content preview --release quantitative-v0002
pnpm build
pnpm preview --host 0.0.0.0
```

`preview` activates the proposed manifest in the local working tree. Use a Git branch for candidate content. Vite's production preview defaults to a different origin/port than development; it has separate local progress. Export first when moving between origins. Production preview tests the PWA build; development mode is not an offline-install test.

The build validates the active manifest, its target/checksum/schema/count, and acceptance receipts before building the app. Tests cover the release workflow, browser migration/delivery failure/rollback, and selection. A missing target fails the build. Published JSON is copied from `public/` into `dist/`.

## GitHub → Vercel setup (not performed yet)

Use a private repository containing this project with `app/` as a subdirectory, the root creation-process Markdown, and `.github/workflows/validate.yml`. Do not commit `node_modules`, `dist`, exported student backups, credentials, or temporary test data. Configure Vercel's Root Directory as `app`, framework Vite, and Node 24. The checked-in `app/vercel.json` specifies the build/output and content-cache headers; enable the Git integration and choose a production branch. File-based Vercel configuration is documented in [Vercel project configuration](https://vercel.com/docs/project-configuration).

Use branch protection requiring the validation job and review before merging. Vercel preview deployments must pass the manual checks below. `publish` does not itself attest that these external checks occurred.

## Publish

```sh
pnpm content publish --release quantitative-v0002
pnpm build
```

This revalidates acceptance and atomically replaces the local manifest. Commit the candidate bank, proposed manifest/receipt, active manifest, accepted source evidence and review decisions to a branch. Verify the Vercel preview, then merge the accepted branch into the configured production branch. Vercel deploys app files and bank files together. No new source-code edits are needed for compatible additions.

Bookmark one stable HTTPS production address on the iPad. Preview/deployment URLs have independent browser storage. Confirm the existing production browser receives the new release from **History & settings → Check for new questions**, retains old results and exposures, and can use the additions. An unfinished session must retain its original questions and deadline.

## Roll back content

```sh
pnpm content rollback --release quantitative-v0001
pnpm build
```

Commit and deploy that manifest change through the same branch/review process. The old bank must remain present with valid acceptance evidence. Rollback switches content identity, not a monotonic version counter. It does not revert app code, delete sessions, reset exposure, or alter historical scores.

## Browser behavior and recovery

The last valid bank is usable while an online update runs. The manifest uses a network-only service-worker rule; immutable bank responses can be cached. Downloads must match schema, checksum, count and supported question formats before an atomic IndexedDB installation. Failed downloads or writes keep the previous active bank. First-load failure shows a retry, never a bundled draft test.

New sessions and their exposures are recorded in one read/write transaction. Competing tabs return the already active session. Answer/flag writes merge changed fields against the previous snapshot, and completed sessions cannot be reopened by stale writes. Unseen IDs are preferred, with family/variant and difficulty diversity. Seen questions require both 14 days and five subsequent completed practices; insufficient content requires an explicit shorter set or review set. A shorter timed set still has five minutes.

Backups are local JSON files with a format version, session snapshots and exposure history. Imports are validated and summarized before confirmation. Existing session IDs stay unchanged; repeated imports do not multiply encounters. A conflicting additional unfinished session is refused. Reset deletes progress only, retaining the question bank. Storage persistence is requested on a user gesture, without promising permanent storage.

## Manual browser/iPad acceptance checklist — pending

1. First-load download: practice stays disabled until a valid bank is available; disconnect before first fetch and verify Retry.
2. Complete a burst, answer/flag an unfinished burst, reload, and reopen the same origin. Confirm answers, deadline, history and exposure.
3. On a second tab click Begin simultaneously; verify both resume the same saved session. Change different answer rows and verify persistence.
4. Install the production PWA and load a bank, then disconnect. Start/finish practice and reopen offline. Verify the installed bank and saved progress.
5. Publish an actually accepted expanded bank to a Vercel preview, then production. Keep a session unfinished during update; it must not change. Check new IDs become unseen, revised IDs keep exposure, and retired IDs disappear from new selection.
6. Exercise content rollback and a broken/incompatible candidate in a test deployment. The previous valid local bank and all history must remain.
7. Exhaust a focus. Verify available count, explicit short/review choice, no silent cooldown relaxation, and correct grading of diagrams and pair answers.
8. Export a backup, reset progress, import it twice, and compare sessions/exposure; confirm the bank remains installed. Use a separate test profile for destructive checks.
9. Check iPad Safari landscape and portrait, VoiceOver descriptions, large touch targets, scroll alignment, background timer expiry and audible/visible completion.
10. Simulate storage denial/quota in a test profile. Verify failed bank install/session start is atomic, Retry works, and temporary practice requires acknowledgment.

Browser automation could not run here because the browser security-policy check was unavailable. GitHub/Vercel configuration, real-browser end-to-end publishing, and physical iPad verification remain external acceptance requirements. No additional unreviewed questions were created to simulate a genuine accepted expansion.
