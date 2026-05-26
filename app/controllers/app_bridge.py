from PySide6.QtCore import QObject, Signal, Slot
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.controllers.individuo_service import IndividuoService
from app.controllers.schemas import IndividuoSchema

class AppBridge(QObject):
    cadastroFinalizado = Signal(bool, str)

    def __init__(self, DBSession: sessionmaker):
        super().__init__()
        self.indiv_serv = IndividuoService(DBSession)

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
            novo_individuo = self.indiv_serv.adicionar(dados_validados)
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
        individuos = self.indiv_serv.listar_todos()

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

    