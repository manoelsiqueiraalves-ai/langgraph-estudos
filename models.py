from pydantic import BaseModel
from typing import Optional


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int