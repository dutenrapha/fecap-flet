from fastapi import FastAPI
from random import choice

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao jogo Cara ou Coroa!"}

@app.get("/jogar/{escolha}")
def jogar(escolha: str):
    resultado = choice(["cara", "coroa"])
    if escolha.lower() == resultado:
        return {"resultado": resultado, "mensagem": "Você ganhou!"}
    else:
        return {"resultado": resultado, "mensagem": "Você perdeu!"}
