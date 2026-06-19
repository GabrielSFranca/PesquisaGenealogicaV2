from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from app.models.local import Local

class LocalRepository:
    def __init__(self, DBSessionMaker: sessionmaker):
        self.Session = DBSessionMaker

    def create(self, data):
        self.Session.add(data)
        self.Session.flush()
        return data    
    # def get_by_id(self, id):
    #     with self.Session() as db:
    #         indi=db.get(Individuo, id)
    #         if indi:
    #             return indi
    #         return None
            
 