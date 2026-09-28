# Upload HSPT Practice 0.3.0

Target repository: [tobiasmezger-prv/HSPT---Preperator](https://github.com/tobiasmezger-prv/HSPT---Preperator).

The delivery ZIP contains a complete source folder, including the `app/` folder, `.github` validation workflow, lockfile, accepted banks, review evidence and documentation. It excludes installed dependencies, compiled files, local progress, project source PDFs/Markdown, temporary checks and previous delivery archives.

## Add the next version

1. Unzip the delivery package. Use the **contents** of `HSPT-Phase-III-v0.3.0`, not the enclosing folder or the ZIP itself, at the repository root.
2. In GitHub Desktop, open or clone the repository. Create a branch such as `phase-iii-reviewed-banks` for this update.
3. Copy the extracted contents into that checkout, including hidden `.github` and `.gitignore` files. Preserve the checkout's `.git` folder. Remove `app/src/data/previewQuestions.ts` if the older version contains it; the historical fixture has moved to `app/tests/fixtures/legacyPreviewQuestions.ts`.
4. Review the changes and commit with **“Integrate reviewed banks across all five HSPT sections”**, then publish the branch.
5. Let the GitHub validation workflow finish and check the Vercel preview before merging to the production branch. A connected Vercel project can deploy automatically on push/merge.

The ZIP also contains `PACKAGE_CONTENTS.sha256`, listing exact source-file hashes for this delivery. No credentials are included or needed by the app.

## Build configuration

- Node.js: **24.x**, already pinned in `app/package.json`.
- Package manager: **pnpm 11.25.0**.
- Vercel root directory: **app**.
- Framework: **Vite**.
- Install: `pnpm install --frozen-lockfile`.
- Build: `pnpm build`.
- Output: **dist**.

For local development, run those install/build commands from `app/`, then `pnpm dev`. The managed development runtime used a local `pnpm_config_verify_deps_before_run=false` override because its pre-existing dependency installation triggers an automatic repair prompt. That override is not committed as a deployment setting; CI starts with a frozen-lockfile installation.

## Preview checks before production

Export existing progress first if you want a personal recovery copy. Keep it private. On the stable production origin, updates preserve browser-local progress; a different preview URL has its own separate storage.

Confirm 100 questions in all five sections, Reading passages and Mathematics figures, answer/submit/review, resume after backgrounding, and download/offline behavior on the actual iPad. The content update is ready to upload, but physical-device and deployed behavior have not been verified here.

Section/full-test modes remain shortened previews. Completing the full Phase III PRD still requires full-length presets and the 298-question exam. See `app/PHASE_III_PREVIEW.md`.

## Recovery

Keep the previous app deployment available. For deployment rollback, restore its compatible app and bank together. `quantitative-v0001` remains in the source as an immutable content rollback target; selecting it in this app disables new practice in the other four sections while preserving historical snapshots.
