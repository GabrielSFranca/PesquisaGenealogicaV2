from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Uniao(Base):
    __tablename__="unioes"
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    conjuge_id1: Mapped[int] = mapped_column(ForeignKey('individuos.id'), nullable=False) # uniao so existe entre duas pessoas que nao sao a mesma e nao sao pais-filhos
    conjuge_id2: Mapped[int] = mapped_column(ForeignKey('individuos.id'), nullable=False)
    
    conjuge1: Mapped["Individuo"] = relationship(foreign_keys=[conjuge_id1], back_populates="unioes_como_conjuge1")
    conjuge2: Mapped["Individuo"] = relationship(foreign_keys=[conjuge_id2], back_populates="unioes_como_conjuge2")
    
    filhos: Mapped[List["Individuo"]]=relationship(
        foreign_keys="[Individuo.id_uniao_pais]", 
        back_populates="uniao_pais"
    )
    
    # data do evento casamento
    dia_casamento: Mapped[Optional[int]]=mapped_column()
    mes_casamento: Mapped[Optional[int]]=mapped_column()
    ano_casamento: Mapped[Optional[int]]=mapped_column()
    # local do casamento
    local_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locais.id"))
    local: Mapped[Optional["Local"]] = relationship(back_populates="unioes")
    
    def __repr__(self) -> str:
        return f"<Uniao: {self.conjuge_id1.nome} + {self.conjuge_id2.nome}"