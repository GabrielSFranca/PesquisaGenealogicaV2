from PySide6.QtCore import QObject, Slot, Signal
from sqlalchemy.orm import sessionmaker
from app.services.individuo_service import IndividuoService
from app.repositories.individuo_repository import IndividuoRepository

class IndividuoController(QObject):
    
    cadastro_finalizado=Signal(bool, str)
    
    def __init__(self, DBSessionMaker: sessionmaker ):
        super().__init__()
        self.service=IndividuoService(DBSessionMaker)
        self.indi_repo=IndividuoRepository(DBSessionMaker)
    
    @Slot(str, str, str)
    def criar(self, nome, sobrenome, genero):
        try: 
            sucess, msg =self.service.criar(nome, sobrenome, genero)
            self.cadastro_finalizado.emit(sucess, msg)
        except Exception:
            raise
    
    @Slot(result=list)
    def listar_todos(self):
        individuos=self.indi_repo.get_all()

        lista_qml = []
        for i in individuos:
            gen = i.genero.value if hasattr(i.genero, "value") else i.genero
            lista_qml.append(
                {
                    "id": i.id,
                    "nome": i.nome,
                    "sobrenome": i.sobrenome,
                    "genero": gen,
                }
            )

        return lista_qml
        
