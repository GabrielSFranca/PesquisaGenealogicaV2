from app.repositories.individuo_repository import IndividuoRepository
from app.models.individuo import Individuo, IndividuoCreateSchema
from pydantic import ValidationError

class IndividuoService:
    
    def __init__(self, DBSessionMaker):
        self.Session=DBSessionMaker
        self.repo=IndividuoRepository(DBSessionMaker=DBSessionMaker)
        
    def listar_todos(self):
        return
    
    def criar_indi2(self, nome, sobrenome, genero):
        # try:
        #     dados_validados=IndividuoCreateSchema(nome=nome, sobrenome=sobrenome, genero=genero)
        # except ValidationError:
        #     raise
        
        with self.Session() as db:
            try:
                dados_validados=IndividuoCreateSchema(nome=nome, sobrenome=sobrenome, genero=genero)
                
                novo=Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=dados_validados.genero
                )
                
                repo=IndividuoRepository(db)
                sucess, msg=repo.create(novo)
                return sucess, msg
                
            except ValidationError as v:
                return False, "validation error"
            
            except Exception:
                return False, "erro"
        
            # novo=Individuo(
            #     nome=dados_validados.nome,
            #     sobrenome=dados_validados.sobrenome,
            #     genero=dados_validados.genero
            # )
            # repo=IndividuoRepository(db)
        
            # try:
            #     return (repo.create(novo))
            #     # novo=repo.create()
            # except Exception:
            #     raise

    def criar(self, nome: str, sobrenome: str, genero) -> tuple[bool, str]:
        """
        Cria um novo indivíduo após validação de esquema.
        Retorna tupla (sucesso, mensagem).
        """
        # 1. Valida FORA da sessão (economiza recursos)
        try:
            dados_validados = IndividuoCreateSchema(
                nome=nome, 
                sobrenome=sobrenome, 
                genero=genero
            )
        except ValidationError as e:
            # Retorna erro de validação sem abrir sessão
            return False, f"Validação falhou: {e.errors()[0]['msg']}"
        
        # 2. Cria objeto com dados validados
        novo = Individuo(
            nome=dados_validados.nome,
            sobrenome=dados_validados.sobrenome,
            genero=dados_validados.genero
        )
        
        # 3. Delega persistência ao repositório
        return self.repo.create(novo)
        
        # with self.Session() as db:
        #     repo = IndividuoRepository(db)
        #     return repo.create(novo)
            
            