from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from game import FarkleGame
from scoring import calculate_score

app = FastAPI()

game = FarkleGame(target_score=2000)

INDEX_HTML = (Path(__file__).parent / "static" / "index.html").resolve()


def _state_payload() -> dict:
    return {
        "players": game.players,
        "scores": game.scores,
        "history": game.history,
        "current_player": game.current_player(),
        "turn_score": game.turn_score,
        "dice_count": game.dice_count,
        "current_roll": game.current_roll,
        "is_game_over": game.is_game_over,
        "winner": game.winner,
        "target_score": game.target_score,
    }


class KeepPayload(BaseModel):
    indices: list[int]


@app.get("/api/state")
def get_state() -> dict:
    return _state_payload()


@app.post("/api/roll")
def roll_dice() -> dict:
    if game.is_game_over:
        raise HTTPException(400, "Game is over.")
    if game.current_player() != "Player":
        raise HTTPException(400, "Not the player's turn.")
    game.roll_dice()
    busted = game.check_bust()
    state = _state_payload()
    state["busted"] = busted
    return state


@app.post("/api/keep")
def keep_dice(payload: KeepPayload) -> dict:
    if game.is_game_over:
        raise HTTPException(400, "Game is over.")
    if game.current_player() != "Player":
        raise HTTPException(400, "Not the player's turn.")

    indices = payload.indices
    if not indices:
        raise HTTPException(400, "No dice selected.")
    if len(set(indices)) != len(indices):
        raise HTTPException(400, "Duplicate indices.")
    if any(i < 0 or i >= len(game.current_roll) for i in indices):
        raise HTTPException(400, "Invalid index.")

    kept_faces = [game.current_roll[i] for i in indices]
    score, count = calculate_score(kept_faces)
    if score == 0 or count != len(kept_faces):
        raise HTTPException(400, "Selection is not a valid scoring combination.")

    roll_snapshot = list(game.current_roll)

    game.record_hold(roll_snapshot, kept_faces, score)
    game.turn_score += score
    game.dice_count -= len(kept_faces)
    hot_dice = False
    if game.dice_count == 0:
        game.dice_count = 6
        hot_dice = True
    game.current_roll = []

    state = _state_payload()
    state["gained"] = score
    state["hot_dice"] = hot_dice
    return state


@app.post("/api/bank")
def bank() -> dict:
    if game.is_game_over:
        raise HTTPException(400, "Game is over.")
    if game.current_player() != "Player":
        raise HTTPException(400, "Not the player's turn.")
    if game.turn_score <= 0:
        raise HTTPException(400, "Nothing to bank yet.")
    game.bank()
    return _state_payload()


@app.post("/api/ai_step")
def ai_step() -> dict:
    if game.is_game_over:
        raise HTTPException(400, "Game is over.")
    if game.current_player() != "AI":
        raise HTTPException(400, "Not the AI's turn.")
    action, roll, kept, turn_score = game.ai_turn()
    state = _state_payload()
    state["ai_action"] = action
    state["ai_roll"] = roll
    state["ai_kept"] = kept
    state["ai_turn_score"] = turn_score
    return state


@app.post("/api/reset")
def reset() -> dict:
    global game
    game = FarkleGame(target_score=2000)
    return _state_payload()


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML.read_text())
