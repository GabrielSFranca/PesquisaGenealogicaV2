import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

# from app.testes.tables import Base, DATABASE_URI
# from app.models import *
# URL do banco de dados (pode ser movida para um .env futuramente)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("variavel nao encontrada no env")

#M MUDAR
# cria o motor de conexao
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,         # O Postgres gerencia um pool (piscina) de conexões
    max_overflow=20,       # Conexões extras permitidas em momentos de pico
)

# cria a fabrica de sessoes
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# db=SessionLocal()
# try:
#     yield db
# finally db.close()
    
def init_db():
    # cria todas as tabelas do banco de dados se elas ainda nao existirem
    Base.metadata.create_all(bind=engine)