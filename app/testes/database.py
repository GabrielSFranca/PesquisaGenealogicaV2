import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/genealogia"
)

engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)