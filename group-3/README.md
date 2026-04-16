# Farkle - Group 3

A playable web-based Farkle game. First to **2,000** points wins - bank your
score or push your luck.

![Farkle game screenshot](screenshot.png)

## Features

- 6 dice, standard push / bank / bust mechanics, hot-dice on all-six-scored.
- Clickable pip-style dice with orange selection glow.
- Animated rolls: dice tumble for ~700ms before settling on the server result.
- Simple AI opponent that picks the highest-scoring combo per roll.
- Per-player turn history with per-hold breakdown rendered as mini pip-dice
  (kept dice highlighted, unkept dimmed, bust holds red) so you can see
  exactly what scored.
- Sticky scoring reference sidebar.

## Run it

```bash
cd group-3
pip install -r requirements.txt
uvicorn app:app --reload
# open http://localhost:8000/
```

Run the scoring unit tests:

```bash
cd group-3
python3 -m unittest test_scoring.py
```

## Files

| File | Purpose |
|---|---|
| `app.py` | FastAPI app: JSON endpoints + serves the SPA. |
| `game.py` | `FarkleGame` state machine (turn flow, history, AI). |
| `scoring.py` | Pure scoring functions (singles, of-a-kind, straight, pair). |
| `test_scoring.py` | Unit tests for the scoring engine. |
| `ui.py` | Original terminal UI (kept for reference / CI). |
| `static/index.html` | Entire frontend in one file (HTML + CSS + JS, no build). |
| `requirements.txt` | `fastapi`, `uvicorn`, `pydantic`. |
| `PROMPTS.md` | The ten prompts that produced this code and the pitfalls hit along the way. |

## Architecture

- **Pure scoring** - `scoring.py` is stateless functions so the rules can be
  unit-tested in isolation.
- **State machine** - `game.py` owns all mutable game state; the API layer
  doesn't touch internals directly except via methods like `record_hold`,
  `bank`, `check_bust`.
- **Thin API** - `app.py` is a small FastAPI layer with one module-level
  `FarkleGame` instance. Endpoints return the full game state so the
  frontend can render without extra round-trips.
- **Frontend in one file** - `static/index.html` has no build step; it uses
  the JSON API via `fetch()` and `Promise.all`s the roll animation with
  the server call so the UI never blocks.

See `PROMPTS.md` for the story of how each feature was prompted into
existence and what went wrong along the way.
