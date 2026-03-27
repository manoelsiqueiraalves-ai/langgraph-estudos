from fastapi import FastAPI
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage

app = FastAPI()

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`."""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`."""
    return a / b

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

@app.get("/teste")
async def teste(pergunta: str = "Quanto é 25 dividido por 5?"):
    messages = [HumanMessage(content=pergunta)]

    ai_msg = model_with_tools.invoke(messages)
    messages.append(ai_msg)

    # Se o modelo chamar alguma tool
    for tool_call in ai_msg.tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

    # Se ele não chamar tool, ainda assim devolve algo
    if not ai_msg.tool_calls:
        return {
            "pergunta": pergunta,
            "resposta_modelo": ai_msg.content,
            "tool_calls": [],
            "observacao": "O modelo respondeu sem usar ferramenta."
        }

    final_response = model_with_tools.invoke(messages)

    return {
        "pergunta": pergunta,
        "resposta_final": final_response.content,
        "tool_calls": ai_msg.tool_calls
    }
