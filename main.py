from fastapi import FastAPI
from app.routers.exercicio_router import router as exercicio_router


app = FastAPI()


app.include_router(exercicio_router)


@app.get("/")
def padrao():
    return {"msg": "Bem-vindo à API de Exercícios"}
