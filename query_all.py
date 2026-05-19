from app.database.db import init_db, Session
# from app.models.individuo import Individuo
from app.models.tables import Individuo
session=Session()
# script com funcao para consulta de todos: buscar e exibir
def consulta_pessoa():
    print("\n--- Lista de Pessoas Cadastradas ---")
    # Executa a query equivalente a: SELECT * FROM individuo;
    individuos=session.query(Individuo).all()

    if not individuos:
        print("Nenhuma pessoa encontrada no banco de dados.")
        return
    # Itera sobre os resultados e imprime no terminal
    for i in individuos:
        # print(i)
        print(f"[{i.id}] Nome: {i.nome} {i.sobrenome}, {i.genero}")
        #print(f"ID: {i.id} | Nome: {i.nome} | Gen: {i.genero0} | Vivo? {i.vivo} | ")
        
    print("-" * 36 + "\n")

if __name__ == "__main__":
    init_db()
    try:
        consulta_pessoa()
    except Exception as e:
        print(f"Erro ao conectar ou consultar o banco de dados:\n{e}")
    finally:
        # É uma boa prática fechar a sessão ao terminar
        session.close()
        
    
# 1. Configuração da Conexão
# Substitua 'usuario', 'senha' e 'nome_do_banco' pelos seus dados reais.
# A porta 5434 está configurada diretamente na string de conexão.
# DATABASE_URL = "postgresql://usuario:senha@localhost:5434/nome_do_banco"

# # O echo=False evita que o SQLAlchemy imprima todo o SQL gerado no terminal
# engine = create_engine(DATABASE_URL, echo=False)
# Base = declarative_base()

# # 2. Mapeamento da Tabela (Model)
# class Individuo(Base):
#     __tablename__ = 'individuo' # Ajuste para o nome exato da sua tabela (ex: 'person')

#     # Mapeie as colunas de acordo com o seu banco de dados
#     id_individuo = Column('id', Integer, primary_key=True) 
#     nome_completo = Column('nome', String)
#     sexo = Column('sexo', String)

# # 3. Configuração da Sessão
# Session = sessionmaker(bind=engine)
# session = Session()

