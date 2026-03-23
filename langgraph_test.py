from langgraph.graph import StateGraph

# Estado
class State(dict):
    pass

# Node 1
def entender_pergunta(state):
    pergunta = state.get("pergunta", "").lower()

    if "curso" in pergunta:
        return {"intencao": "cursos"}
    elif "calculo" in pergunta or "somar" in pergunta:
        return {"intencao": "calculo"}
    else:
        return {"intencao": "desconhecido"}


# Node 2
def responder(state):
    intencao = state.get("intencao", "desconhecido")

    if intencao == "cursos":
        return {"resposta": "Aqui estão os cursos disponíveis"}
    elif intencao == "calculo":
        return {"resposta": "Use a calculadora"}
    else:
        return {"resposta": "Não entendi"}


# Grafo
builder = StateGraph(dict)

builder.add_node("entender", entender_pergunta)
builder.add_node("responder", responder)

builder.set_entry_point("entender")
builder.add_edge("entender", "responder")

graph = builder.compile()

# Execução
for step in graph.stream({"pergunta": "quais cursos você tem"}):
    print(step)
