from fastapi import FastAPI
from random import choice
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Lista de palavras para o jogo de forca
palavras = ["banana", "laranja", "morango", "abacaxi", "uva"]

# Modelo Pydantic para a resposta da palavra
class Palavra(BaseModel):
    palavra: str

# Escolhe uma palavra aleatória para o jogo de forca
def escolher_palavra():
    return choice(palavras)

# Rota para obter uma nova palavra para o jogo de forca
@app.get("/palavra", response_model=Palavra)
def obter_palavra():
    palavra = escolher_palavra()
    return {"palavra": palavra}

# Rota para servir o arquivo HTML do frontend
@app.get("/", response_class=HTMLResponse)
async def read_item():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)