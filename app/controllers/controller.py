from PySide6.QtCore import QObject, Slot, Signal
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, or_, and_

from app.controllers.schemas import IndividuoSchema
from app.repositories.uniao_repository import UniaoRepository
from app.repositories.individuo_repository import IndividuoRepository
from app.testes.tables import Individuo, Uniao

class Controller(QObject):
    cadastroFinalizado=Signal(bool, str)
    uniaoFinalizada=Signal(bool, str)
    filiacaoFinalizada=Signal(bool, str)
    pesquisaFinalizada=Signal(bool, list, str)  # success, results, message
    
    def __init__(self, ses_mkr: sessionmaker ):
        super().__init__()
        self.Session=ses_mkr
        self.uniao_service=UniaoRepository(ses_mkr)
        self.individuo_service=IndividuoRepository(ses_mkr)
    
    @Slot(str, str, str)
    def cria_individuo(self, nome, sobrenome, genero):
        try:
            dados_validados=IndividuoSchema(
                nome=nome,
                sobrenome=sobrenome,
                genero=genero
            )      
        except ValidationError as err:
            self.cadastroFinalizado.emit(False, f"err de validacao: \n{err.errors()[0]['msg']}")
            return 

        gen_enum=dados_validados.genero

        with self.Session() as session:
            try:
                novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=gen_enum
                )
                session.add(novo_indi)
                session.commit()
                session.refresh(novo_indi)
                
                self.cadastroFinalizado.emit(True, f"Imigrante pioneiro {novo_indi.nome_completo()} registrado!")
                
            except SQLAlchemyError as err_db:
                session.rollback()
                self.cadastroFinalizado.emit(False, "erro ao gravar na database")
                raise Exception(f"Erro na base de dados: {str(err_db)}")
            
    

    @staticmethod
    def _parse_required_int(valor: str, campo: str) -> int:
        valor_limpo = valor.strip()
        if not valor_limpo:
            raise ValueError(f"{campo} é obrigatório.")
        try:
            return int(valor_limpo)
        except ValueError:
            raise ValueError(f"{campo} deve ser um número inteiro.")

    @staticmethod
    def _parse_optional_int(valor: str, campo: str):
        valor_limpo = valor.strip()
        if not valor_limpo:
            return None
        try:
            return int(valor_limpo)
        except ValueError:
            raise ValueError(f"{campo} deve ser um número inteiro.")

    @Slot(str, str, str, str, str, str)
    def cria_uniao(self, conjuge_id1, conjuge_id2, dia_casamento, mes_casamento, ano_casamento, local_id):
        try:
            dados_entrada = {
                "conjuge_id1": self._parse_required_int(conjuge_id1, "ID do cônjuge 1"),
                "conjuge_id2": self._parse_required_int(conjuge_id2, "ID do cônjuge 2"),
                "dia_casamento": self._parse_optional_int(dia_casamento, "Dia do casamento"),
                "mes_casamento": self._parse_optional_int(mes_casamento, "Mês do casamento"),
                "ano_casamento": self._parse_optional_int(ano_casamento, "Ano do casamento"),
                "local_id": self._parse_optional_int(local_id, "ID do local"),
            }

            nova_uniao = self.uniao_service.criar_uniao(dados_entrada)
            self.uniaoFinalizada.emit(
                True,
                f"União registrada entre os indivíduos {nova_uniao.conjuge_id1} e {nova_uniao.conjuge_id2}.",
            )
        except ValueError as err:
            self.uniaoFinalizada.emit(False, str(err))
        except Exception as err:
            self.uniaoFinalizada.emit(False, f"Erro ao criar união: {str(err)}")
    
    
    @Slot(str)
    def pesquisa_individuos_por_nome(self, termo_busca: str):
        """
        Pesquisa Individuos no banco de dados por nome completo (nome + sobrenome).
        Emite pesquisaFinalizada com lista de resultados encontrados.
        """
        try:
            termo_limpo = termo_busca.strip()
            if not termo_limpo:
                self.pesquisaFinalizada.emit(False, [], "Digite um termo de busca")
                return
            
            resultados = self.individuo_service.buscar_por_nome(termo_limpo)
            
            if not resultados:
                self.pesquisaFinalizada.emit(False, [], f"Nenhum indivíduo encontrado com '{termo_busca}'")
            else:
                # Converte para formato amigável para UI
                resultados_dict = [
                    {
                        "id": ind.id,
                        "nome_completo": ind.nome_completo(),
                        "genero": str(ind.genero.value)
                    }
                    for ind in resultados
                ]
                self.pesquisaFinalizada.emit(True, resultados_dict, f"{len(resultados)} resultado(s) encontrado(s)")
        except Exception as err:
            self.pesquisaFinalizada.emit(False, [], f"Erro na pesquisa: {str(err)}")
    
    
    @Slot(str, str, str, str, str, str)
    def cria_uniao_por_nomes(self, nome_conjuge1: str, nome_conjuge2: str, dia_casamento: str, mes_casamento: str, ano_casamento: str, local_id: str):
        """
        Cria uma União pesquisando os cônjuges pelo nome completo.
        O fluxo é:
        1. Pesquisa o primeiro cônjuge por nome
        2. Pesquisa o segundo cônjuge por nome
        3. Se encontrar exatamente um de cada, cria a União
        """
        try:
            nome1_limpo = nome_conjuge1.strip()
            nome2_limpo = nome_conjuge2.strip()
            
            if not nome1_limpo or not nome2_limpo:
                self.uniaoFinalizada.emit(False, "Ambos os nomes dos cônjuges são obrigatórios")
                return
            
            # Pesquisa os dois cônjuges
            with self.Session() as session:
                resultados1 = session.query(Individuo).filter(
                    or_(
                        Individuo.nome.ilike(f"%{nome1_limpo}%"),
                        (Individuo.nome + ' ' + Individuo.sobrenome).ilike(f"%{nome1_limpo}%")
                    )
                ).all()
                
                resultados2 = session.query(Individuo).filter(
                    or_(
                        Individuo.nome.ilike(f"%{nome2_limpo}%"),
                        (Individuo.nome + ' ' + Individuo.sobrenome).ilike(f"%{nome2_limpo}%")
                    )
                ).all()
            
            # Valida se encontrou exatamente um de cada
            if len(resultados1) == 0:
                self.uniaoFinalizada.emit(False, f"Nenhum cônjuge encontrado com o nome '{nome_conjuge1}'")
                return
            
            if len(resultados1) > 1:
                nomes = ", ".join([ind.nome_completo() for ind in resultados1])
                self.uniaoFinalizada.emit(False, f"Múltiplos indivíduos encontrados para '{nome_conjuge1}': {nomes}. Seja mais específico.")
                return
            
            if len(resultados2) == 0:
                self.uniaoFinalizada.emit(False, f"Nenhum cônjuge encontrado com o nome '{nome_conjuge2}'")
                return
            
            if len(resultados2) > 1:
                nomes = ", ".join([ind.nome_completo() for ind in resultados2])
                self.uniaoFinalizada.emit(False, f"Múltiplos indivíduos encontrados para '{nome_conjuge2}': {nomes}. Seja mais específico.")
                return
            
            # Obtém os IDs dos cônjuges
            conjuge_id1 = str(resultados1[0].id)
            conjuge_id2 = str(resultados2[0].id)
            
            # Chama o método existente para criar a União
            self.cria_uniao(conjuge_id1, conjuge_id2, dia_casamento, mes_casamento, ano_casamento, local_id)
            
        except Exception as err:
            self.uniaoFinalizada.emit(False, f"Erro ao criar união por nomes: {str(err)}")
    
    
    @Slot(str, int)
    def adiciona_filiacao(self, nome_filho: str, id_uniao: int):
        """
        Adiciona um filho a uma União (Filiação).
        O fluxo é:
        1. Pesquisa o filho pelo nome no banco
        2. Se encontrar exatamente um, vincula-o à União
        
        Args:
            nome_filho: Nome do filho para buscar
            id_uniao: ID da União (pais)
        """
        try:
            nome_limpo = nome_filho.strip()
            if not nome_limpo:
                self.filiacaoFinalizada.emit(False, "Nome do filho é obrigatório")
                return
            
            with self.Session() as session:
                # Pesquisa o filho
                resultados = session.query(Individuo).filter(
                    or_(
                        Individuo.nome.ilike(f"%{nome_limpo}%"),
                        (Individuo.nome + ' ' + Individuo.sobrenome).ilike(f"%{nome_limpo}%")
                    )
                ).all()
                
                # Valida a pesquisa
                if len(resultados) == 0:
                    self.filiacaoFinalizada.emit(False, f"Nenhum indivíduo encontrado com o nome '{nome_filho}'")
                    return
                
                if len(resultados) > 1:
                    nomes = ", ".join([ind.nome_completo() for ind in resultados])
                    self.filiacaoFinalizada.emit(False, f"Múltiplos indivíduos encontrados: {nomes}. Seja mais específico.")
                    return
                
                # Verifica se a União existe
                uniao = session.query(Uniao).filter(Uniao.id == id_uniao).first()
                if not uniao:
                    self.filiacaoFinalizada.emit(False, f"União com ID {id_uniao} não encontrada")
                    return
                
                # Obtém o filho
                filho = resultados[0]
                
                # Verifica se já está vinculado
                if filho.id_uniao_pais is not None:
                    self.filiacaoFinalizada.emit(False, f"{filho.nome_completo()} já possui pais vinculados (Uniao ID: {filho.id_uniao_pais})")
                    return
                
                # Adiciona o vínculo
                filho.id_uniao_pais = id_uniao
                session.add(filho)
                session.commit()
                session.refresh(filho)
                
                self.filiacaoFinalizada.emit(
                    True,
                    f"Filiação registrada: {filho.nome_completo()} vinculado à União (ID: {id_uniao})"
                )
                
        except SQLAlchemyError as err_db:
            self.filiacaoFinalizada.emit(False, f"Erro ao registrar filiação na base de dados: {str(err_db)}")
        except Exception as err:
            self.filiacaoFinalizada.emit(False, f"Erro ao adicionar filiação: {str(err)}")
