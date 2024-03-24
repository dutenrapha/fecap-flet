from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class Pessoa(BaseModel):
    name: str

@app.get("/")
async def root():
    return {"message": "Hi I'm Gu!"}

@app.post("/hello")
async def say_hello(pessoa: Pessoa):
    return {"message": "Hello, " + pessoa.name + "! 👋"}

@app.post("/bye")
async def say_bye(pessoa: Pessoa):
    return {"message": "Bye, " + pessoa.name + "! 👋"}

