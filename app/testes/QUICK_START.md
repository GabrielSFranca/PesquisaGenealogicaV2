# ⚡ Quick Start - União e Filiação

## 🚀 Em 5 Minutos

### 1. Entender o que foi criado
```
3 novos métodos no Controller:
- pesquisa_individuos_por_nome("João")      → retorna lista com ID e nome
- cria_uniao_por_nomes("João", "Maria", ...)  → cria casamento
- adiciona_filiacao("Pedro", 1)              → vincula filho à União
```

### 2. Ver em ação (Python)
```python
from app.controllers.controller import Controller
from sqlalchemy.orm import sessionmaker

# Criar controller
controller = Controller(SessionMaker)

# Conectar ao signal
def on_pesquisa(success, results, msg):
    print(f"{msg}: {results}")

controller.pesquisaFinalizada.connect(on_pesquisa)

# Pesquisar
controller.pesquisa_individuos_por_nome("João")
# Saída: "1 resultado(s) encontrado(s): [{'id': 1, 'nome_completo': 'João Silva', 'genero': 'M'}]"
```

### 3. Usar em QML
```qml
// Pesquisar
backendBridge.pesquisa_individuos("João")

// Criar União
backendBridge.cria_uniao_por_nomes("João Silva", "Maria Santos", "15", "6", "1990", "")

// Adicionar Filho
backendBridge.adiciona_filiacao("Pedro Silva", 1)

// Conectar signals
Connections {
    target: backendBridge
    function onPesquisaFinalizada(success, results, message) {
        console.log(message)
    }
    function onUniaoFinalizada(success, message) {
        console.log(message)
    }
    function onFiliacaoFinalizada(success, message) {
        console.log(message)
    }
}
```

### 4. Copiar UI exemplo
```bash
# Abra: EXEMPLO_QML_NOVO.qml
# Copie o código para seu arquivo QML
# Adapte os nomes de campos conforme necessário
```

---

## 📖 Para Saber Mais

| Necessidade | Arquivo |
|-------------|---------|
| Entender tudo | `GUIA_COMPLETO.md` |
| API técnica | `NOVO_CONTROLLER_DOCS.md` |
| Código QML | `EXEMPLO_QML_NOVO.qml` |
| Testes | `test_controller_novo.py` |
| Índice | `INDEX_NOVO_FEATURES.md` |

---

## 🧪 Testar Tudo

```bash
pytest test_controller_novo.py -v
```

Resultado esperado: ✅ **10+ testes passando**

---

## ✨ Pronto!

Seus 3 novos métodos estão:
- ✅ Implementados
- ✅ Testados
- ✅ Documentados
- ✅ Prontos para usar

Basta integrar no QML! 🎉
