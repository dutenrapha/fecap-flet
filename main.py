from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tarefa(BaseModel):
    título: str
    concluída: bool

tarefas = []

@app.get("/tarefas", response_model=List[Tarefa])
def ler_tarefas():
    return tarefas

@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa):
    tarefas.append(tarefa)
    return tarefa

@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def ler_tarefa(tarefa_id: int):
    return tarefas[tarefa_id]

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa):
    tarefas[tarefa_id] = tarefa
    return tarefa

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    del tarefas[tarefa_id]
    return {"detalhe": "Tarefa excluída."}
