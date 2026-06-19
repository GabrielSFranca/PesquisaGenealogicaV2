from PySide6.QtCore import QObject, Slot, Signal
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, or_, and_

from app.controllers.schemas import IndividuoSchema
from app.repositories.uniao_repository import UniaoRepository
from app.testes.tables import Individuo, Uniao

class Controller(QObject):
    cadastroFinalizado=Signal(bool, str)
    uniaoFinalizada=Signal(bool, str)
    filiacaoFinalizada=Signal(bool, str)
    
    def __init__(self, ses_mkr: sessionmaker ):
        super().__init__()
        self.Session=ses_mkr
        self.uniao_service=UniaoRepository(ses_mkr)
    
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

    @Slot(str, str, str)
    def cria_filiacao(self, filho_id, pai_id1, pai_id2):
        try:
            dados_entrada = {
                "filho_id": self._parse_required_int(filho_id, "ID do(a) filho(a)"),
                "pai_id1": self._parse_required_int(pai_id1, "ID do pai/mãe 1"),
                "pai_id2": self._parse_required_int(pai_id2, "ID do pai/mãe 2"),
            }
            if dados_entrada["pai_id1"] == dados_entrada["pai_id2"]:
                raise ValueError("Os pais devem ser indivíduos diferentes.")
            if dados_entrada["filho_id"] in (dados_entrada["pai_id1"], dados_entrada["pai_id2"]):
                raise ValueError("O filho não pode ser um dos pais.")

            with self.Session() as session:
                filho = session.get(Individuo, dados_entrada["filho_id"])
                if filho is None:
                    raise ValueError(f"Indivíduo com ID {dados_entrada['filho_id']} não encontrado.")

                if filho.id_uniao_pais is not None:
                    raise ValueError(f"{filho.nome_completo()} já possui pais vinculados.")

                pai1 = session.get(Individuo, dados_entrada["pai_id1"])
                if pai1 is None:
                    raise ValueError(f"Indivíduo com ID {dados_entrada['pai_id1']} não encontrado.")

                pai2 = session.get(Individuo, dados_entrada["pai_id2"])
                if pai2 is None:
                    raise ValueError(f"Indivíduo com ID {dados_entrada['pai_id2']} não encontrado.")

                uniao_existente = session.query(Uniao).filter(
                    or_(
                        and_(
                            Uniao.conjuge_id1 == dados_entrada["pai_id1"],
                            Uniao.conjuge_id2 == dados_entrada["pai_id2"],
                        ),
                        and_(
                            Uniao.conjuge_id1 == dados_entrada["pai_id2"],
                            Uniao.conjuge_id2 == dados_entrada["pai_id1"],
                        ),
                    )
                ).first()

                if uniao_existente is None:
                    uniao_existente = Uniao(
                        conjuge_id1=dados_entrada["pai_id1"],
                        conjuge_id2=dados_entrada["pai_id2"],
                    )
                    session.add(uniao_existente)
                    session.flush()
                    self.uniaoFinalizada.emit(
                        True,
                        f"União registrada entre os indivíduos {uniao_existente.conjuge_id1} e {uniao_existente.conjuge_id2}.",
                    )

                filho.id_uniao_pais = uniao_existente.id
                session.commit()

                self.filiacaoFinalizada.emit(
                    True,
                    f"Filiação registrada do indivíduo {dados_entrada['filho_id']} a {uniao_existente.conjuge_id1} e {uniao_existente.conjuge_id2}.",
                )
        except ValueError as err:
            self.filiacaoFinalizada.emit(False, str(err))
        except Exception as err:
            self.filiacaoFinalizada.emit(False, f"Erro ao criar filiação: {str(err)}")



