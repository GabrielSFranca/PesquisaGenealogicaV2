from typing import Optional
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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