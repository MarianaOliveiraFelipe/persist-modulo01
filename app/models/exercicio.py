from pydantic import BaseModel


class Exercicio(BaseModel):
    id: int
    nome: str
    grupo_muscular: str
    dificuldade: str
    series: int
    repeticoes: int
    descricao: str
