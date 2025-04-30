from fastapi import FastAPI
from routes.user_route import router as user_router
from routes.auth_route import AuthRouter
from routes.secure_route import router as secure_router
from services.auth_service import AuthService
from database.connection import Base, engine


# Inicializa o FastAPI
app = FastAPI(
    title="CME System API",
    description="API para gerenciamento de Central de Materiais e Esterilização (CME).",
    version="1.0.0"
)

# Cria as tabelas no banco de dados ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

# Instancia os serviços e rotas
auth_service = AuthService(secret_key="super-secret-key")
auth_router = AuthRouter(auth_service=auth_service)

# Registro das rotas
app.include_router(user_router)
app.include_router(auth_router.router)
app.include_router(secure_router)


@app.get("/", tags=["Status"])
def root():
    """
    Endpoint raiz apenas para verificar se o servidor está ativo.

    Returns:
        dict: Mensagem de status.
    """
    return {"message": "CME System API is running 🚀"}
