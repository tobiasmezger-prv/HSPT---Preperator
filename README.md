# HSPT Practice

An iPad-first, paper-style practice app covering all five HSPT sections. Version **0.4.0 (Phase IV)** includes **1,691 questions**: the original 500 plus 1,191 reviewed Barron’s/Gables additions, with explanations, recreated vector diagrams, and shared Reading passages. The approved 20-question samples per section represent the imported batch; unsampled questions are not individually human-approved.

Five-minute bursts use section-specific question counts. Full sections use the correct counts and timers, including 60 Verbal questions in 18 minutes. The full test has 298 questions and 143 timed minutes. The H logo and Abort test button end a test without counting it in completed-test statistics.

Question-bank updates are versioned. Progress, answer snapshots, backups, and repeat cooldowns stay on the device; no account or backend is required.

## Run locally

Use Node 24 and pnpm 11.25.0:

```sh
cd app
pnpm install --frozen-lockfile
pnpm dev
```

## Validate and build

```sh
cd app
pnpm build
```

The build validates accepted content, runs the automated tests, checks TypeScript, and produces the static PWA in `app/dist/`.

## Deploy on Vercel

Import this repository into Vercel and set **Root Directory** to `app`, **Framework** to Vite, and **Node.js** to 24. The checked-in Vercel configuration sets the build, output directory, and content cache headers. Use one stable production URL so browser progress remains available across deployments.

A push to a repository connected to Vercel may trigger deployment. Use a branch/preview deployment before promoting to production.

## Content and review

- [Publishing, preview, and rollback](app/CONTENT_PUBLISHING.md)
- [Question creation and calibration process](QUESTION_BANK_CREATION_PROCESS.md)
- [Import and acceptance process](app/content/QUESTION_IMPORT_PROCESS.md)
- [Current Phase IV status](app/PHASE_IV_STATUS.md)
- [Question bank index and section counts](app/content/QUESTION_BANK_INDEX.md)
- [Next-version upload instructions](GITHUB_UPLOAD.md)
- [Release notes](RELEASE_NOTES.md)
- [Additional-bank approval](app/content/review/additional-v3/decisions.json)

Accepted bank releases are under `app/public/content/`. Drafts and acceptance evidence are under `app/content/` and are never automatically selected for practice. Older sessions keep their original question snapshots.

Physical iPad Safari and deployment-to-browser verification remain manual acceptance checks. Keep student progress backups private; they are excluded from this repository.
