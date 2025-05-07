from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate

class UserService:
    """
    Serviço para operações relacionadas ao usuário.
    """

    def __init__(self):
        # Define o contexto de criptografia usando bcrypt
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """
        Retorna a senha criptografada.
        """
        return self.pwd_context.hash(password)

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """
        Cria um novo usuário no banco com senha criptografada.
        """
        hashed_pw = self.hash_password(user_data.password)

        new_user = User(
            username=user_data.username,
            password=hashed_pw,
            role=user_data.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_user_by_username(self, db: Session, username: str) -> User | None:
        """
        Busca um usuário pelo nome de usuário.
        """
        return db.query(User).filter(User.username == username).first()
