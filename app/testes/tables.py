from enum import Enum
from typing import Optional, List
from sqlalchemy import create_engine, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship, validates

DATABASE_URI = "sqlite:///dbtest1.db"
# engine = create_engine(DATABASE_URL, echo=True)

# Session = sessionmaker(bind=engine)
# session = Session()
class Base(DeclarativeBase):
    pass

# enums
class GenderEnum(Enum):
    M = "masculino"
    F = "feminino"
    NB = "nao-binario"
    OTHER = "outro"
    
class EvenTagEnum(Enum):
    BIRT = "Nascimento"
    CHR = "Batismo"
    DEAT = "Falecimento"
    IMMI = "Imigracao"

    # MARR = "Casamento"
    
# tabelas
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
    #eventos
        
    # # 2. Validação de Nome (Impedir strings vazias ou só com espaços)
    # @validates('nome', 'sobrenome') # Você pode validar múltiplas colunas de uma vez
    # def validar_nome(self, key, val):
    #     if not val or not val.strip():
    #         raise ValueError(f"Erro: O campo '{key}' não pode estar em branco.")
            
    #     return val.strip().title() # Remove espaços extras e capitaliza (ex: " joão " -> "João")
    
    def nome_completo(self) -> str:
         return f"{self.nome} {self.sobrenome}"
    
    def __repr__(self) -> str:
        return f"([{self.id}] {self.nome_completo()}- {self.genero})"

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
    
    # def __init__(self, tipo, d, m, a, data_exata=True, notas=""):
    #     self.tag=tipo
    #     self.dia=d
    #     self.mes=m
    #     self.ano=a
    #     self.data_exata=data_exata
    #     self.notas=notas
        
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

class Local(Base):
    __tablename__="locais"
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    # Detalhes geográficos normalizados
    cidade: Mapped[Optional[str]] = mapped_column(String(100))
    estado: Mapped[Optional[str]] = mapped_column(String(100)) # Opcional (ex: países sem estados)
    regiao: Mapped[Optional[str]] = mapped_column(String(100)) # Ex: Europa, América do Sul, etc.
    pais: Mapped[str] = mapped_column(String(100), nullable=False, default="Brasil")
    
    # def __init__(self, cidade, estado, regiao, pais="Brasil"):
    #     self.cidade=cidade
    #     self.estado=estado
    #     self.regiao=regiao
    #     self.pais=pais
    
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
    
    #local: Mapped[Optional[str]] = mapped_column() local vem de outra tabela
    #lista de filhos


# Base.metadata.create_all(bind=engine)





# from sqlalchemy import create_engine, String
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# # 1. O Engine: É a ponte de comunicação com o SQLite
# # echo=True faz com que o SQLAlchemy imprima no terminal todo o SQL que ele gera
# engine = create_engine("sqlite:///meubanco.db", echo=True)

# # 2. A Classe Base: Todas as nossas tabelas vão herdar desta classe
# class Base(DeclarativeBase):
#   pass
    #resolver regiao
    # def __repr__(self) -> str:
        
    #     loc_str_formatado = f"id=[{self.id}] "
        
    #     if not self.regiao:
    #         self.regiao="null"
            
    #     if not self.cidade:
    #         self.cidade="null"
            
    #     if not self.estado:
    #         self.estado="null"
            
    #     loc_str_formatado = loc_str_formatado + f"{self.cidade}, {self.estado}, {self.pais}"
            
    #     return (loc_str_formatado)
    # def nome_formatado(self) -> str:
    #     partes = [self.cidade]
    #     if self.estado: partes.append(self.estado)
    #     partes.append(self.pais)
    #     return ", ".join(partes)