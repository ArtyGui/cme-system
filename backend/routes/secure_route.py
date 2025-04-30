from fastapi import APIRouter, Depends
from dependencies.jwt_bearer import JWTBearer

router = APIRouter(prefix="/secure", tags=["Protegidas"])

jwt_bearer = JWTBearer(secret_key="super-secret-key")


@router.get("/usuarios", dependencies=[Depends(jwt_bearer)])
def usuarios_protegidos():
    return {"message": "Acesso autenticado com sucesso!"}
