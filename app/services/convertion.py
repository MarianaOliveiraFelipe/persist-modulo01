from app.services.loading import carregar_exercicios
import json
import zipfile
import hashlib


exercicios_file = "exercicios.csv"


def csv_para_json() -> str:
    exercicios = carregar_exercicios()
    exercicios_dict = [exercicio.model_dump() for exercicio in exercicios]

    json_filename = "exercicios.json"
    try:
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(exercicios_dict, json_file, ensure_ascii=False, indent=4)
        return json_filename
    except Exception as e:
        raise Exception(f"Erro ao converter CSV para JSON: {str(e)}")


def csv_para_zip(csv_file: str) -> str:
    zip_filename = csv_file.replace(".csv", ".zip")
    try:
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_file, arcname=csv_file)
        return zip_filename
    except Exception as e:
        raise Exception(f"Erro ao compactar arquivo CSV: {str(e)}")


def calcular_hash(csv_file: str) -> str:
    try:
        with open(csv_file, "rb") as f:
            file_data = f.read()
            sha256_hash = hashlib.sha256(file_data).hexdigest()
        return sha256_hash
    except Exception as e:
        raise Exception(f"Erro ao calcular hash do arquivo: {str(e)}")
