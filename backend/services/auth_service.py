from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User

class AuthService:
    """
    Serviço responsável por autenticação de usuários e geração de tokens JWT.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expire_minutes: int = 30):
        """
        Inicia o serviço com as configurações básicas de segurança

        Args:
            secret_key (str): Chave secreta usada para assinar o JWT.
            algorithm (str): Algoritmo de criptografia (default: HS256).
            token_expire_minutes (int): Tempo de expiração do token.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha fornecida bate com o hash armazenado
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, db: Session, username: str, password: str) -> User | None:
        """
        Valida credenciais e retorna o usuário autenticado ou None.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Gera o token JWT com tempo de expiração.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.token_expire_minutes))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token
