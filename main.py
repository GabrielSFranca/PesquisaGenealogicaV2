import os
import sys
from app.models.database import init_db, SessionLocal
from app.controllers.controller import Controller
from app.controllers.app_bridge import AppBridge
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

if __name__ == "__main__":    
    print(" inicializando a base de dados.......")
    init_db()
    
    # QGuiApplication= essencial p apps QT QUICK/QML; inicia a aplicacao visual
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Universal")
    # motor responsavel por carregar o arquivo QML
    engine = QQmlApplicationEngine()
    # QML_FILE="Home.qml"
    # bridge = Controller(Session)
    bridge=AppBridge(SessionLocal)
    engine.rootContext().setContextProperty("backendBridge", bridge)
    # Carrega o arquivo da Interface Gráfica
    qml_file = os.path.join(os.path.dirname(__file__), "app/views/main.qml")
    engine.load(qml_file)
    
    # verificacao se o arq foi carregado c sucesso
    if not engine.rootObjects():
        sys.exit(-1)
        
    # mantem o app rodando em loop
    sys.exit(app.exec())
