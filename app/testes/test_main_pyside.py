# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.database.db import init_db, Session
# import controller
from app.controllers.schemas import IndividuoController
# import view
from app.trash.cadastro_indi_vw import CadastroIndiVw

def main():
    # configura e inicia a base de dados/cria tabelas
    # 1. Configuração do Banco de Dados (PostgreSQL mapeado no .env)
    # Por enquanto usando SQLite para exemplificar o teste local
    print("Inicializando base de dados...")
    init_db()
    # passa a sessao para o controle
    controller=IndividuoController(Session)
    
    # inicia a Interface Gráfica de Usuário com PySide6
    app = QApplication(sys.argv)
    
    # Instancia a View passando o Controller (Injeção de Dependência)
    janela=CadastroIndiVw(controller)
    # mostra a janela
    janela.show()
    # loop principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # from app.db import Base
# from app.trash.tabelas import Base
# from app.trash.tabelas import Individuo
# from app.controllers.individuo_controller import IndividuoController
# from app.database.connection import engine
# from app.models.base import Base
# from app.controllers.genealogia_controller import GenealogiaController
# from app.views.main_window import MainWindow

# def main():
#     # 1. Garante que as tabelas existem
#     Base.metadata.create_all(engine)

#     # 2. Inicia o Controller
#     controller = GenealogiaController()
 
#     # 3. Inicia e roda a View passando o Controller
#     app = MainWindow(controller)
#     app.mainloop()

# if __name__ == "__main__":
#     main()

# from app.controllers.individuo_controller import IndividuoController
# from app.views.cadastro_view import CadastroView


# from PySide6.QtWidgets import QApplication
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models.base import Base
# # Importar os modelos é necessário para o create_all funcionar
# from app.models.individuo import Individuo 
# from app.models.evento import Evento

# from app.database.db import init_db

# if __name__ == "__main__":
#     init_db()
#     print("Banco criado com sucesso.")