# validacao com pydantic
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator
# tabelas.py -> models
# from app.testes.tables import Individuo, Evento, GenderEnum, EvenTagEnum 

from app.models.individuo import Individuo
from app.models.evento import Evento
from app.models.uniao import Uniao
from app.models.enums import GenderEnum, EvenTagEnum

from typing import Optional
from datetime import datetime
import re
# db -> controller
# main -> GUI.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class EventSchema(BaseModel):
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
    def validar_calendario_real(self) -> 'EventSchema':
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
        
class IndividuoSchema(BaseModel):
    nome: str=Field(..., min_length=2, max_length=50, description="Primeiro nome da pessoa")
    sobrenome: str=Field(..., min_length=2, max_length=100, description="Sobrenome da pessoa")
    # validacao suja, nao sei como validar isso, mas tbm nao acho necessario
    genero: GenderEnum
    
    @field_validator('nome', 'sobrenome')
    @classmethod
    def validar_nome(cls, val: str) -> str:
        if not val:
            raise ValueError("O campo nao pode estar vazio")
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", val):
            raise ValueError("Nome deve conter apenas letras")
        return val.strip().title() # remove espacos em branco e captaliza


class UnSchema(BaseModel):
    conjuge_id1: int = Field(..., gt=0, description="ID do primeiro cônjuge")
    conjuge_id2: int = Field(..., gt=0, description="ID do segundo cônjuge")
    
    # Datas do casamento (opcionais)
    dia_casamento: Optional[int] = Field(default=None, ge=1, le=31, description="Dia do casamento")
    mes_casamento: Optional[int] = Field(default=None, ge=1, le=12, description="Mês do casamento")
    ano_casamento: Optional[int] = Field(default=None, ge=1870, le=datetime.now().year, description="Ano do casamento")
    
    # Local do casamento (opcional)
    local_id: Optional[int] = Field(default=None, gt=0, description="ID do local do casamento")
    
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
    def validar_conjuges_diferentes(self) -> 'UnSchema':
        if self.conjuge_id1 == self.conjuge_id2:
            raise ValueError("Os cônjuges devem ser pessoas diferentes (conjuge_id1 ≠ conjuge_id2)")
        return self
    
    @model_validator(mode='after')
    def validar_data_casamento(self) -> 'UnSchema':
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


#################################################################

class IndividuoController:
    def __init__(self, ses_mkr: sessionmaker):
        # injeta a fabrica de sessoes do sqlalchemy
        # permite usar psql ou sqlite
        self.Session = ses_mkr
        
    def cria_individuo(self, dados_entrada: dict):
        # 1-pydantic
        # recebe um dicionario
        eventos=[] # cria uma lista vazia de eventos da pessoa
        try:
            # valida com o esquema do pydantic
            dados_validados=IndividuoSchema(**dados_entrada) # ** serve para desencapsular dicionario
            nascimento=EventSchema(**dados_entrada["nascimento"])
            eventos.append(nascimento)
            
            # validar dados
        except ValidationError as err:
            # erro capturado pelo pydantic
            raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")
        
        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                # cria o individuo com seus dados pessoais
                novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=dados_validados.genero,
                    vivo=dados_validados.vivo
                )
                session.add(novo_indi)
                session.flush() # garante que indi esta disponivel
                
                for evento in eventos:
                    novo_event=Evento(
                        tag=EvenTagEnum.BIRT, # logica errada
                        data=evento.data,
                        local=evento.local.strip(),
                        notas=evento.notas,
                        indi_id=novo_indi.id
                    )
                    session.add(novo_event)

                # novo_indi.eventos.append(eventonascimento)
                session.commit()
                session.refresh(novo_indi)
                
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")
