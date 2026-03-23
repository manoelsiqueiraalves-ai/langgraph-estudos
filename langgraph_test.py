from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict
from langgraph.graph import StateGraph, END


app = FastAPI()


class PerguntaInput(BaseModel):
    pergunta: str


class AgentState(TypedDict, total=False):
    pergunta: str
    intencao: str
    resposta: str


def entender_pergunta(state: AgentState) -> AgentState:
    pergunta = state.get("pergunta", "").lower()

    if "curso" in pergunta or "cursos" in pergunta:
        return {"intencao": "cursos"}

    if "somar" in pergunta or "calculo" in pergunta or "conta" in pergunta:
        return {"intencao": "calculo"}

    return {"intencao": "desconhecido"}


def responder(state: AgentState) -> AgentState:
    intencao = state.get("intencao", "desconhecido")
    pergunta = state.get("pergunta", "")

    if intencao == "cursos":
        return {"resposta": "Temos cursos de Python, FastAPI e IA."}

    if intencao == "calculo":
        return {"resposta": f"Voce pediu um calculo. Ainda vou implementar isso. Pergunta: {pergunta}"}

    return {"resposta": "Nao entendi sua pergunta."}


builder = StateGraph(AgentState)
builder.add_node("entender_pergunta", entender_pergunta)
builder.add_node("responder", responder)
builder.set_entry_point("entender_pergunta")
builder.add_edge("entender_pergunta", "responder")
builder.add_edge("responder", END)

graph = builder.compile()


@app.post("/agente")
def executar_agente(dados: PerguntaInput):
    resultado = graph.invoke({"pergunta": dados.pergunta})
    return resultado
