from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
from typing import Optional, List

# from app.controllers.schemas import UniaoCreateSchema
# from app.testes.tables import Individuo, Local
from app.models.uniao import Uniao, UniaoCreateSchema
from app.models.individuo import Individuo, IndividuoCreateSchema
from app.models.local import Local

class UniaoRepository:
    def __init__(self, DBSession: sessionmaker):
        """Inicializa o serviço com uma fábrica de sessões."""
        self.Session = DBSession
    
    def criar(self, conjuge1, conjuge2):
        return
    
    def get_by_id(self, id):
        with self.Session() as db:
            data=db.get(Uniao, id)
            if not data:
                return None
            return data
            # if data:
            #     return data
            # return None
    
    def create(self, data: Uniao) -> Optional[Uniao]:
        with self.Session() as db:
            try:
                db.add(data)
                db.commit()
                db.refresh(data)
                return data
            except IntegrityError:
                db.rollback()
                raise
            except SQLAlchemyError:
                db.rollback()
                raise
            
    
    def add_child(self, child: Individuo, union: Uniao):
        with self.Session() as db:
            try:
                union.filhos.append(child)
                db.commit()
                db.refresh(union)
                return True, "Filho adicionado com sucesso"
            except IntegrityError:
                db.rollback()
                return False, "Erro de integridade: dados duplicados ou inválidos"
            except SQLAlchemyError as err_db:
                db.rollback()
                return False, f"Erro na base de dados: {str(err_db)}"
    
        
        
        
    def adicionar(self, dados):
        with self.Session() as db:
            try:
                conj1 = db.get(Individuo, dados.conjuge_id1)
                conj2 = db.get(Individuo, dados.conjuge_id2)

                if conj1 is None:
                    raise ValueError(f"Indivíduo com ID {dados.conjuge_id1} não encontrado.")
                if conj2 is None:
                    raise ValueError(f"Indivíduo com ID {dados.conjuge_id2} não encontrado.")

                uniao_exist = db.query(Uniao).filter(
                    or_(
                        and_(
                            Uniao.conjuge_id1 == dados.conjuge_id1,
                            Uniao.conjuge_id2 == dados.conjuge_id2,
                        ),
                        and_(
                            Uniao.conjuge_id1 == dados.conjuge_id2,
                            Uniao.conjuge_id2 == dados.conjuge_id1,
                        ),
                    )
                ).first()

                if uniao_exist is not None:
                    raise ValueError("Essa união já está cadastrada.")

                if dados.loc_id is not None:
                    local = db.get(Local, dados.loc_id)
                    if local is None:
                        raise ValueError(f"Local com ID {dados.loc_id} não encontrado.")

                nova_uniao = Uniao(
                    conjuge_id1=dados.conjuge_id1,
                    conjuge_id2=dados.conjuge_id2,
                    dia_casamento=dados.dia,
                    mes_casamento=dados.mes,
                    ano_casamento=dados.ano,
                    local_casamento_id=dados.loc_id,
                )

                db.add(nova_uniao)
                db.commit()
                db.refresh(nova_uniao)
                return nova_uniao

            except ValueError:
                db.rollback()
                raise
            except SQLAlchemyError as err_db:
                db.rollback()
                raise Exception(f"Erro ao salvar a união no banco de dados: {str(err_db)}")

    def criar_uniao(self, dados_entrada: dict) -> Uniao:
        """
        Cria uma nova união (casamento) após validação com Pydantic.

        Args:
            dados_entrada: Dicionário contendo conjuge_id1, conjuge_id2, e dados opcionais.

        Returns:
            Objeto Uniao criado.
        """
        try:
            dados_validados = UniaoCreateSchema(**dados_entrada)
        except ValidationError as err:
            raise ValueError(f"Erro de validação na união: {err.errors()[0]['msg']}")

        with self.Session() as db:
            try:
                conjuge1 = db.get(Individuo, dados_validados.conjuge_id1)
                conjuge2 = db.get(Individuo, dados_validados.conjuge_id2)

                if conjuge1 is None:
                    raise ValueError(f"Indivíduo com ID {dados_validados.conjuge_id1} não encontrado.")
                if conjuge2 is None:
                    raise ValueError(f"Indivíduo com ID {dados_validados.conjuge_id2} não encontrado.")

                uniao_existente = db.query(Uniao).filter(
                    or_(
                        and_(
                            Uniao.conjuge_id1 == dados_validados.conjuge_id1,
                            Uniao.conjuge_id2 == dados_validados.conjuge_id2,
                        ),
                        and_(
                            Uniao.conjuge_id1 == dados_validados.conjuge_id2,
                            Uniao.conjuge_id2 == dados_validados.conjuge_id1,
                        ),
                    )
                ).first()

                if uniao_existente is not None:
                    raise ValueError("Essa união já está cadastrada.")

                if dados_validados.local_casamento_id is not None:
                    local = db.get(Local, dados_validados.local_casamento_id)
                    if local is None:
                        raise ValueError(f"Local com ID {dados_validados.local_casamento_id} não encontrado.")

                nova_uniao = Uniao(
                    conjuge_id1=dados_validados.conjuge_id1,
                    conjuge_id2=dados_validados.conjuge_id2,
                    dia_casamento=dados_validados.dia_casamento,
                    mes_casamento=dados_validados.mes_casamento,
                    ano_casamento=dados_validados.ano_casamento,
                    local_id=dados_validados.local_casamento_id,
                )

                db.add(nova_uniao)
                db.commit()
                db.refresh(nova_uniao)
                return nova_uniao

            except ValueError:
                db.rollback()
                raise
            except SQLAlchemyError as err_db:
                db.rollback()
                raise Exception(f"Erro ao salvar a união no banco de dados: {str(err_db)}")
