# HSPT Practice

An iPad-first, paper-style Quantitative Skills practice app. Includes 100 original, mathematically checked questions with a human-reviewed sample, diagrams, grading, explanations, and tips.

Phase II adds versioned question-bank delivery, browser-local progress, backup/restore, repeat cooldowns, and an owner-controlled content publishing workflow. Student practice data stays in the browser; no account or backend is required.

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

GitHub contains the source and published bank; pushing to GitHub alone does not create a live website.

## Content and review

- [Publishing, preview, and rollback](app/CONTENT_PUBLISHING.md)
- [Question creation and calibration process](QUESTION_BANK_CREATION_PROCESS.md)
- [Import and acceptance process](app/content/QUESTION_IMPORT_PROCESS.md)
- [Phase II status and remaining manual checks](app/PHASE_II_STATUS.md)
- [Twenty-question review packet](app/content/review/gables-v2/REVIEW_20.md)

Accepted bank releases are under `app/public/content/`. Drafts and acceptance evidence are under `app/content/` and are never automatically selected for practice. Older sessions keep their original question snapshots.

Physical iPad Safari and deployment-to-browser verification remain manual acceptance checks. Keep student progress backups private; they are excluded from this repository.
