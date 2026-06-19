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

class EventoRepository:
    def __init__(self, DBSession: sessionmaker):
        """Inicializa o serviço com uma fábrica de sessões."""
        self.Session = DBSession
    
    def criar(self, data):
        self.Session.add(data)
        return data
        # except Exception:
        #     raise
        # except IntegrityError:
        #     db.rollback()
        #     return False, "Erro de integridade: dados duplicados ou inválidos"
        # except SQLAlchemyError as err_db:
        #     db.rollback()
        #     return False, f"Erro na base de dados: {str(err_db)}"
            
    
    def create(self, data) -> tuple[bool, str]:
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