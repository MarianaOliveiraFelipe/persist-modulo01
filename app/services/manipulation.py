from fastapi import HTTPException
from http import HTTPStatus
from app.models.exercicio import Exercicio
from app.services.persistence import salvar_exercicios
from app.services.loading import carregar_exercicios

exercicios = carregar_exercicios()

def adicionar_exercicio(exercicio: Exercicio) -> Exercicio:
    if any(e.id == exercicio.id for e in exercicios):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID já existe.")
    exercicios.append(exercicio)
    salvar_exercicios(exercicios)  # Chama salvar_exercicio ao invés de salvar_exercicios
    return exercicio

def atualizar_exercicio(exercicio_id: int, exercicio_atualizado: Exercicio) -> Exercicio:
    for indice, exercicio in enumerate(exercicios):
        if exercicio.id == exercicio_id:
            # Substituindo o exercício existente
            exercicios[indice] = exercicio_atualizado
            salvar_exercicios(exercicios)  # Salva as atualizações no arquivo CSV
            return exercicio_atualizado
    # Se o exercício com o ID não for encontrado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")

def remover_exercicio(exercicio_id: int):
    for exercicio in exercicios:
        if exercicio.id == exercicio_id:
            exercicios.remove(exercicio)
            salvar_exercicios(exercicios)
            return {"msg": "Exercício removido com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")