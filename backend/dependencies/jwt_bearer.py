from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette.status import HTTP_403_FORBIDDEN


class JWTBearer(HTTPBearer):
    """
    Middleware que protege rotas exigindo um token JWT válido no cabeçalho Authorization.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256", auto_error: bool = True):
        """
        Inicializa o validador com chave e algoritmo padrão.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def __call__(self, request: Request):
        """
        Executa a validação do token na requisição.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Esquema de autenticação inválido"
                )
            if not self._verify_token(credentials.credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Token inválido ou expirado"
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Credenciais de autenticação não fornecidas"
            )

    def _verify_token(self, token: str) -> bool:
        """
        Verifica se o token é válido e não expirou.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return "sub" in payload
        except JWTError:
            return False
