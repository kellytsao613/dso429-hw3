"""
DSO 429 Homework 3 - Hourly Quiz answer bot.

Each run:
  1. Downloads questions.csv from the course repo.
  2. Finds every round that has no answers/round-NNNN.json yet.
  3. Sends each round's 25 questions to Google Gemini in one request.
  4. Double-checks the AI with the calculator in checks.py; if they disagree,
     the calculator wins (it is exact on every question type it knows).
  5. Writes answers/round-NNNN.json and a readable log in logs/.

GitHub Actions runs this on a schedule and pushes the results (see
.github/workflows/quiz.yml). Uses only the Python standard library.

Environment variables:
  GEMINI_API_KEY   Google AI Studio key (stored as a GitHub secret).
                   If missing, the bot still answers with the calculator alone.
  GEMINI_MODELS    Comma-separated model names to try in order.
  MAX_ROUNDS       Max rounds to answer per run (default 12, to stay inside
                   free-tier rate limits).
"""
import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from checks import check

QUESTIONS_URL = "https://raw.githubusercontent.com/FaisalXL/dso429-hourly-quiz/main/questions.csv"
KEYS_URL = "https://raw.githubusercontent.com/FaisalXL/dso429-hourly-quiz/main/practice_keys.csv"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODELS = "gemini-3.8-flash,gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-2.5-flash"

ROOT = Path(__file__).resolve().parent
ANSWERS = ROOT / "answers"
LOGS = ROOT / "logs"
LETTERS = ("A", "B", "C", "D")
FIRST_GRADED_ROUND = 49
RETRY_WINDOW_HOURS = 2.5  # rounds with guessed answers get re-tried within the 3-hour correction window


def log(msg):
    print(msg, flush=True)


def fetch_text(url, tries=4):
    for i in range(tries):
        try:
            # cache-buster: raw.githubusercontent.com caches for a few minutes
            with urllib.request.urlopen(f"{url}?t={int(time.time())}", timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            log(f"  fetch failed ({e}); retrying")
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"could not download {url}")


def load_rounds(text):
    rounds = defaultdict(list)
    for row in csv.DictReader(io.StringIO(text)):
        rounds[int(row["round_id"])].append(row)
    for rid in rounds:
        rounds[rid].sort(key=lambda r: int(r["q_index"]))
    return rounds


def answer_path(rid):
    return ANSWERS / f"round-{rid:04d}.json"


def load_status():
    p = LOGS / "status.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save_status(status):
    LOGS.mkdir(exist_ok=True)
    (LOGS / "status.json").write_text(json.dumps(status, indent=2, sort_keys=True))


def hours_since(released_at):
    try:
        t = datetime.fromisoformat(released_at.replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() / 3600
    except Exception:
        return 0.0


# ---------------------------------------------------------------- AI part

PROMPT = """You are answering a business arithmetic quiz. Each question has exactly one correct option.
For every question, do the calculation carefully step by step (keep full precision, round only at the end),
then pick the option letter that matches.

Return ONLY a JSON object, with one key per question ("q1", "q2", ...). Each value is an object:
  {{"work": "<short calculation, one line>", "answer": "<A, B, C or D>"}}

Questions:
{questions}
"""


def build_prompt(rows):
    lines = []
    for r in rows:
        lines.append(
            f"q{r['q_index']}. {r['question_text']}\n"
            f"   A) {r['option_a']}   B) {r['option_b']}   C) {r['option_c']}   D) {r['option_d']}"
        )
    return PROMPT.format(questions="\n".join(lines))


def call_gemini(prompt, api_key, models):
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }).encode()
    last_err = None
    for model in models:
        for attempt in range(3):
            req = urllib.request.Request(
                GEMINI_URL.format(model=model), data=body, method="POST",
                headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = json.loads(r.read())
                text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
                return model, text
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:300]
                last_err = f"{model}: HTTP {e.code} {detail}"
                log(f"  {last_err}")
                if e.code in (400, 401, 403, 404):
                    break  # bad key or model not available: try next model
                time.sleep(20 * (attempt + 1))  # 429 / 5xx: wait and retry
            except Exception as e:
                last_err = f"{model}: {e}"
                log(f"  {last_err}")
                time.sleep(10 * (attempt + 1))
    raise RuntimeError(last_err or "no model available")


def parse_ai(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    data = json.loads(text)
    out = {}
    for k, v in data.items():
        m = re.fullmatch(r"q?(\d+)", str(k).strip().lower())
        if not m:
            continue
        ans = v.get("answer") if isinstance(v, dict) else v
        work = v.get("work", "") if isinstance(v, dict) else ""
        ans = str(ans).strip().upper()[:1]
        if ans in LETTERS:
            out[int(m.group(1))] = (ans, work)
    return out


# ---------------------------------------------------------------- one round

def solve_round(rid, rows, api_key, models):
    ai, model, ai_error = {}, None, None
    if api_key:
        try:
            model, text = call_gemini(build_prompt(rows), api_key, models)
            ai = parse_ai(text)
        except Exception as e:
            ai_error = str(e)
    else:
        ai_error = "no GEMINI_API_KEY set"

    answers, report, guessed = {}, [], 0
    counts = defaultdict(int)
    for r in rows:
        qi = int(r["q_index"])
        opts = {L: r[f"option_{L.lower()}"] for L in LETTERS}
        calc = check(r["question_text"], opts)
        ai_ans, work = ai.get(qi, (None, ""))
        if ai_ans and calc and ai_ans != calc:
            final, src = calc, "calculator (overrode AI)"
        elif ai_ans:
            final, src = ai_ans, "AI" + (" + calculator agree" if calc else "")
        elif calc:
            final, src = calc, "calculator (no AI answer)"
        else:
            final, src = "A", "GUESS (no AI or calculator answer)"
            guessed += 1
        counts[src] += 1
        answers[f"q{qi}"] = final
        report.append(f"| q{qi} | {r['question_text']} | {ai_ans or '-'} | {calc or '-'} | **{final}** | {src} | {work} |")
    return answers, report, dict(counts), model, ai_error, guessed


def write_round(rid, rows, answers, report, counts, model, ai_error):
    ANSWERS.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    ordered = {f"q{i}": answers[f"q{i}"] for i in range(1, len(rows) + 1)}
    answer_path(rid).write_text(json.dumps({"round_id": rid, "answers": ordered}, indent=2) + "\n")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Round {rid}",
        f"Released {rows[0]['released_at']} - answered {now} - model: {model or 'none'}",
        "",
        "Sources: " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())),
    ]
    if ai_error:
        lines.append(f"\nAI problem: {ai_error}")
    lines += ["", "| # | Question | AI | Calculator | Final | Source | AI work |", "|---|---|---|---|---|---|---|"]
    lines += report
    (LOGS / f"round-{rid:04d}.md").write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------- main

def main():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    models = [m.strip() for m in os.environ.get("GEMINI_MODELS", DEFAULT_MODELS).split(",") if m.strip()]
    max_rounds = int(os.environ.get("MAX_ROUNDS", "12"))

    rounds = load_rounds(fetch_text(QUESTIONS_URL))
    status = load_status()
    log(f"{len(rounds)} rounds published; AI {'on' if api_key else 'OFF (calculator only)'}")

    todo = []
    for rid, rows in rounds.items():
        if len(rows) != 25:
            log(f"round {rid}: only {len(rows)} questions so far, still answering what is there")
        if not answer_path(rid).exists():
            todo.append(rid)
        elif status.get(str(rid), {}).get("guessed", 0) and hours_since(rows[0]["released_at"]) < RETRY_WINDOW_HOURS:
            todo.append(rid)  # had guesses and there is still time to correct within 3 hours
    # Graded rounds first (oldest first, since the timing credit clock is running), then practice.
    todo.sort(key=lambda r: (r < FIRST_GRADED_ROUND, r))
    todo = todo[:max_rounds]
    if not todo:
        log("nothing new to answer")
        return

    for i, rid in enumerate(todo):
        rows = rounds[rid]
        answers, report, counts, model, ai_error, guessed = solve_round(rid, rows, api_key, models)
        write_round(rid, rows, answers, report, counts, model, ai_error)
        status[str(rid)] = {"guessed": guessed, "model": model, "ai_error": bool(ai_error), "sources": counts}
        save_status(status)
        log(f"round {rid}: done ({counts})" + (f" - AI problem: {ai_error}" if ai_error else ""))
        if api_key and i < len(todo) - 1:
            time.sleep(8)  # stay under free-tier requests-per-minute limits

    if os.environ.get("CHECK_PRACTICE"):
        practice_score()


def practice_score():
    """Compare answered practice rounds with the public keys (only rounds 1-48 have keys)."""
    keys = defaultdict(dict)
    for row in csv.DictReader(io.StringIO(fetch_text(KEYS_URL))):
        keys[int(row["round_id"])][f"q{row['q_index']}"] = row["answer"]
    right = total = 0
    for rid, key in keys.items():
        p = answer_path(rid)
        if p.exists():
            got = json.loads(p.read_text())["answers"]
            right += sum(got.get(q) == a for q, a in key.items())
            total += len(key)
    log(f"practice accuracy: {right}/{total}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"FAILED: {e}")
        sys.exit(1)
