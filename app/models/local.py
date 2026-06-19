from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator

from .base import Base

class Local(Base):
    __tablename__="locais"
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    # Detalhes geográficos normalizados
    cidade: Mapped[Optional[str]] = mapped_column(String(100))
    estado: Mapped[Optional[str]] = mapped_column(String(100)) # Opcional (ex: países sem estados)
    regiao: Mapped[Optional[str]] = mapped_column(String(100)) # Ex: Europa, América do Sul, etc.
    pais: Mapped[str] = mapped_column(String(100), nullable=False, default="Brasil")
    # Relacionamento de volta para achar quais eventos/casamentos aconteceram aqui
    eventos: Mapped[List["Evento"]] = relationship(back_populates="local")
    unioes: Mapped[List["Uniao"]] = relationship(back_populates="local")
    
    def local_formatado(self) -> str:
        partes=[]
        if self.cidade:
            partes.append(self.cidade)
        if self.estado:
            partes.append(self.estado)
        
        partes.append(self.pais)
        return ", ".join(partes)
    
    def __repr__(self) -> str:
        return f"{self.local_formatado()}"
    

class LocalCreate(BaseModel):
    cidade: Optional[str]
    estado: Optional[str]
    regiao: Optional[str]
    pais: str