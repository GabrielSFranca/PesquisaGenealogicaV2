from PySide6.QtCore import QObject, Signal, Slot
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.repositories.individuo_repository import IndividuoRepository
from app.controllers.schemas import IndividuoSchema, UniaoCreateSchema
from app.repositories.uniao_repository import UniaoRepository
from app.controllers.controller import Controller

class AppBridge(QObject):
    cadastroFinalizado = Signal(bool, str)
    uniaoFinalizada = Signal(bool, str)
    filiacaoFinalizada = Signal(bool, str)
    pesquisaFinalizada = Signal(bool, list, str)

    def __init__(self, DBSession: sessionmaker):
        super().__init__()
        self.indiv_serv = IndividuoRepository(DBSession)
        self.un_serv=UniaoRepository(DBSession)
        self.controller = Controller(DBSession)
        
        # Conectar signals do controller
        self.controller.pesquisaFinalizada.connect(self.pesquisaFinalizada.emit)
        self.controller.filiacaoFinalizada.connect(self.filiacaoFinalizada.emit)
        self.controller.uniaoFinalizada.connect(self.uniaoFinalizada.emit)

    def _erro_validacao_pt_br(self, err: ValidationError) -> str:
        partes = []
        for item in err.errors():
            campo = " -> ".join(str(parte) for parte in item["loc"])
            mensagem = item["msg"]

            if mensagem == "Field required":
                mensagem = "campo obrigatório"
            elif mensagem == "String should have at least 2 characters":
                mensagem = "deve ter pelo menos 2 caracteres"
            elif mensagem == "Input should be a valid enum":
                mensagem = "valor inválido"
            elif mensagem == "Input should be a valid string":
                mensagem = "deve ser uma string válida"

            partes.append(f"{campo}: {mensagem}")

        return "Erro de validação: " + "; ".join(partes)

    def _erro_banco_pt_br(self, err: Exception) -> str:
        if isinstance(err, IntegrityError):
            return "Erro de banco: esse dado já existe ou viola uma restrição de integridade."
        if isinstance(err, SQLAlchemyError):
            return "Erro na base de dados. Tente novamente mais tarde."
        return f"Erro ao salvar no banco: {str(err)}"

    @Slot(str, str, str)
    def cria_individuo(self, nome, sobrenome, genero):
        try:
            dados_validados = IndividuoSchema(
                nome=nome,
                sobrenome=sobrenome,
                genero=genero,
            )
        except ValidationError as err:
            self.cadastroFinalizado.emit(False, self._erro_validacao_pt_br(err))
            return

        try:
            novo_individuo = self.indiv_serv.create(dados_validados)
            self.cadastroFinalizado.emit(
                True,
                f"Indivíduo {novo_individuo.nome_completo()} registrado com sucesso!",
            )
        except IntegrityError as err:
            self.cadastroFinalizado.emit(False, self._erro_banco_pt_br(err))
        except SQLAlchemyError as err:
            self.cadastroFinalizado.emit(False, self._erro_banco_pt_br(err))
        except ValueError as err:
            self.cadastroFinalizado.emit(False, str(err))

    @Slot(result=list)
    def carregar_individuos(self):
        individuos = self.indiv_serv.get_all()

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
    
    
# @Slot(str, result='QVariantList')
#     def pesquisarIndividuos(self, termo: str) -> list:
#         # 1. Chama o serviço passando a string do QML
#         resultados = self.individuo_service.buscar_aproximada(termo)
        
#         # 2. Converte os objetos SQLAlchemy para dicionários padrão do Python
#         # O Qt consegue transformar isso nativamente em um modelo visual (ListView)
#         lista_retorno = []
#         for pessoa in resultados:
#             lista_retorno.append({
#                 "id": pessoa.id,
#                 "nome": pessoa.nome,
#                 "sexo": pessoa.sexo
#                 # Aqui você pode adicionar datas de nascimento no futuro para ajudar a diferenciar homônimos
#             })
            
#         return lista_retorno
    
    
    @Slot(str, str, str, str, str, str)
    def cria_uniao(self, conjuge_id1, conjuge_id2, dia, mes, ano, loc_id):

        if conjuge_id1==conjuge_id2:
            self.cadastroFinalizado.emit(False, "Pessoa nao pode casar consigo mesma")
            return
        try:
            dados_validados=UniaoCreateSchema(conjuge_id1, conjuge_id2, dia, mes, ano, loc_id)
        except ValidationError as err:
            self.cadastroFinalizado.emit(False, f"err de validacao: \n{err.errors()[0]['msg']}")
            return 
        
        try:
            nova_un=self.un_serv.adicionar(dados_validados)
            self.cadastroFinalizado.emit(
                True,
                f"União registrada entre os indivíduos {nova_un.conjuge_id1} + {nova_un.conjuge_id2}.",
            )
        except ValueError as err:
            self.cadastroFinalizado.emit(False, str(err))
        except Exception as err:
            self.cadastroFinalizado.emit(False, f"Erro ao criar união: {str(err)}")
    
    
    @Slot(str)
    def pesquisa_individuos(self, termo_busca: str):
        """Pesquisa indivíduos por nome (novo)"""
        self.controller.pesquisa_individuos_por_nome(termo_busca)
    
    
    @Slot(str, str, str, str, str, str)
    def cria_uniao_por_nomes(self, nome_conjuge1: str, nome_conjuge2: str,
                             dia_casamento: str = "", mes_casamento: str = "", 
                             ano_casamento: str = "", local_id: str = ""):
        """Cria união pesquisando cônjuges por nome (novo)"""
        self.controller.cria_uniao_por_nomes(
            nome_conjuge1, nome_conjuge2,
            dia_casamento, mes_casamento, ano_casamento, local_id
        )
    
    
    @Slot(str, int)
    def adiciona_filiacao(self, nome_filho: str, id_uniao: int):
        """Adiciona filho a uma união (novo)"""
        self.controller.adiciona_filiacao(nome_filho, id_uniao)    