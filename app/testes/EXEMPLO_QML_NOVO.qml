/**
 * EXEMPLO DE USO EM QML - Novas Funcionalidades do Controller
 * 
 * Este arquivo demonstra como integrar as novas funcionalidades
 * (pesquisa, criação de União e Filiação) em uma interface QML.
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    width: 1000
    height: 700
    color: "#f5f5f5"

    // ====== PESQUISA DE INDIVÍDUOS ======
    GroupBox {
        id: pesquisaBox
        title: "1. Pesquisar Indivíduos"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        height: 150

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10

            TextField {
                id: termoBusca
                placeholderText: "Digite nome ou sobrenome..."
                Layout.fillWidth: true
            }

            Button {
                text: "Pesquisar"
                Layout.alignment: Qt.AlignRight
                onClicked: {
                    backendBridge.pesquisa_individuos_por_nome(termoBusca.text)
                }
            }

            Text {
                id: resultadoPesquisa
                text: "Aguardando pesquisa..."
                Layout.fillWidth: true
                wrapMode: Text.Wrap
                color: "#666"
            }
        }
    }

    // ====== LISTA DE RESULTADOS ======
    GroupBox {
        id: listaResultados
        title: "Resultados"
        anchors.top: pesquisaBox.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        height: 180

        ListView {
            id: resultadosList
            anchors.fill: parent
            anchors.margins: 10

            model: ListModel { id: resultadosModel }

            delegate: Rectangle {
                width: resultadosList.width - 20
                height: 40
                color: "#e0e0e0"
                radius: 4
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.margins: 5

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 20

                    Text {
                        text: model.id + ": " + model.nome_completo + " (" + model.genero + ")"
                        Layout.fillWidth: true
                    }

                    Button {
                        text: "Selecionar"
                        onClicked: {
                            console.log("Selecionado: " + model.id + " - " + model.nome_completo)
                            // Armazena para criar União ou Filiação
                            if (!window.conjuge1_selecionado) {
                                window.conjuge1_selecionado = {
                                    id: model.id,
                                    nome: model.nome_completo
                                }
                                conjuge1Label.text = "Cônjuge 1: " + model.nome_completo
                            } else if (!window.conjuge2_selecionado) {
                                window.conjuge2_selecionado = {
                                    id: model.id,
                                    nome: model.nome_completo
                                }
                                conjuge2Label.text = "Cônjuge 2: " + model.nome_completo
                            }
                        }
                    }
                }
            }
        }
    }

    // ====== CRIAR UNIÃO ======
    GroupBox {
        id: criar_uniao_box
        title: "2. Criar União (por nomes)"
        anchors.top: listaResultados.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        height: 250

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 10

            Text {
                text: "Preencha os cônjuges ou selecione da pesquisa acima"
                color: "#666"
                font.italic: true
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                TextField {
                    id: conjuge1Field
                    placeholderText: "Nome do Cônjuge 1"
                    Layout.fillWidth: true
                }

                TextField {
                    id: conjuge2Field
                    placeholderText: "Nome do Cônjuge 2"
                    Layout.fillWidth: true
                }
            }

            Text {
                id: conjuge1Label
                text: "Cônjuge 1: (nenhum selecionado)"
                color: "#666"
            }

            Text {
                id: conjuge2Label
                text: "Cônjuge 2: (nenhum selecionado)"
                color: "#666"
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                TextField {
                    id: dia_casamento
                    placeholderText: "Dia (1-31)"
                    inputMethodHints: Qt.ImhDigitsOnly
                    Layout.preferredWidth: 100
                }

                TextField {
                    id: mes_casamento
                    placeholderText: "Mês (1-12)"
                    inputMethodHints: Qt.ImhDigitsOnly
                    Layout.preferredWidth: 100
                }

                TextField {
                    id: ano_casamento
                    placeholderText: "Ano"
                    inputMethodHints: Qt.ImhDigitsOnly
                    Layout.preferredWidth: 100
                }

                TextField {
                    id: local_id
                    placeholderText: "ID Local (opt.)"
                    inputMethodHints: Qt.ImhDigitsOnly
                    Layout.fillWidth: true
                }
            }

            Button {
                text: "Criar União"
                Layout.alignment: Qt.AlignRight
                onClicked: {
                    let nome1 = conjuge1Field.text || window.conjuge1_selecionado?.nome || ""
                    let nome2 = conjuge2Field.text || window.conjuge2_selecionado?.nome || ""

                    backendBridge.cria_uniao_por_nomes(
                        nome1,
                        nome2,
                        dia_casamento.text,
                        mes_casamento.text,
                        ano_casamento.text,
                        local_id.text
                    )

                    // Limpar seleção
                    window.conjuge1_selecionado = null
                    window.conjuge2_selecionado = null
                }
            }

            Text {
                id: uniao_resultado
                text: "..."
                Layout.fillWidth: true
                wrapMode: Text.Wrap
                color: "#666"
            }
        }
    }

    // ====== ADICIONAR FILIAÇÃO ======
    GroupBox {
        id: filiacao_box
        title: "3. Adicionar Filiação (filho da União)"
        anchors.top: criar_uniao_box.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
        anchors.bottom: parent.bottom

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 10

            TextField {
                id: nome_filho
                placeholderText: "Nome do filho para buscar"
                Layout.fillWidth: true
            }

            TextField {
                id: uniao_id
                placeholderText: "ID da União (pais)"
                inputMethodHints: Qt.ImhDigitsOnly
                Layout.fillWidth: true
            }

            Button {
                text: "Adicionar Filiação"
                Layout.alignment: Qt.AlignRight
                onClicked: {
                    backendBridge.adiciona_filiacao(
                        nome_filho.text,
                        parseInt(uniao_id.text) || 0
                    )
                }
            }

            Text {
                id: filiacao_resultado
                text: "..."
                Layout.fillWidth: true
                wrapMode: Text.Wrap
                color: "#666"
            }
        }
    }

    // ====== CONNECTIONS (Sinais do Backend) ======
    Connections {
        target: backendBridge

        function onPesquisaFinalizada(success, results, message) {
            console.log("Pesquisa finalizada:", success, message)
            resultadoPesquisa.text = message

            resultadosModel.clear()
            if (success) {
                for (let result of results) {
                    resultadosModel.append({
                        id: result.id,
                        nome_completo: result.nome_completo,
                        genero: result.genero
                    })
                }
            }
        }

        function onUniaoFinalizada(success, message) {
            console.log("União finalizada:", success, message)
            uniao_resultado.text = message
            uniao_resultado.color = success ? "#008000" : "#cc0000"

            if (success) {
                // Limpar formulário
                conjuge1Field.text = ""
                conjuge2Field.text = ""
                dia_casamento.text = ""
                mes_casamento.text = ""
                ano_casamento.text = ""
                local_id.text = ""
            }
        }

        function onFiliacaoFinalizada(success, message) {
            console.log("Filiação finalizada:", success, message)
            filiacao_resultado.text = message
            filiacao_resultado.color = success ? "#008000" : "#cc0000"

            if (success) {
                // Limpar formulário
                nome_filho.text = ""
                uniao_id.text = ""
            }
        }
    }

    // ====== Variáveis globais ======
    QtObject {
        id: window
        property var conjuge1_selecionado: null
        property var conjuge2_selecionado: null
    }
}

/**
 * ====== FLUXO DE USO ======
 * 
 * 1. PESQUISAR:
 *    - Digite um termo de busca
 *    - Clique "Pesquisar"
 *    - Resultados aparecem na lista
 *    - Pode clicar "Selecionar" para marcar cônjuges
 * 
 * 2. CRIAR UNIÃO:
 *    - Preencha os nomes dos cônjuges (ou selecione da pesquisa)
 *    - Preencha data do casamento (opcional)
 *    - Clique "Criar União"
 *    - Mensagem de sucesso/erro aparece
 * 
 * 3. ADICIONAR FILIAÇÃO:
 *    - Digite o nome do filho
 *    - Digite o ID da União (pais)
 *    - Clique "Adicionar Filiação"
 *    - Mensagem de sucesso/erro aparece
 * 
 * ====== VALIDAÇÕES AUTOMÁTICAS ======
 * 
 * - Se não encontrar filho: erro "Nenhum indivíduo encontrado"
 * - Se encontrar múltiplos: lista todos e pede mais especificidade
 * - Se União não existe: erro "União não encontrada"
 * - Se filho já tem pais: erro "Já possui pais vinculados"
 */
