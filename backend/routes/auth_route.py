from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.auth_schema import LoginRequest, TokenResponse
from services.auth_service import AuthService
from database.connection import get_db


class AuthRouter:
    """
    Classe responsável por gerenciar a rota de autenticação (login).
    """

    def __init__(self, auth_service: AuthService):
        self.router = APIRouter(prefix="/auth", tags=["Autenticação"])
        self.auth_service = auth_service
        self._add_routes()

    def _add_routes(self):
        """
        Registra as rotas de autenticação no router interno.
        """
        @self.router.post("/login", response_model=TokenResponse)
        def login(
            login_data: LoginRequest,
            db: Session = Depends(get_db)
        ):
            """
            Rota responsável por autenticar o usuário e gerar o token JWT.

            Args:
                login_data (LoginRequest): Dados de login enviados pelo cliente.
                db (Session): Sessão de banco de dados injetada.

            Returns:
                TokenResponse: Token JWT válido e tipo do token (Bearer).
            """
            user = self.auth_service.authenticate_user(
                db, login_data.username, login_data.password
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas"
                )

            token = self.auth_service.create_access_token({"sub": user.username})
            return TokenResponse(access_token=token, token_type="bearer")
