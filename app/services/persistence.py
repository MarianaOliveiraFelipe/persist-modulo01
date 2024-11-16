import csv
from app.models.exercicio import Exercicio

exercicios_file = "exercicios.csv"

def salvar_exercicios(exercicios: list[Exercicio]):
    with open(exercicios_file, mode="w", newline='', encoding="utf-8") as f:
        fieldnames = ['id', 'nome', 'grupo_muscular', 'dificuldade', 'series', 'repeticoes', 'descricao']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if f.tell() == 0:
            writer.writeheader()

        for exercicio in exercicios:
            writer.writerow(exercicio.dict())