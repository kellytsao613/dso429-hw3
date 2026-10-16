# DSO 429 Homework 3 — Hourly Quiz Bot

An automated pipeline that answers the hourly DSO 429 quiz and commits one
`answers/round-NNNN.json` file per round, around the clock, with no laptop needed.

## How it works

1. **Always on.** GitHub Actions (`.github/workflows/quiz.yml`) runs the bot on GitHub's servers.
   GitHub's built-in scheduler turned out to skip most runs, so the bot doesn't depend on it.
   Each run stays on for about 5.5 hours and checks for new rounds every 5 minutes, then starts
   the next run itself. An hourly scheduled run is kept only as a backup in case that chain breaks,
   and only one run can be active at a time.
2. **Fetch.** `solve.py` downloads the course's `questions.csv` and finds every round that
   doesn't have an answer file yet, not only the newest one. Graded rounds (49+) go first.
3. **AI answers.** Each round's 25 questions go to Google Gemini in a single request. The model
   works through each calculation and returns a JSON answer letter for every question.
4. **Calculator double-check.** `checks.py` recognizes the 12 question types from the practice
   rounds and computes them exactly. If the AI and the calculator disagree, the calculator wins.
   If the AI is down, the calculator answers on its own. A question type neither one can handle
   is guessed and retried on the next run while it's still inside the 3-hour correction window.
5. **Commit.** After each check, the workflow pushes any new answer files to `main`. If `main`
   changed in the meantime, it re-applies its answers on top of the latest version and merges
   `status.json` instead of failing.

Every round also gets a readable log in `logs/round-NNNN.md`. It shows each question, the AI's
answer and work, the calculator's answer, and which one was used.

## Results on the practice rounds

- The calculator matches the official key on all 1,200 practice questions.
- The full pipeline was tested with a simulated AI that was wrong about 7% of the time and
  sometimes returned broken output. It still scored 1,200 / 1,200.
- Running live on GitHub, the bot answered all 48 practice rounds and scored 1,200 / 1,200
  against the official key, with no AI errors and no guessed answers.

## Setup

1. Get a free Gemini API key at https://aistudio.google.com (click **Get API key**).
2. In this repo, go to **Settings → Secrets and variables → Actions → New repository secret**.
   Name it `GEMINI_API_KEY` and paste the key.
3. Go to **Actions → Answer quiz rounds → Run workflow** to start it once by hand. After that
   it keeps itself going.

To stop the bot, cancel the run that's in progress on the **Actions** tab. A cancelled run
doesn't start the next one. The hourly backup can still start a new run, so to stop it for good,
also click **...** → **Disable workflow** on the workflow's page.

## Files

| File | What it does |
|---|---|
| `solve.py` | Main bot: fetch, ask the AI, cross-check, write answers |
| `checks.py` | Calculator for the known question types |
| `.github/workflows/quiz.yml` | Keeps the bot running on GitHub and pushes its answers |
| `answers/` | Submitted answer files, one per round |
| `logs/` | Per-round logs and `status.json` |
