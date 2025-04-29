from fastapi import FastAPI
from routes.user_route import router as user_router
from database.connection import Base, engine

app = FastAPI(
    title="CME System API",
    description="API para gerenciamento de Central de Materiais e Esterilização (CME).",
    version="1.0.0"
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Registro das rotas
app.include_router(user_router)

@app.get("/", tags=["Status"])
def root():
    """
    Endpoint raiz apenas para verificar se o servidor está ativo.

    Returns:
        dict: Mensagem de status.
    """
    return {"message": "CME System API is running 🚀"}
