# HSPT Practice

An iPad-first, paper-style practice app covering all five HSPT sections. Version **0.3.0** includes **500 original questions: 100 per section**, answer explanations, original diagrams, and shared Reading passages. Each bank has a human-reviewed 20-question sample; unsampled questions are not individually human-approved.

Phase III content is integrated into the existing practice experience. Five-minute bursts, 10-question section previews, and a 50-question five-section preview are available. Full-length section presets and the 298-question exam remain planned work; this version is not the completed Phase III exam simulator.

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
- [Current Phase III status](app/PHASE_III_PREVIEW.md)
- [Next-version upload instructions](GITHUB_UPLOAD.md)
- [Release notes](RELEASE_NOTES.md)
- [Additional-bank approval](app/content/review/additional-v3/decisions.json)

Accepted bank releases are under `app/public/content/`. Drafts and acceptance evidence are under `app/content/` and are never automatically selected for practice. Older sessions keep their original question snapshots.

Physical iPad Safari and deployment-to-browser verification remain manual acceptance checks. Keep student progress backups private; they are excluded from this repository.
