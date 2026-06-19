from app.repositories.individuo_repository import IndividuoRepository
from app.models.individuo import Individuo, IndividuoCreateSchema
from pydantic import ValidationError
from app.models.uniao import Uniao, UniaoCreateSchema
from app.repositories.uniao_repository import UniaoRepository
from app.repositories.individuo_repository import IndividuoRepository


class UniaoService:
    
    def __init__(self, DBSessionMaker):
        self.Session=DBSessionMaker
        self.repo_indiv=IndividuoRepository(DBSessionMaker)
        self.repo_union=UniaoRepository(DBSessionMaker)
        
    
    def adicionar_filiacao(self, filho: Individuo, union: Uniao):
        # verifica se a uniao exist
        # verifica se o filho existe
        
        if not self.repo_indiv.get_by_id(filho.id):
            return
        
        if filho.id_uniao_pais is not None:
            return
        
        if not self.repo_union.get_by_id(union.id):
            return
        
        self.repo_union.add_child(child=filho, union=union)
    
        # verifica se o filho ja tem pais
        
        
    def criar(self, c1: int, c2: int, d: int, m: int, a: int, local_id: int):
        # if c1 == c2:
        #     return ValueError("Pessoas iguais")
        try:
            dados_validados=UniaoCreateSchema(
                conjuge_id1=c1,
                conjuge_id2=c2,
                dia_casamento=d,
                mes_casamento=m,
                ano_casamento=a,
                local_casamento_id=local_id
            )
        except ValidationError:
            raise
        
        
        with self.Session() as db:
            indiv_repo=IndividuoRepository(db)
            
            conjuge1=indiv_repo.get_by_id(c1)
            conjuge2=indiv_repo.get_by_id(c2)
            
            if conjuge1 is None:
                return ValueError(f"pessoa com id {c1} nao existe")
            if conjuge2 is None:
                return ValueError(f"pessoa com id {c2} nao existe")
            
            
            # falta verificar se a uniao existe
            
            novo=Uniao(
                conjuge_id1=dados_validados.conjuge_id1,
                conjuge_id2=dados_validados.conjuge_id2,
                dia_casamento=dados_validados.dia_casamento,
                mes_casamento=dados_validados.mes_casamento,
                ano_casamento=dados_validados.ano_casamento,
                local_id=dados_validados.local_casamento_id
            )
            
            un_repo=UniaoRepository(db)
        
            try:
                un_nova=un_repo.create(novo)
                return True, "uniao cadastrada com sucesso"
                # return (un_repo.create(novo))
                # novo=repo.create()
            except Exception:
                raise
        
        
        # try:
        #     dados_validados=UniaoCreateSchema(
        #         conjuge_id1=c1,
        #         conjuge_id2=c2,
        #         dia_casamento=d,
        #         mes_casamento=m,
        #         ano_casamento=a,
        #         local_casamento_id=local_id
        #     )
        # except ValidationError:
        #     raise
        
        # with self.Session() as db:
        #     novo=Uniao(
        #         conjuge_id1=dados_validados.conjuge_id1,
        #         conjuge_id2=dados_validados.conjuge_id2,
        #         dia_casamento=dados_validados.dia_casamento,
        #         mes_casamento=dados_validados.mes_casamento,
        #         ano_casamento=dados_validados.ano_casamento,
        #         local_id=dados_validados.local_casamento_id
        #     )
        #     uniao_repo=UniaoRepository(db)
        
        #     try:
        #         return (uniao_repo.create(novo))
        #         # novo=repo.create()
        #     except Exception:
        #         raise