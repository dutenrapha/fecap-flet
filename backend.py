from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import sleep
import random
import uvicorn

app = FastAPI()

class PlayRequest(BaseModel):
    text: str

opcoes = ("Pedra","Papel","Tesoura")

@app.post("/play")
async def get_play(play_request: PlayRequest):
    escolha_computador = random.choice(opcoes)  
    return {"play": escolha_computador}  