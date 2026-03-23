from fastapi import FastAPI, HTTPException, status, Path, Header, Depends
from app.models import Curso
from time import sleep
from typing import Any, Optional, List

app = FastAPI(
    title='API de Cursos da Geek University',
    version='0.0.1',
    description='A Python API for Cursos do Manoel',
)


def fake_db():
    try:
        print("Abrindo conexão com banco de dados")
        sleep(1)
    finally:
        print("Conectado com banco de dados")
        sleep(1)


cursos = {
    1: {
        "titulo": "Programação para Leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritmos e Lógica de Programação",
        "aulas": 87,
        "horas": 67
    }
}


@app.get(
    "/cursos",
    description="Retorna todos os cursos ou uma lista vazia",
    summary="Retorna todos os cursos ou uma lista vazia",
    response_model=List[Curso],
    response_description="Cursos retornados",
)
def get_cursos(db: Any = Depends(fake_db)):
    return [
        {"id": id_, **curso}
        for id_, curso in cursos.items()
    ]


@app.get("/cursos/{curso_id}")
def get_curso(
    curso_id: int = Path(
        ...,
        title="ID do curso",
        description="Deve ser entre 1 e 5",
        gt=0,
        lt=5
    ),
    db: Any = Depends(fake_db)
):
    curso = cursos.get(curso_id)

    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    return {"id": curso_id, **curso}


@app.post(
    "/cursos",
    description="Adiciona um curso novo",
    summary="Novidade"
)
def post_curso(curso: Curso, db: Any = Depends(fake_db)):

    next_id = len(cursos) + 1

    cursos[next_id] = {
        "titulo": curso.titulo,
        "aulas": curso.aulas,
        "horas": curso.horas
    }

    return {
        "id": next_id,
        **cursos[next_id]
    }


@app.put(
    "/cursos/{curso_id}",
    description="Altera um curso existente",
    summary="Alteração"
)
def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):

    if curso_id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com o id {curso_id}"
        )

    cursos[curso_id] = {
        "titulo": curso.titulo,
        "aulas": curso.aulas,
        "horas": curso.horas
    }

    return {
        "id": curso_id,
        **cursos[curso_id]
    }


@app.delete(
    "/cursos/{curso_id}",
    description="Deleta um curso",
    summary="Delete"
)
def delete_curso(curso_id: int, db: Any = Depends(fake_db)):

    if curso_id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    del cursos[curso_id]

    return {"message": "Curso removido com sucesso"}


@app.get("/calculadora")
async def calculadora(
    a: int,
    b: int,
    x_geek: str = Header(default=None),
    c: Optional[int] = None
):
    soma = a + b

    if c is not None:
        soma += c

    print(f"X-GEEK: {x_geek}")

    return {"resultado": soma}


@app.get("/agente")
def agente(pergunta: str):
    pergunta = pergunta.lower()

    if "curso" in pergunta:
        lista_cursos = [
            curso["titulo"] for curso in cursos.values()
        ]
        return {
            "resposta": "Aqui estão alguns cursos disponíveis:",
            "cursos": lista_cursos
        }

    elif "calculo" in pergunta or "somar" in pergunta:
        return {
            "resposta": "Você quer fazer um cálculo. Use o endpoint /calculadora."
        }

    else:
        return {
            "resposta": "Não entendi sua pergunta, mas estou aprendendo!"
        }