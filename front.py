"front"
from fastapi import FastAPI
from random import choice

app = FastAPI()

# Lista de palavras para o jogo de forca
palavras = ["banana", "laranja", "morango", "abacaxi", "uva"]

# Escolhe uma palavra aleatória para o jogo de forca
def escolher_palavra():
    return choice(palavras)

# Rota para obter uma nova palavra para o jogo de forca
@app.get("/palavra")
def obter_palavra():
    palavra = escolher_palavra()
    return {"palavra": palavra}