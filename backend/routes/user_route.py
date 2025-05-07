from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService
from dependencies.jwt_bearer import JWTBearer


router = APIRouter(prefix="/users", tags=["Usuários"])

# Instância da classe de serviço
user_service = UserService()

# Middleware de autenticação JWT
jwt_bearer = JWTBearer(secret_key="super-secret-key")


def get_db():
    """
    Cria e gerencia uma sessão do banco de dados para cada requisição.

    Returns:
        Generator[Session, None, None]: Sessão do banco.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário com senha criptografada.

    Args:
        user (UserCreate): Dados recebidos para criação do usuário.
        db (Session): Sessão ativa do banco de dados.

    Raises:
        HTTPException: Se o nome de usuário já existir.

    Returns:
        UserResponse: Dados do usuário criado (sem senha).
    """
    if user_service.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe"
        )
    
    return user_service.create_user(db, user)


@router.get("/usuarios-protegidos", dependencies=[Depends(jwt_bearer)])
def usuarios_protegidos():
    """
    Rota protegida para testar autenticação via JWT.

    Returns:
        dict: Mensagem de sucesso.
    """
    return {"message": "Você acessou uma rota protegida com sucesso!"}
