from PySide6.QtCore import QObject, Slot, Signal
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.schemas import IndividuoSchema
# from app.models.enums import GenderEnum
from app.models.tables import Individuo

class Controller(QObject):
    cadastroFinalizado=Signal(bool, str)
    
    def __init__(self, ses_mkr: sessionmaker ):
        super().__init__()
        self.Session=ses_mkr
    
    @Slot(str, str, str)
    def cria_individuo(self, nome, sobrenome, genero):
        # 1-pydantic
        # recebe um dicionario
        # eventos=[] # cria uma lista vazia de eventos da pessoa
        try:
            # valida com o esquema do pydantic
            dados_validados=IndividuoSchema(
                nome=nome,
                sobrenome=sobrenome,
                genero=genero
            )      
            # dados_validados=IndividuoSchema(**dados_entrada) # ** serve para desencapsular dicionario
            # nascimento=EventSchema(**dados_entrada["nascimento"])
            # eventos.append(nascimento)
            # validar dados
        except ValidationError as err:
            # erro capturado pelo pydantic
            self.cadastroFinalizado.emit(False, f"err de validacao: \n{err.errors()[0]['msg']}")
            # raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")
            return 
        
        # 2. Conversão de Domínio (String para Enum do SQLAlchemy)
        # gen_map = {
        #     "masculino": GenderEnum.M,
        #     "feminino": GenderEnum.F,
        #     "nao-binario": GenderEnum.NB,
        #     "outro": GenderEnum.OTHER
        # }
        
        
        # gen_enum = gen_map[dados_validados.genero]
        # gen_enum = gen_map[dados_validados.genero]
        # gen_enum=GenderEnum(genero)
        
        gen_enum=dados_validados.genero
        
        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                # cria o individuo com seus dados pessoais
                novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=gen_enum
                )
                session.add(novo_indi)
                # session.flush() # garante que indi esta disponivel
                
                # for evento in eventos:
                #     novo_event=Evento(
                #         tag=EvenTagEnum.BIRT, # logica errada
                #         data=evento.data,
                #         local=evento.local.strip(),
                #         notas=evento.notas,
                #         indi_id=novo_indi.id
                #     )
                #     session.add(novo_event)

                # novo_indi.eventos.append(eventonascimento)
                session.commit()
                session.refresh(novo_indi)
                
                self.cadastroFinalizado.emit(True, f"Imigrante pioneiro {novo_indi.nome_completo()} registrado!")
                
            except SQLAlchemyError as err_db:
                session.rollback()
                self.cadastroFinalizado.emit(True, "erro ao gravar na database")
                raise Exception(f"Erro na base de dados: {str(err_db)}")
