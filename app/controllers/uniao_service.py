from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.controllers.schemas import UnSchema
from app.testes.tables import Uniao, Individuo, Local


class UniaoService:
    def __init__(self, DBSessionMkr: sessionmaker):
        """Inicializa o serviço com uma fábrica de sessões."""
        self.Session = DBSessionMkr

    def criar_uniao(self, dados_entrada: dict) -> Uniao:
        """
        Cria uma nova união (casamento) após validação com Pydantic.

        Args:
            dados_entrada: Dicionário contendo conjuge_id1, conjuge_id2, e dados opcionais.

        Returns:
            Objeto Uniao criado.
        """
        try:
            dados_validados = UnSchema(**dados_entrada)
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

                if dados_validados.local_id is not None:
                    local = db.get(Local, dados_validados.local_id)
                    if local is None:
                        raise ValueError(f"Local com ID {dados_validados.local_id} não encontrado.")

                nova_uniao = Uniao(
                    conjuge_id1=dados_validados.conjuge_id1,
                    conjuge_id2=dados_validados.conjuge_id2,
                    dia_casamento=dados_validados.dia_casamento,
                    mes_casamento=dados_validados.mes_casamento,
                    ano_casamento=dados_validados.ano_casamento,
                    local_id=dados_validados.local_id,
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
