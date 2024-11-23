import csv
from app.models.exercicio import Exercicio


exercicios_file = "exercicios.csv"


def carregar_exercicios() -> list[Exercicio]:
    exercicios = []
    try:
        with open(exercicios_file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Criar instância do modelo Pydantic
                exercicio = Exercicio.parse_obj(
                    {
                        "id": int(row["id"]),
                        "nome": row["nome"],
                        "grupo_muscular": row["grupo_muscular"],
                        "dificuldade": row["dificuldade"],
                        "series": int(row["series"]),
                        "repeticoes": int(row["repeticoes"]),
                        "descricao": row["descricao"],
                    }
                )
                exercicios.append(exercicio)
    except FileNotFoundError:
        pass
    return exercicios
