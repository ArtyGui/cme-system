from pydantic import BaseModel, constr
from enum import Enum

class RoleEnum(str, Enum):
    """
    Enumeração dos tipos de usuário aceitos no sistema.
    """
    tecnico = "tecnico"
    enfermagem = "enfermagem"
    administrativo = "administrativo"

class UserCreate(BaseModel):
    """
    Schema para a criação de um novo usuário.

    Atributos:
        username (str): Nome de usuário único.
        password (str): Senha do usuário.
        role (RoleEnum): Tipo/função do usuário (técnico, enfermagem ou administrativo).
    """
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6)
    role: RoleEnum

class UserResponse(BaseModel):
    """
    Schema para a resposta da API ao retornar dados de um usuário.

    Atributos:
        id (int): ID do usuário.
        username (str): Nome do usuário.
        role (RoleEnum): Tipo de função do usuário.
    """
    id: int
    username: str
    role: RoleEnum

    class Config:
        orm_mode = True
