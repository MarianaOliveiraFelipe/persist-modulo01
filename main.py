from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from app.models.exercicio import Exercicio  # Modelo baseado em Pydantic
import csv

app = FastAPI()

# Nome do arquivo CSV para armazenar os dados
exercicios_file = "exercicios.csv"

# Função para carregar os exercícios do arquivo CSV
def carregar_exercicios() -> list[Exercicio]:
    exercicios = []
    try:
        with open(exercicios_file, mode="r", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Criar instância do modelo Pydantic
                exercicio = Exercicio.parse_obj({
                    "id": int(row['id']),
                    "nome": row['nome'],
                    "grupo_muscular": row['grupo_muscular'],
                    "dificuldade": row['dificuldade'],
                    "series": int(row['series']),
                    "repeticoes": int(row['repeticoes']),
                    "descricao": row['descricao']
                })
                exercicios.append(exercicio)
    except FileNotFoundError:
        pass
    return exercicios

# Função para salvar os exercícios no arquivo CSV
def salvar_exercicios(exercicios: list[Exercicio]):
    with open(exercicios_file, mode="w", newline='', encoding="utf-8") as f:
        fieldnames = ['id', 'nome', 'grupo_muscular', 'dificuldade', 'series', 'repeticoes', 'descricao']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for exercicio in exercicios:
            writer.writerow(exercicio.dict())  # Utilizando o método embutido do Pydantic

# Carregar os exercícios existentes ao iniciar a API
exercicios = carregar_exercicios()

@app.get("/")
def padrao():
    return {"msg": "Bem-vindo à API de Exercícios"}

@app.get("/exercicios/{exercicio_id}")
def ler_exercicio(exercicio_id: int) -> Exercicio:
    for exercicio in exercicios:
        if exercicio.id == exercicio_id:
            return exercicio
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")

@app.get("/exercicios/")
def listar_exercicios() -> list[Exercicio]:
    return exercicios

@app.post("/exercicios/", status_code=HTTPStatus.CREATED)
def adicionar_exercicio(exercicio: Exercicio) -> Exercicio:
    if any(e.id == exercicio.id for e in exercicios):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID já existe.")
    exercicios.append(exercicio)
    salvar_exercicios(exercicios)
    return exercicio

@app.put("/exercicios/{exercicio_id}")
def atualizar_exercicio(exercicio_id: int, exercicio_atualizado: Exercicio) -> Exercicio:
    for indice, exercicio in enumerate(exercicios):
        if exercicio.id == exercicio_id:
            exercicio_atualizado.id = exercicio_id
            exercicios[indice] = exercicio_atualizado
            salvar_exercicios(exercicios)
            return exercicio_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")

@app.delete("/exercicios/{exercicio_id}")
def remover_exercicio(exercicio_id: int):
    for exercicio in exercicios:
        if exercicio.id == exercicio_id:
            exercicios.remove(exercicio)
            salvar_exercicios(exercicios)
            return {"msg": "Exercício removido com sucesso."}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")
