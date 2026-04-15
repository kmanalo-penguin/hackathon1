# Farkle Hackathon — Lunch & Learn Challenge [AI]

Build a playable, text-based **Farkle** dice game that runs in a terminal.
Use **Cursor** as your primary tool — that is the whole point of this hackathon.

There is no starter code in this repo on purpose. Teams build from scratch using Cursor's Agent mode.


## Quick Start

```bash
git clone https://github.com/nickmccollum/hackathon1.git
cd hackathon1
git checkout -b group-N      # replace N with your assigned group number
```

Open the repo in **Cursor**, then use Agent mode (`Ctrl+I` / `Cmd+I`) to start building.


## The Challenge

Six dice. First player to **2,000 points** wins. Bank your score or push your luck — but if nothing
scores on a roll, you **bust** and lose everything from that turn.

Your game must include:

- **Dice rolling** — roll 6 six-sided dice; display results clearly
- **Die selection** — player chooses which dice to keep; must include a scoring combo
- **Scoring** — correct point calculation per the Farkle scoring table; show running totals
- **Turn flow** — bank or roll again; bust if nothing scores; handle the all-six pickup rule
- **Win condition** — first to 2,000 points
- **AI opponent** — at minimum a simple AI that takes functional turns after the human player

Full details in [`challenge.md`](challenge.md). Complete scoring table and rules in
[`farkle-rules.md`](farkle-rules.md).


## Suggested Starting Prompt

Paste this into Cursor Agent mode to scaffold your game:

> Create a Python script for a text-based Farkle dice game. 6 dice, players take turns rolling,
> selecting scoring dice to keep, choosing to bank or roll again. Bust = lose turn points.
> All 6 score = pick up all 6 and roll again. Simple AI opponent. First to 2,000 wins.
> Show all game state in the terminal.

Adjust, iterate, and build from there. Any language works — Python is a safe default.


## Branch Convention

Each team works on a branch named `group-` plus their assigned number:

| Group | Branch |
|-------|--------|
| 1 | `group-1` |
| 2 | `group-2` |
| 3 | `group-3` |
| ... | `group-N` |


## Collaboration

No mandated workflow. Teams can:

- Work directly on this GitHub repo (create your `group-N` branch and push)
- Mirror or import the repo into GitLab or another forge
- Fork the repo
- Copy the files and work from a completely different remote

Pick whatever lets everyone on your team contribute. The only requirement is that your work
is accessible for the demo — it should not exist only on one laptop.


## Repo Contents

| File | Purpose |
|------|---------|
| `README.md` | This file — quickstart and AI agent context |
| `farkle-rules.md` | Complete Farkle rules, scoring table, and examples |
| `challenge.md` | Required features, stretch goals, and Cursor tips |
| `.gitignore` | Standard Python ignores |
