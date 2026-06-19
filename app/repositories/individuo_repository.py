from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from app.models import Individuo
from sqlalchemy.orm import Session

class IndividuoRepository:
    def __init__(self, DBSessionMaker: sessionmaker):
        self.Session = DBSessionMaker
        
    
    
    def cria(self, data):
        self.Session.add(data)
        return data
    
    def create(self, data: Individuo) -> tuple[bool, str]:
        with self.Session() as db: 
            try:
                db.add(data)
                db.commit()
                db.refresh(data)
                return True, "Dado criado com sucesso"
            except IntegrityError:
                db.rollback()
                return False, "Erro de integridade: dados duplicados ou inválidos"
            except SQLAlchemyError as err_db:
                db.rollback()
                return False, f"Erro na base de dados: {str(err_db)}"
            
    def get_by_id(self, id):
        with self.Session() as db:
            data=db.get(Individuo, id)
            if not data:
                return None
            return data
            
    # def get_by_id(self, id):
    #     try:
    #         return (self.db.query(Individuo)
    #                 .filter(Individuo.id == id)
    #                 .first()
    #         )
    #     except OperationalError:
    #         raise

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

    def pesquisa_por_nome(self, term: str):
        termo_limpo=term.strip().lower()
        if not termo_limpo:
            return []
        
        with self.Session() as db:
            stmt=select(Individuo).where(
                Individuo.nome_completo().lower().ilike(f"%{term}%")
            )
            return db.execute(stmt).scalars().all()
    
    
    
    def buscar_por_nome(self, termo_busca: str):
        
        
        with self.Session() as session:
            # O % ao redor do termo atua como um "coringa" no SQL (busca parcial)
            query = select(Individuo).where(
                Individuo.nome.ilike(f"%{termo_busca}%") |
                Individuo.sobrenome.ilike(f"%{termo_busca}%")
            )
            return session.execute(query).scalars().all()
    
    def buscar_simples(self, termo: str) -> List[Individuo]:
        """
        Realiza uma busca direta e rápida por nome/sobrenome no banco de dados.
        Retorna registros que contenham o termo digitado em qualquer parte do nome.
        """
        termo_limpo = termo.strip()
        if not termo_limpo:
            return []

        # O 'ilike' converte a busca em: WHERE nome LIKE '%termo%'
        # O uso de 'or_' permite expandir facilmente para buscar em outros campos no futuro (ex: observações)
        query = self.Session.query(Individuo).filter(
            Individuo.nome.ilike(f"%{termo_limpo}%")
        )
        
        # Ordena em ordem alfabética para facilitar a leitura na UI
        return query.order_by(Individuo.nome.asc()).all()

    def get_all(self):
        with self.Session() as db:
            stmt=select(Individuo)
            return db.execute(stmt).scalars.all()
        

            # # return db.execute(select(Individuo)).scalars().all()
            # # Executa a query equivalente a: SELECT * FROM individuo;
            # individuos=db.query(Individuo).all()
            # # return db.query(Individuo).all()
            # # individuos=session.query(Individuo).all()
            # if not individuos:
            #     print("Nenhuma pessoa encontrada no banco de dados")
            #     return
            
            # return individuos


    # def get_all(self, skip: int = 0, limit: int = 100): 
    #     with self.SesLoc() as db:
    #         try:
    #             return (
    #                 db.query(Usuario)
    #                 .order_by(Usuario.id)
    #                 .offset(skip)
    #                 .limit(limit)
    #                 .all()
    #             )
    #         except OperationalError:
    #             raise  


    def delete(self, data: Individuo) -> bool:
        try:
            self.Session.delete(data)
            self.Session.commit()
            return True
        except IntegrityError:
            self.Session.rollback()
            raise
        except SQLAlchemyError as err_db:
            self.Session.rollback()
            raise Exception(f"Erro na base de dados: {str(err_db)}") from err_db
        
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
