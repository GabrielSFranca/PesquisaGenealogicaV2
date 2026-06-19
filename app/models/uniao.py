from datetime import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator

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
        return f"<Uniao: {self.conjuge1.nome} + {self.conjuge2.nome}"
    
    
class UniaoCreateSchema(BaseModel):
    conjuge_id1: int = Field(..., gt=0, description="ID do primeiro cônjuge")
    conjuge_id2: int = Field(..., gt=0, description="ID do segundo cônjuge")
    
    # Datas do casamento (opcionais)
    dia_casamento: Optional[int] = Field(default=None, ge=1, le=31, description="Dia do casamento")
    mes_casamento: Optional[int] = Field(default=None, ge=1, le=12, description="Mês do casamento")
    ano_casamento: Optional[int] = Field(default=None, ge=1870, le=datetime.now().year, description="Ano do casamento")
    
    # Local do casamento (opcional)
    local_casamento_id: Optional[int] = Field(default=None, gt=0, description="ID do local do casamento")
    
    @field_validator('ano_casamento')
    @classmethod
    def validar_ano_casamento(cls, val: int) -> int:
        '''Impede registro de casamentos no futuro'''
        if val is not None:
            ano_atual = datetime.now().year
            if val > ano_atual:
                raise ValueError(f"O ano {val} não pode ser futuro")
        return val
    
    @model_validator(mode='after')
    def validar_conjuges_diferentes(self) -> 'UniaoCreateSchema':
        if self.conjuge_id1 == self.conjuge_id2:
            raise ValueError("Os cônjuges devem ser pessoas diferentes (conjuge_id1 ≠ conjuge_id2)")
        return self
    
    @model_validator(mode='after')
    def validar_data_casamento(self) -> 'UniaoCreateSchema':
        '''
        Validação cruzada complexa:
        1. Se tem dia, deve ter mês e ano.
        2. Verifica se a data realmente existe no calendário.
        '''
        # Regra 1: Coerência de preenchimento
        if self.dia_casamento is not None and (self.mes_casamento is None or self.ano_casamento is None):
            raise ValueError("Se o dia for informado, o mês e o ano também devem ser preenchidos.")
        
        # Regra 2: Validação no calendário real
        if self.dia_casamento and self.mes_casamento and self.ano_casamento:
            try:
                datetime(self.ano_casamento, self.mes_casamento, self.dia_casamento)
            except ValueError:
                raise ValueError(f"A data {self.dia_casamento}/{self.mes_casamento}/{self.ano_casamento} é inválida no calendário.")
        
        return self