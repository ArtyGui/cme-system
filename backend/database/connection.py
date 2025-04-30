from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configurações de conexão
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "db"  # o nome do serviço no docker-compose
DB_PORT = "5432"
DB_NAME = "cme_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """
    Fornece uma instância de banco de dados para uso nas dependências do FastAPI.
    Cuida da abertura e fechamento da sessão automaticamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
