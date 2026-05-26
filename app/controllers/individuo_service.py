from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.models import Individuo

class IndividuoService:
    def __init__(self, DBSessionMkr: sessionmaker):
        self.Session = DBSessionMkr

    def adicionar(self, dados_validados) -> Individuo:
        with self.Session() as db:
            novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=dados_validados.genero,
                )
            try:
                db.add(novo_indi)
                db.commit()
                db.refresh(novo_indi)
                return novo_indi
            except SQLAlchemyError as err_db:
                db.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}") from err_db

    def pesquisa(self, nome=None, sobrenome=None):
        with self.Session() as session:
            try:
                stmt = select(Individuo)
                if nome is not None:
                    stmt = stmt.where(Individuo.nome == nome)
                if sobrenome is not None: 
                    stmt = stmt.where(Individuo.sobrenome == sobrenome)
                return session.scalars(stmt).all()
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}") from err_db

    def pesquisa_simples(self, nome, sobrenome):
        return

    def listar_todos(self):
        with self.Session() as db:
            # return db.execute(select(Individuo)).scalars().all()
            # Executa a query equivalente a: SELECT * FROM individuo;
            individuos=db.query(Individuo).all()
            # return db.query(Individuo).all()
            # individuos=session.query(Individuo).all()
            if not individuos:
                print("Nenhuma pessoa encontrada no banco de dados")
                return
            
            return individuos

    def apagar(self, individuo_id: int) -> bool:
        with self.Session() as db:
            try:
                indi = db.get(Individuo, individuo_id)
                if indi is None:
                    raise ValueError(f"Indivíduo com id {individuo_id} não encontrado")

                db.delete(indi)
                db.commit()
                return True
            except SQLAlchemyError as err_db:
                db.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}") from err_db
