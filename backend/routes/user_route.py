from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import create_user, get_user_by_username

router = APIRouter(prefix="/users", tags=["Usuários"])

def get_db():
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
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para cadastrar um novo usuário no sistema.

    Args:
        user (UserCreate): Dados do usuário a ser criado.
        db (Session, optional): Sessão do banco injetada via Depends. Defaults to Depends(get_db).

    Raises:
        HTTPException: 400 caso o nome de usuário já exista.

    Returns:
        UserResponse: Dados do usuário criado (sem senha).
    """
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    new_user = create_user(db, user)
    return new_user
