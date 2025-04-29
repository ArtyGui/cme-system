from sqlalchemy import Column, Integer, String, Enum
from database.connection import Base
import enum

class RoleEnum(enum.Enum):
    """
    Enumeração que define os tipos de usuários no sistema.

    - tecnico: Usuário técnico responsável por realizar as etapas do processo de CME.
    - enfermagem: Usuário da enfermagem responsável por verificar rastreabilidade e consultar relatórios.
    - administrativo: Usuário administrativo responsável por cadastrar novos usuários e funções.
    """
    tecnico = "tecnico"
    enfermagem = "enfermagem"
    administrativo = "administrativo"

class User(Base):
    """
    Modelo de tabela para armazenar informações de usuários do sistema.

    Atributos:
        id (Integer): Identificador único do usuário (Primary Key).
        username (String): Nome de login do usuário (deve ser único).
        password (String): Senha de acesso do usuário.
        role (Enum): Função do usuário (definida pela enumeração RoleEnum).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
