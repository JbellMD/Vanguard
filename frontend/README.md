# Vanguard Frontend Dashboard

Minimal Next.js 14 (App Router) dashboard for the Vanguard AI Eval Platform.

## Getting started

From the `frontend/` directory:

```bash
npm install
npm run dev
```

The app will start at:

- http://localhost:3000

Backend assumptions:

- Backend API base URL is currently hard-coded in `lib/api.ts` as:
  - `http://localhost:8000`
- Endpoints used:
  - `GET /v1/evals/runs` – list runs
  - `GET /v1/evals/runs/{run_id}` – run details

## Pages

- `/` – Landing page with a link to **View Evaluation Runs**.
- `/runs` – Table of evaluation runs.
- `/runs/[id]` – Summary and per-test results for a specific run.

The UI is styled with TailwindCSS using simple cards, tables, and badges.
