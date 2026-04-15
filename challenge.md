# The Challenge: Build Farkle in Cursor


## Your Mission

Using **Cursor**, build a playable text-based version of **Farkle** that runs in a terminal window.

You have the rules (see `farkle-rules.md`). You have Cursor. Your team has the next **~60 minutes**.

At the end of the session, you will **demo your game live** to the group.


## Tools

- **Cursor** — use it as much as possible. That's the whole point.
- Any programming language you're comfortable with. Python is a safe default.
- Your terminal / console to run the game.
- The internet for documentation lookups (but not for copy-pasting a pre-built Farkle implementation).


## Required Features (Minimum Viable Game)

Your game must include all of the following to qualify for the demo:

**1. Dice Rolling**
- Roll 6 six-sided dice at the start of each turn
- Display the result clearly in the terminal (e.g., `Roll: [3, 1, 5, 5, 2, 4]`)

**2. Die Selection**
- The player can choose which dice to keep (set aside) after each roll
- Kept dice must include at least one scoring combination
- Warn the player if they try to keep a non-scoring combination

**3. Scoring**
- Correctly calculate points from kept dice using the Farkle scoring table
- Display a running turn total and the player's cumulative score after each roll

**4. Turn Flow**
- After keeping dice, the player chooses to **bank** (end their turn) or **roll again** with remaining dice
- Handle **bust** correctly: if no dice score on a roll, the player loses all turn points and their turn ends
- Handle the **all-six** case correctly: if all 6 dice score without busting, the player may pick up all 6
  and roll again, carrying accumulated turn points — but still risks busting on the next roll

**5. Win Condition**
- First player to reach **2,000 points** wins

**6. Two-Player Support**
- Implement at minimum a simple **AI opponent** that takes its turn after the human player
- The AI does not need to be smart — it just needs to be functional (e.g., always banks after one roll,
  or always rolls until it busts or hits a threshold)
- Bonus: support a second human player with alternating turns


## Stretch Goals

Got the basics working with time to spare? Consider adding:

- A smarter AI that uses basic strategy (e.g., always rolls if score is below X)
- Color output using ANSI codes (green for scores, red for bust)
- A scoreboard that displays both players' running totals each turn
- Score history or turn log
- Named players with a game start prompt
- Multiple rounds with best-of-N tracking
- A "spectator mode" that shows what choices the AI is considering


## Judging

After demos, if time allows, each participant ranks their **top 3** teams (ranked-choice voting — you
cannot vote for your own). Facilitators verify each game runs correctly before voting opens. Results
announced in the main room.


## Tips for Using Cursor

If you haven't used Cursor before, here's the short version:

**Agent Mode (the big one)** — Press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac). Describe what you want to
build in plain English. Cursor will generate files, write code, and make changes across your project. This is
your primary tool today.

**Inline Edit** — Highlight a block of code and press `Ctrl+K` / `Cmd+K` to ask Cursor to modify just that
section. Good for fixing bugs or tweaking a specific function.

**Tab Completion** — Cursor predicts what you're about to type. Press Tab to accept. Works mid-sentence in code.

**Starting point suggestion:**

> "Create a Python script for a text-based Farkle dice game. The game uses 6 six-sided dice.
> Players take turns rolling, selecting scoring dice to keep, and choosing to bank their points or roll
> the remaining dice again. If no dice score on a roll, the player busts and loses all turn points.
> If all 6 dice score without busting, the player picks up all 6 and may roll again (still risking a bust).
> Include a simple AI opponent. First player to reach 2,000 points wins.
> Show all game state clearly in the terminal."

Adjust, iterate, and build from there.
