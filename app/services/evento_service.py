from app.repositories.evento_repository import EventoRepository
from app.models.evento import Evento, EventCreateSchema
from pydantic import ValidationError

class EventoService:
    
    def __init__(self, DBSessionMaker):
        self.Session=DBSessionMaker
        self.repo=EventoRepository(DBSessionMaker)

    def criar(self, tag, d, m, a, data_exata, nt, individuo, local):

        try:
            dados_validados = EventCreateSchema(
                tag=tag,
                dia=d,
                mes=m,
                ano=a,
                data_exata=data_exata,
                notas=nt
            )
        except ValidationError as e:
            # Retorna erro de validação sem abrir sessão
            return False, f"Validação falhou: {e.errors()[0]['msg']}"
        
        # 2. Cria objeto com dados validados
        novo=Evento(
            tag=dados_validados.tag,
            dia=dados_validados.dia,
            mes=dados_validados.mes,
            ano=dados_validados.ano,
            data_exata=dados_validados.data_exata,
            notas=dados_validados.notas,
            indi_id=individuo.id,
            local_id=local.id    
        )
        
        # 3. Delega persistência ao repositório
        return self.repo.create(novo)
        
        # with self.Session() as db:
        #     repo = IndividuoRepository(db)
        #     return repo.create(novo)
            