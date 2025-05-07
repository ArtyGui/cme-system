from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from models.user import User


class AuthService:
    """
    Serviço de autenticação e geração de token JWT.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expiration_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration_minutes = token_expiration_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha digitada confere com a senha criptografada.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, db, username: str, password: str) -> User:
        """
        Autentica o usuário. Retorna o usuário se válido, senão levanta erro 401.
        """
        from services.user_service import UserService
        user_service = UserService()
        user = user_service.get_user_by_username(db, username)

        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha inválidos"
            )
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """
        Gera um token de acesso JWT para o usuário autenticado.

        Args:
            data (dict): Dados a serem codificados no token (ex: {"sub": username}).
            expires_delta (timedelta, opcional): Tempo até o token expirar.

        Returns:
            str: Token JWT assinado.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.token_expiration_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
