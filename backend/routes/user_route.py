from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import create_user, get_user_by_username
from dependencies.jwt_bearer import JWTBearer


router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

# Middleware de proteção JWT
jwt_bearer = JWTBearer(secret_key="super-secret-key")

def get_db() -> Session:
    """
    Cria uma nova sessão com o banco de dados para cada requisição.

    Returns:
        Session: Sessão ativa do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Cadastra um novo usuário no sistema.

    Args:
        user (UserCreate): Dados enviados na requisição para criação do usuário.
        db (Session): Sessão do banco de dados injetada via FastAPI.

    Raises:
        HTTPException: Se o nome de usuário já estiver cadastrado.

    Returns:
        UserResponse: Dados do usuário criado (sem exibir a senha).
    """
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    new_user = create_user(db, user)
    return new_user


@router.get("/usuarios-protegidos", dependencies=[Depends(jwt_bearer)])
def usuarios_protegidos() -> dict:
    """
    Rota protegida por autenticação JWT.

    Returns:
        dict: Mensagem de confirmação de acesso autorizado.
    """
    return {"message": "Você acessou uma rota protegida com sucesso!"}
