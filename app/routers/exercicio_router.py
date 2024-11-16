from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.exercicio import Exercicio
from app.services.loading import carregar_exercicios
from app.services.manipulation import adicionar_exercicio, atualizar_exercicio, remover_exercicio
from app.services.convertion import csv_para_zip, csv_para_json, calcular_hash
from http import HTTPStatus

router = APIRouter()

# Get da lista de exercícios
@router.get("/exercicios/")
def listar_exercicios():
    exercicios = carregar_exercicios()
    return exercicios

# Get by ID
@router.get("/exercicios/{exercicio_id}")
def ler_exercicio(exercicio_id: int) -> Exercicio:
    exercicios = carregar_exercicios()
    for exercicio in exercicios:
        if exercicio.id == exercicio_id:
            return exercicio
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Exercício não encontrado.")

# Post de novo exercício
@router.post("/exercicios/", status_code=HTTPStatus.CREATED)
def criar_exercicio(exercicio: Exercicio):
    return adicionar_exercicio(exercicio)

# Atualizar exercício
@router.put("/exercicios/{exercicio_id}")
def atualizar_exercicio_endpoint(exercicio_id: int, exercicio_atualizado: Exercicio):
    return atualizar_exercicio(exercicio_id, exercicio_atualizado)

# Remover exercício
@router.delete("/exercicios/{exercicio_id}")
def remover_exercicio_endpoint(exercicio_id: int):
    return remover_exercicio(exercicio_id)

# Converter exercícios.csv para exercícios.json
@router.get("/exercicios/json/")
def converter_exercicios():
    try:
        json_filename = csv_para_json()
        return FileResponse(json_filename, media_type='application/json', filename=json_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter arquivo: {str(e)}")

# Compactar exercícios.csv
@router.get("/exercicios/compactar/")
def compactar_exercicios():
    try:
        zip_filename = csv_para_zip("exercicios.csv")
        return FileResponse(zip_filename, media_type='application/zip', filename=zip_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compactar arquivo: {str(e)}")
    
# Calcular hash de exercícios.csv
@router.get("/exercicios/hash/")
def get_csv_hash():
    try:
        csv_file = "exercicios.csv"
        hash_sha256 = calcular_hash(csv_file)
        return {"sha256_hash": hash_sha256}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))