from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Antes (SQLite):
# DATABASE_URL = "sqlite:///mydb.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Agora (PostgreSQL):
DATABASE_URL = "postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=10,         # O Postgres gerencia um pool (piscina) de conexões
    max_overflow=20       # Conexões extras permitidas em momentos de pico
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# A nova URL de conexão aponta para o seu container Docker local
# Formato: postgresql+driver://usuario:senha@localhost:porta/nome_do_banco
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/genealogiadb"

# IMPORTANTE: Remover o connect_args={"check_same_thread": False}
# O PostgreSQL gere conexões de forma nativa e não precisa (nem aceita) esse comando do SQLite.
engine = create_engine(
    DATABASE_URL, 
    echo=True,          # Mantém o log do SQL no terminal
    pool_size=10,       # (Opcional) O Postgres lida bem com pools de conexão
    max_overflow=20
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. Carrega as variáveis de ambiente do ficheiro .env para a memória
load_dotenv()

# 2. Pega a URL. Se não existir, o sistema avisa imediatamente (Fail-Fast)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada no ficheiro .env!")

# 3. Cria o Engine do PostgreSQL
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 4. A Fábrica de Sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def init_db():
    """Cria as tabelas físicas no PostgreSQL caso não existam"""
    Base.metadata.create_all(bind=engine)