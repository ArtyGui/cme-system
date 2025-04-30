from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    Esquema de entrada para autenticação de usuários.

    Atributos:
        username (str): Nome de usuário cadastrado.
        password (str): Senha do usuário.
    """
    username: str = Field(..., example="artur")
    password: str = Field(..., example="senha123")


class TokenResponse(BaseModel):
    """
    Esquema de resposta com token de acesso JWT.

    Atributos:
        access_token (str): Token de acesso gerado pelo sistema.
        token_type (str): Tipo do token (ex: Bearer).
    """
    access_token: str = Field(..., example="eyJhbGciOi...")
    token_type: str = Field(default="bearer", example="bearer")
