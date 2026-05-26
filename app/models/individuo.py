from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .enums import GenderEnum
from .base import Base

class Individuo(Base):
    # alteramos o nome da tabela pela variavel interna da classe Base
    __tablename__="individuos"
    
    # define 'id' como chave primaria com autoincremento
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    
    # define uma coluna de texto obrigatoria
    nome: Mapped[str]=mapped_column(String(50), nullable=False)
    sobrenome: Mapped[str]=mapped_column(String(100), nullable=False)
    
    genero: Mapped[GenderEnum] = mapped_column(
        SQLEnum(GenderEnum, native_enum=False, length=10), 
        nullable=False,
        default=GenderEnum.OTHER
    ) # opcional = native_enum=False         default=GenderEnum.OTHER
    #genero
    #pais
    
    id_uniao_pais: Mapped[Optional[int]]=mapped_column(ForeignKey('unioes.id'))
    
    uniao_pais: Mapped[Optional["Uniao"]]=relationship(
        foreign_keys=[id_uniao_pais],
        back_populates="filhos"
    )
    
    # Relações bidirecionais exigidas pela classe Uniao
    unioes_como_conjuge1: Mapped[List["Uniao"]] = relationship(
        foreign_keys="[Uniao.conjuge_id1]", 
        back_populates="conjuge1"
    )
    
    unioes_como_conjuge2: Mapped[List["Uniao"]] = relationship(
        foreign_keys="[Uniao.conjuge_id2]", 
        back_populates="conjuge2"
    )
    
    eventos: Mapped[Optional[List["Evento"]]]=relationship(
        back_populates="indi", 
        cascade="all, delete-orphan"
    )
    
    def nome_completo(self) -> str:
         return f"{self.nome} {self.sobrenome}"
    
    def __repr__(self) -> str:
        return f"([{self.id}] {self.nome_completo()}- {self.genero})"