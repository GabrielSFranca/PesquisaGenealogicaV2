import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    
    QQuickStyle.setStyle("Material")
    
    FILE="QtQuickWiki.qml"
    engine.load(FILE)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# import sys
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtQml import QQmlApplicationEngine

# from PySide6.QtQuickControls2 import QQuickStyle

# if __name__ == "__main__":
    
#     # QGuiApplication= essencial p apps QT QUICK/QML; inicia a aplicacao visual
#     app = QGuiApplication(sys.argv)
    
#     QQuickStyle.setStyle("Universal")
    
#     # motor responsavel por carregar o arquivo QML
#     QML_FILE="novo.qml"
#     engine = QQmlApplicationEngine()
#     engine.load(QML_FILE)
    
#     # verificacao se o arq foi carregado c sucesso
#     if not engine.rootObjects():
#         sys.exit(-1)
        
#     # mantem o app rodando em loop
#     sys.exit(app.exec())


# import sys
# from PySide6.QtWidgets import QApplication
# from app.database.db import init_db, SessionLocal
# from app.controllers.individuo_controller import IndividuoController
# from app.views.cadastro_indi_vw import CadastroIndiVw

# def main():
#     # 1. Inicializa o Banco de Dados (cria tabelas)
#     # Substitui a lógica de main_gabr.py
#     print("Inicializando banco de dados...")
#     init_db()
    
#     # 2. Prepara a infraestrutura do Controller
#     # Passamos a fábrica de sessões (SessionLocal) para o controlador
#     # conforme definido no seu individuo_controller.py
#     controller = IndividuoController(SessionLocal)
    
#     # 3. Inicia a aplicação GUI (PySide6)
#     # Lógica extraída e limpa do seu script.py
#     app = QApplication(sys.argv)
    
#     # 4. Instancia a View passando o Controller (Injeção de Dependência)
#     janela = CadastroIndiVw(controller)
#     janela.show()
    
#     # 5. Loop principal
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()