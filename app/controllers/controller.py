from PySide6.QtCore import QObject, Slot, Signal
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.schemas import IndividuoSchema
from app.controllers.uniao_service import UniaoService
from app.testes.tables import Individuo

class Controller(QObject):
    cadastroFinalizado=Signal(bool, str)
    uniaoFinalizada=Signal(bool, str)
    
    def __init__(self, ses_mkr: sessionmaker ):
        super().__init__()
        self.Session=ses_mkr
        self.uniao_service=UniaoService(ses_mkr)
    
    @Slot(str, str, str)
    def cria_individuo(self, nome, sobrenome, genero):
        try:
            dados_validados=IndividuoSchema(
                nome=nome,
                sobrenome=sobrenome,
                genero=genero
            )      
        except ValidationError as err:
            self.cadastroFinalizado.emit(False, f"err de validacao: \n{err.errors()[0]['msg']}")
            return 

        gen_enum=dados_validados.genero

        with self.Session() as session:
            try:
                novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=gen_enum
                )
                session.add(novo_indi)
                session.commit()
                session.refresh(novo_indi)
                
                self.cadastroFinalizado.emit(True, f"Imigrante pioneiro {novo_indi.nome_completo()} registrado!")
                
            except SQLAlchemyError as err_db:
                session.rollback()
                self.cadastroFinalizado.emit(False, "erro ao gravar na database")
                raise Exception(f"Erro na base de dados: {str(err_db)}")
            
    

    @staticmethod
    def _parse_required_int(valor: str, campo: str) -> int:
        valor_limpo = valor.strip()
        if not valor_limpo:
            raise ValueError(f"{campo} é obrigatório.")
        try:
            return int(valor_limpo)
        except ValueError:
            raise ValueError(f"{campo} deve ser um número inteiro.")

    @staticmethod
    def _parse_optional_int(valor: str, campo: str):
        valor_limpo = valor.strip()
        if not valor_limpo:
            return None
        try:
            return int(valor_limpo)
        except ValueError:
            raise ValueError(f"{campo} deve ser um número inteiro.")

    @Slot(str, str, str, str, str, str)
    def cria_uniao(self, conjuge_id1, conjuge_id2, dia_casamento, mes_casamento, ano_casamento, local_id):
        try:
            dados_entrada = {
                "conjuge_id1": self._parse_required_int(conjuge_id1, "ID do cônjuge 1"),
                "conjuge_id2": self._parse_required_int(conjuge_id2, "ID do cônjuge 2"),
                "dia_casamento": self._parse_optional_int(dia_casamento, "Dia do casamento"),
                "mes_casamento": self._parse_optional_int(mes_casamento, "Mês do casamento"),
                "ano_casamento": self._parse_optional_int(ano_casamento, "Ano do casamento"),
                "local_id": self._parse_optional_int(local_id, "ID do local"),
            }

            nova_uniao = self.uniao_service.criar_uniao(dados_entrada)
            self.uniaoFinalizada.emit(
                True,
                f"União registrada entre os indivíduos {nova_uniao.conjuge_id1} e {nova_uniao.conjuge_id2}.",
            )
        except ValueError as err:
            self.uniaoFinalizada.emit(False, str(err))
        except Exception as err:
            self.uniaoFinalizada.emit(False, f"Erro ao criar união: {str(err)}")
