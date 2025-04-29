from sqlalchemy.orm import Session
from models.user import User, RoleEnum
from schemas.user_schema import UserCreate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.

    Args:
        password (str): Senha em texto puro.

    Returns:
        str: Hash da senha.
    """
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.

    Args:
        db (Session): Sessão ativa do banco de dados.
        user (UserCreate): Dados do usuário a ser criado.

    Returns:
        User: Usuário criado no banco de dados.
    """
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Busca um usuário no banco de dados pelo username.

    Args:
        db (Session): Sessão ativa do banco de dados.
        username (str): Nome de usuário para buscar.

    Returns:
        User | None: Usuário encontrado ou None se não existir.
    """
    return db.query(User).filter(User.username == username).first()
