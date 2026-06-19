# from app.repositories.evento_repository import EventoRepository
from app.models.evento import Evento, EventCreateSchema
from app.models.enums import GenderEnum, EvenTagEnum
from app.models.individuo import Individuo, IndividuoCreate
# from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import sessionmaker
# from app.repositories.individuo_repository import IndividuoRepository
# from app.repositories.local_repository import LocalRepository
from app.models.local import Local, LocalCreate

class IndividuoEventoService:
    def __init__(self, DBSessionMaker: sessionmaker):
        self.Session=DBSessionMaker
        # self.repo=EventoRepository(DBSessionMaker)

    def cadastro_indi_eventos(self, data: IndividuoCreate):
        with self.Session() as db:
            try:
                # repo_loc=LocalRepository(db)
                if data.eventos.local:
                    local_evento=Local(
                        cidade=data.eventos.local.cidade,
                        estado=data.eventos.local.estado,
                        regiao=data.eventos.local.regiao,
                        pais=data.eventos.local.pais
                    )
                    db.add(local_evento)
                    db.flush()
                else:
                    local_evento=None
                    
                # loc=repo_loc.create(data.eventos.local)
                # repo_indiv=IndividuoRepository(db)
                novo_individuo=Individuo(
                    nome=data.nome, 
                    sobrenome=data.sobrenome, 
                    genero=data.genero)
                db.add(novo_individuo)
                # O flush() sincroniza com o PostgreSQL para gerar os IDs na memória,
                # permitindo o relacionamento sem efetivar o commit ainda.
                db.flush()
                
                # Passo 3: Criar o Evento (Nascimento) linkando os IDs gerados
                
                # se nao tem evento do tipo, adiciona
                # se nao tem, edita
                novo_event=Evento(
                    tag=EvenTagEnum.BIRT,
                    dia=data.eventos.dia,
                    mes=data.eventos.mes,
                    ano=data.eventos.ano,
                    data_exata=data.eventos.data_exata,
                    notas=data.eventos.notas,
                    local=local_evento
                    # individuo_id=novo_individuo.id,
                    # local_id=loc.id if loc else None,
                )
                
                novo_individuo.eventos.append(novo_event) # nao sei se funciona
                db.add(novo_event)
                # db.add(novo_individuo)

                # novo_i=repo_indiv.cria(novo_individuo)
                # novo_i.eventos.append(evento_nascimento)
                # db.add(evento_n;ascimento)
                # repo_indiv
                db.commit()
                
                db.refresh(novo_individuo)
                
                return True, "Finalizado com sucess"
            
            except IntegrityError:
                db.rollback()
                return False, "Erro de integridade: dados duplicados ou inválidos"
            
            except SQLAlchemyError as err_db:
                db.rollback()
                return False, f"Erro na base de dados: {str(err_db)}"
                
                