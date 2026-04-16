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
| `PROMPTS.md` | The raw prompts that produced this code and the pitfalls hit along the way. |

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

---

# Prompts Used

Below are the raw prompts from the Cursor Agent session that produced this
app, in order. Each section is one user message, quoted verbatim, followed
by a short note on what was produced in response. Reading top to bottom
reconstructs how the app grew from a terminal game to the interactive web
UI in this folder.

---

## 1. Initial build (terminal game + decoupled architecture)

> ### Git Workflow & Safety Constraints
> 0. **Target Repository:** `None` (Ensure you are working in the correct local clone of this repository).
> 1. Check out the latest `main` branch and pull the latest changes.
> 2. Create and switch to a new branch named `FIELDENG-1264`.
> 3. Implement the requested changes and commit them locally.
> 4. **CRITICAL:** Do NOT push the branch to the remote repository. Stop after committing locally.
> 5. Provide a concise summary of the work completed.
>
> ### Context
> We need to build a playable version of the dice game Farkle in Python. The game uses 6 dice. The goal is to be the first to reach 2,000 points. On a turn, a player rolls dice, sets aside scoring dice to accumulate points, and can either "bank" those points or "push their luck" by rolling the remaining dice. If a roll yields no scoring dice, they "bust" and lose all unbanked points for that turn.
>
> ### Original Strict Requirements
> 1. Implement the core game logic for Farkle in Python.
> 2. Build a text-based, terminal UI for the game.
> 3. The winning score threshold must be exactly 2,000 points.
> 4. You must implement the standard Farkle push/bank/bust mechanics.
> 5. Fetch and read the specific scoring rules from `https://github.com/nickmccollum/hackathon1/` before implementing the scoring logic.
>
> ### AI Recommended Enhancements
> 1. **Decoupled Architecture:** Keep the core game logic, scoring engine, and terminal UI completely separate. We may need to swap the terminal UI for a Python GUI or web interface later.
> 2. **ASCII Dice:** Implement a simple ASCII art display for the dice in the terminal to improve the user experience.
>
> ### Instructions for IDE LLM
> 1. Use the WebFetch or Shell tool to read the README/rules from `https://github.com/nickmccollum/hackathon1/` to get the exact scoring combinations.
> 2. Create the core scoring logic and write a few basic unit tests to verify it works.
> 3. Implement the game state manager and the terminal UI loop.
> 4. Follow the Git Workflow constraints strictly.

**Delivered:** `scoring.py` (pure functions), `game.py` (state machine
with AI opponent, hot dice, bust handling), `ui.py` (terminal loop with
ASCII dice), `test_scoring.py` (unit tests covering singles, 3/4/5/6 of
a kind, three-pair, straight, bust). The decoupling request is what
made every later UI swap cheap.

---

## 2. Move off the terminal

> Let's tranfser to a FastUI and React backend with an ability to select the dice

**Delivered:** first web version using FastAPI + FastUI. Dice became
clickable via a FastUI form.

---

## 3. Scoring reference page

> A scoring reference is also needed on a page

**Delivered:** `/rules` page with the full scoring table.

---

## 4. Match a specific aesthetic

An image was attached (deep-navy/violet background, red "FARKLE" title,
outlined score cards with an active-player glow, pip-style dice, inline
scoring card).

> I want to match this aesthetic with selectable dice

**Delivered:** FastUI scrapped. Replaced with a hand-written
single-page frontend (`static/index.html`) served by FastAPI, plus a
JSON API (`/api/state`, `/api/roll`, `/api/keep`, `/api/bank`,
`/api/ai_step`, `/api/reset`). Dice are tracked by index so duplicate
faces stay independently selectable.

---

## 5. Turn history

> Would it add value to show turn history on the left for player and right for AI?

Offered two layouts: outer sidebars vs inline under each score card.

> 2

**Delivered:** compact scrollable turn lists under each score card.
Green left-border for banked turns, red for busts, numbered per turn.

---

## 6. Scoring reference as a sidebar

> How one should/could score should be a sidebar

**Delivered:** inline scoring card moved to a sticky right-hand
sidebar, split into Singles / Three of a Kind / Sets / Rules sections.
Collapses on narrow viewports.

---

## 7. Richer turn history

> Turn history needs to convey details on how scoring occurred from either opponent, it's better to understand how one is losing or winning compared to their opponent

**Delivered:** every turn entry expanded to show the per-hold
breakdown (the roll, the dice kept, points earned). `game.py` now
records a `holds` list on every bank / bust event, including the AI's.

---

## 8. Graphical dice in history

> +1 idea: For turn history, can you show the dice graphically like how we select dice for the playing

**Delivered:** text roll listings replaced with mini pip-dice matching
the playing dice style. Kept dice glow orange, unkept are dimmed, bust
holds get a red border and a `BUST` tag.

---

## 9. Push-your-luck bug

> "Push your luck - roll the remaining dice, hoping to score more."
>
> We have an issue in which we should be able to re-roll the unselected die

**Delivered:** `/api/keep` was leaving unselected dice in
`current_roll`, which made the Roll button stay disabled. Fix: clear
`current_roll` on keep, rely on `dice_count` alone. Roll button label
became contextual (`Roll Dice` / `Roll N Remaining` /
`Hot Dice! Roll All 6`). Added hot-dice toast.

---

## 10. Animated roll

> Roll dice should be graphically animated (at most a second, but change random pips until final result)

**Delivered:** dice tumble (random faces every 80ms via a wobble
keyframe) for ~700ms before settling on the server-returned roll. The
animation and the `fetch()` run concurrently (`Promise.all`), so the
visual roll plays regardless of server latency. Buttons disable during
the animation; a `rollAnimating` flag keeps `render()` from stomping
the animation frames.

---

## Pitfalls encountered

Things that weren't obvious up front and cost an iteration or two:

- **FastUI was the wrong choice for a custom aesthetic.** The first
  web migration (prompt #2) used FastUI. It works for generic admin
  UIs, but once the target became a specific dark-purple, pixel-precise
  theme (prompt #4), FastUI was scrapped in favor of plain
  HTML / CSS / JS served as a static file from FastAPI.

- **`uvicorn farkle.app:app` broke with `ModuleNotFoundError`.**
  Running the app as a package changed `game` and `scoring` from
  top-level modules into package-relative ones, requiring
  `from .game import ...` and an `__init__.py`. Moving into the flat
  `group-3/` folder for the PR reversed the switch - `group-3` has a
  hyphen and can't be a Python package name, so the imports went back
  to absolute.

- **Selecting dice by face value doesn't work when faces repeat.** A
  roll of `1, 1, 1, 5, 5, 5` has six distinct selectable dice, not
  two. Early code passed `kept_faces` (a list of face values) to the
  keep endpoint, which is ambiguous. Fixed by sending **indices** from
  the frontend and resolving them to faces server-side.

- **Recording "how much was lost on a bust" has a sequencing trap.**
  `check_bust()` resets `turn_score` to `0` and calls `next_turn()`.
  Adding history required capturing the soon-to-be-lost `turn_score`
  **before** the reset, not after.

- **Push-your-luck was silently blocked.** After a keep, the backend
  kept the unselected dice in `current_roll`, which made the frontend
  disable the Roll button (`roll.length > 0`). Fix: clear
  `current_roll` on keep and rely on `dice_count` alone.

- **Animation races with `render()`.** While dice are tumbling, the AI
  turn completion or a parallel `render()` call could overwrite the
  animation frames. A single `rollAnimating` flag that makes
  `render()` a no-op during animation solved it.

- **AI history needed the same hold-recording as the player path.** The
  AI turn mutates state directly inside `game.py`, not through the
  `/api/keep` endpoint. Without explicitly calling `record_hold()` in
  `ai_turn()`, the AI's history entries had no detail - just the final
  bank/bust total.

---

## Architectural principles that emerged

- **Clean separation**: `scoring.py` is pure functions; `game.py` is
  state; `app.py` is a thin FastAPI layer; `static/index.html` is the
  entire frontend (HTML + CSS + JS in one file, no build step).
- **Selection by index, not face value**: duplicate faces (two 5s) need
  to be independently selectable, so the API keeps state as ordered
  lists and accepts indices.
- **The API carries enough for a rich UI**: every state response
  includes the turn history with per-hold breakdowns (roll snapshot,
  kept dice, points), so the frontend renders narratives without extra
  round-trips.
- **Animations overlap server calls**: `Promise.all([animate, fetch])`
  keeps the UI feeling responsive.
