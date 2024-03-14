# Matheus Antonio Simões Arromba
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Move(BaseModel):
    player: str
    position: int

class GameState(BaseModel):
    board: List[str]
    winner: str = None

game_state = GameState(board=[""] * 9)

def check_winner(board):
    # Linhas Horizontais
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != "":
            return board[i]

    # Linhas Verticais
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "":
            return board[i]

    # Linhas Diagonais
    if board[0] == board[4] == board[8] != "":
        return board[0]
    if board[2] == board[4] == board[6] != "":
        return board[2]

    # Empate
    if "" not in board:
        return "tie"

    return None

@app.post("/move/", response_model=GameState)
async def make_move(move: Move):
    if game_state.winner:
        raise HTTPException(status_code=400, detail="Game is already over")

    if move.player not in ["X", "O"]:
        raise HTTPException(status_code=400, detail="Invalid player")

    if move.position < 0 or move.position > 8 or game_state.board[move.position] != "":
        raise HTTPException(status_code=400, detail="Invalid move")

    game_state.board[move.position] = move.player
    game_state.winner = check_winner(game_state.board)

    return game_state
