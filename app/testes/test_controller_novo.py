"""
Testes para as novas funcionalidades do Controller:
- pesquisa_individuos_por_nome()
- cria_uniao_por_nomes()
- adiciona_filiacao()
"""

import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup do banco de dados de teste
TEST_DB = "sqlite:///:memory:"
engine = create_engine(TEST_DB, echo=False)
Session = sessionmaker(bind=engine)

# Imports após setup do banco
from app.models.base import Base
from app.models.enums import GenderEnum
from app.models.individuo import Individuo
from app.models.uniao import Uniao
from app.controllers.controller import Controller


@pytest.fixture
def setup_db():
    """Cria as tabelas e retorna a session factory"""
    Base.metadata.create_all(engine)
    yield Session
    Base.metadata.drop_all(engine)


@pytest.fixture
def controller(setup_db):
    """Instancia o Controller com a session de teste"""
    return Controller(setup_db)


@pytest.fixture
def individuos_teste(setup_db):
    """Cria indivíduos de teste no banco"""
    session = setup_db()
    
    ind1 = Individuo(nome="João", sobrenome="Silva", genero=GenderEnum.MALE)
    ind2 = Individuo(nome="Maria", sobrenome="Santos", genero=GenderEnum.FEMALE)
    ind3 = Individuo(nome="Pedro", sobrenome="Silva", genero=GenderEnum.MALE)
    
    session.add_all([ind1, ind2, ind3])
    session.commit()
    
    return {
        "joao": ind1,
        "maria": ind2,
        "pedro": ind3
    }


class TestPesquisaIndividuosPorNome:
    """Testes para pesquisa_individuos_por_nome()"""
    
    def test_pesquisa_por_nome_encontra_resultado(self, controller, individuos_teste):
        """Deve encontrar indivíduo por nome"""
        resultados = []
        mensagem = []
        success = []
        
        def on_pesquisa_finalizada(s, res, msg):
            success.append(s)
            resultados.extend(res)
            mensagem.append(msg)
        
        controller.pesquisaFinalizada.connect(on_pesquisa_finalizada)
        controller.pesquisa_individuos_por_nome("João")
        
        assert len(success) > 0
        assert success[0] is True
        assert len(resultados) > 0
        assert resultados[0]["nome_completo"] == "João Silva"
    
    def test_pesquisa_por_nome_parcial(self, controller, individuos_teste):
        """Deve encontrar por busca parcial"""
        resultados = []
        success = []
        
        def on_pesquisa_finalizada(s, res, msg):
            success.append(s)
            resultados.extend(res)
        
        controller.pesquisaFinalizada.connect(on_pesquisa_finalizada)
        controller.pesquisa_individuos_por_nome("Silva")  # sobrenome
        
        assert len(success) > 0
        assert success[0] is True
        assert len(resultados) == 2  # João Silva e Pedro Silva
    
    def test_pesquisa_por_nome_nao_encontrado(self, controller, individuos_teste):
        """Deve retornar erro se não encontrar"""
        success = []
        resultados = []
        
        def on_pesquisa_finalizada(s, res, msg):
            success.append(s)
            resultados.extend(res)
        
        controller.pesquisaFinalizada.connect(on_pesquisa_finalizada)
        controller.pesquisa_individuos_por_nome("Inexistente")
        
        assert len(success) > 0
        assert success[0] is False
        assert len(resultados) == 0
    
    def test_pesquisa_com_termo_vazio(self, controller, individuos_teste):
        """Deve rejeitar termo vazio"""
        success = []
        
        def on_pesquisa_finalizada(s, res, msg):
            success.append(s)
        
        controller.pesquisaFinalizada.connect(on_pesquisa_finalizada)
        controller.pesquisa_individuos_por_nome("")
        
        assert len(success) > 0
        assert success[0] is False


class TestCriaUniaoPorNomes:
    """Testes para cria_uniao_por_nomes()"""
    
    def test_cria_uniao_com_nomes_exatos(self, controller, individuos_teste):
        """Deve criar union quando encontra exatamente um de cada cônjuge"""
        sucesso = []
        mensagem = []
        
        def on_uniao_finalizada(s, msg):
            sucesso.append(s)
            mensagem.append(msg)
        
        controller.uniaoFinalizada.connect(on_uniao_finalizada)
        controller.cria_uniao_por_nomes("João Silva", "Maria Santos", "15", "6", "1990", "")
        
        assert len(sucesso) > 0
        assert sucesso[0] is True
        assert "União registrada" in mensagem[0]
    
    def test_cria_uniao_primeiro_conjuge_nao_encontrado(self, controller, individuos_teste):
        """Deve falhar se primeiro cônjuge não existe"""
        sucesso = []
        
        def on_uniao_finalizada(s, msg):
            sucesso.append(s)
        
        controller.uniaoFinalizada.connect(on_uniao_finalizada)
        controller.cria_uniao_por_nomes("Inexistente", "Maria Santos", "15", "6", "1990", "")
        
        assert len(sucesso) > 0
        assert sucesso[0] is False
    
    def test_cria_uniao_multiplos_resultados(self, controller, individuos_teste):
        """Deve falhar se encontra múltiplos resultados para um cônjuge"""
        sucesso = []
        
        def on_uniao_finalizada(s, msg):
            sucesso.append(s)
        
        controller.uniaoFinalizada.connect(on_uniao_finalizada)
        # "Silva" coincide com João Silva e Pedro Silva
        controller.cria_uniao_por_nomes("Silva", "Maria Santos", "15", "6", "1990", "")
        
        assert len(sucesso) > 0
        assert sucesso[0] is False
        assert "Múltiplos" in sucesso[0] or "múltiplos" in sucesso[0]
    
    def test_cria_uniao_nomes_obrigatorios(self, controller, individuos_teste):
        """Deve rejeitar se algum nome está vazio"""
        sucesso = []
        
        def on_uniao_finalizada(s, msg):
            sucesso.append(s)
        
        controller.uniaoFinalizada.connect(on_uniao_finalizada)
        controller.cria_uniao_por_nomes("", "Maria Santos", "15", "6", "1990", "")
        
        assert len(sucesso) > 0
        assert sucesso[0] is False


class TestAdicionaFiliacao:
    """Testes para adiciona_filiacao()"""
    
    def test_adiciona_filiacao_com_filho_valido(self, controller, individuos_teste):
        """Deve vincular filho a uma União"""
        session = Session()
        
        # Cria uma União primeiro
        joao = session.query(Individuo).filter_by(nome="João").first()
        maria = session.query(Individuo).filter_by(nome="Maria").first()
        
        uniao = Uniao(
            conjuge_id1=joao.id,
            conjuge_id2=maria.id,
            dia_casamento=15,
            mes_casamento=6,
            ano_casamento=1990
        )
        session.add(uniao)
        session.commit()
        uniao_id = uniao.id
        session.close()
        
        # Agora adiciona a filiação
        sucesso = []
        mensagem = []
        
        def on_filiacao_finalizada(s, msg):
            sucesso.append(s)
            mensagem.append(msg)
        
        controller.filiacaoFinalizada.connect(on_filiacao_finalizada)
        controller.adiciona_filiacao("Pedro Silva", uniao_id)
        
        assert len(sucesso) > 0
        assert sucesso[0] is True
        assert "Filiação registrada" in mensagem[0]
        
        # Verifica se foi salvo no banco
        session = Session()
        pedro = session.query(Individuo).filter_by(nome="Pedro").first()
        assert pedro.id_uniao_pais == uniao_id
        session.close()
    
    def test_adiciona_filiacao_filho_nao_encontrado(self, controller, individuos_teste):
        """Deve falhar se filho não existe"""
        session = Session()
        joao = session.query(Individuo).filter_by(nome="João").first()
        maria = session.query(Individuo).filter_by(nome="Maria").first()
        
        uniao = Uniao(
            conjuge_id1=joao.id,
            conjuge_id2=maria.id
        )
        session.add(uniao)
        session.commit()
        uniao_id = uniao.id
        session.close()
        
        sucesso = []
        
        def on_filiacao_finalizada(s, msg):
            sucesso.append(s)
        
        controller.filiacaoFinalizada.connect(on_filiacao_finalizada)
        controller.adiciona_filiacao("Inexistente", uniao_id)
        
        assert len(sucesso) > 0
        assert sucesso[0] is False
    
    def test_adiciona_filiacao_uniao_nao_existe(self, controller, individuos_teste):
        """Deve falhar se União não existe"""
        sucesso = []
        
        def on_filiacao_finalizada(s, msg):
            sucesso.append(s)
        
        controller.filiacaoFinalizada.connect(on_filiacao_finalizada)
        controller.adiciona_filiacao("Pedro Silva", 9999)  # ID que não existe
        
        assert len(sucesso) > 0
        assert sucesso[0] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
