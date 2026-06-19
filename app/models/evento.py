from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
# validacao com pydantic
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator

from app.models.individuo import IndividuoCreate
from app.models.local import LocalCreate

from .enums import EvenTagEnum
from .base import Base

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    tag: Mapped[EvenTagEnum] = mapped_column(
        SQLEnum(EvenTagEnum),
        nullable=False
    )    
    # data: dia INT, mes INT -> opcionais
    dia: Mapped[Optional[int]]=mapped_column()
    mes: Mapped[Optional[int]]=mapped_column()
    # data.ano: obrigatorio
    ano: Mapped[int]=mapped_column(nullable=False)
    data_exata: Mapped[bool] = mapped_column(default=True)
    # local: Mapped[Optional[str]] = mapped_column()
    notas: Mapped[Optional[str]] = mapped_column(String(200))

    indi_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    indi: Mapped["Individuo"] = relationship(back_populates="eventos")
    
    local_id: Mapped[Optional[int]]=mapped_column(ForeignKey("locais.id"))
    local: Mapped[Optional["Local"]]=relationship(back_populates="eventos")
        
    def get_ev_indi(self) -> tuple:
        fullname=self.indi.nome_completo() if self.indi else "Indi desconhecido"
        return (
            self.tag.value,
            self.dia,
            self.mes,
            self.ano,
            self.notas,
            fullname
        )

class EventResponseSchema(BaseModel):
    id: int
    tag: EvenTagEnum
    dia: Optional[int]
    mes: Optional[int]
    ano: int
    individuo: int
    local: Optional[int]


class EventCreate(BaseModel):
    dia: Optional[int]
    mes: Optional[int]
    ano: int
    data_exata: bool=True
    notas: Optional[str]
    # individuo: IndividuoCreate
    local: Optional[LocalCreate]
    


class EventCreateSchema(BaseModel):
    tag: EvenTagEnum
    
    # opcional, pode ser None
    # MASE SE for preenchido deve ser ge=1 maior ou igual a
    # a função Field Pydantic permite add metadados e restricoes diretamente na declaracao do atributo
    dia: Optional[int]= Field(default=None, ge=1, le=31, description="Dia do evento")
    mes: Optional[int]= Field(default=None, ge=1, le=12, description="Mês do evento")
    
    ano: int=Field(..., ge=1870, le=datetime.now().year, description="Ano do evento")
    data_exata: bool=True
    notas: Optional[str]=Field(default=None, max_length=200)
    # se a regra for personalizada, como um formato regex ou uma validacao logica, usamos o decorator field_validator
    
    # indi_id: int=field
    # local_id: int
    
    @field_validator('ano')
    @classmethod
    def validar_ano(cls, val: int) -> int:
        # impede registro de eventos no futuro
        if val is not None:
            ano_atual=datetime.now().year
            if val > ano_atual:
                raise ValueError(f"o ano {val} nao pode ser futuro")
        return val
    
    @field_validator('notas')
    @classmethod
    def clean_str(cls, v: Optional[str]) -> Optional[str]:
        # remove spacos em branco
        # anula str vazias
        if v is not None:
            v_limpo=v.strip()
            if len(v_limpo) == 0:
                return None
            return v_limpo
        return v
    
    @model_validator(mode='after')
    def validar_calendario_real(self) -> 'EventCreateSchema':
        '''
        Validação cruzada complexa: 
        1. Se tem dia, normalmente tem de ter mês e ano.
        2. Verifica se a data realmente existe no calendário (ex: anos bissextos).
        '''
        # Regra 1: Coerência de preenchimento
        if self.dia is not None and (self.mes is None or self.ano is None):
            raise ValueError("Se o dia for informado, o mês e o ano também devem ser preenchidos.")
        
        # Regra 2: Validação no calendário real
        if self.dia and self.mes and self.ano:
            try:
                # Tenta criar um objeto datetime apenas para ver se o Python aceita
                datetime(self.ano, self.mes, self.dia)
            except ValueError:
                raise ValueError(f"A data {self.dia}/{self.mes}/{self.ano} é uma data inexistente no calendário.")
                
        return self