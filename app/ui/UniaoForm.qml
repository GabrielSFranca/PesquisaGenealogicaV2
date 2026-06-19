import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "./components" as Components

Page {
    Dialog {
        id: msgDialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok
        property alias texto: lblMsg.text
        Label { id: lblMsg; text: "" }
    }

    Connections {
        target: backendBridge
        function onUniaoFinalizada(sucesso, mensagem) {
            msgDialog.texto = mensagem
            msgDialog.open()
            if (sucesso) {
                inputConjuge1.text = ""
                inputConjuge2.text = ""
                inputDia.text = ""
                inputMes.text = ""
                inputAno.text = ""
                inputLocalId.text = ""
            }
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 12
        width: 360

        Components.Title { lbl: "Cadastro de união" }

        TextField {
            id: inputConjuge1
            Layout.fillWidth: true
            placeholderText: "ID do cônjuge 1 (obrigatório)"
        }
 
        TextField {
            id: inputConjuge2
            Layout.fillWidth: true
            placeholderText: "ID do cônjuge 2 (obrigatório)"
        }

        TextField {
            id: inputDia
            Layout.fillWidth: true
            placeholderText: "Dia do casamento (opcional)"
        }

        TextField {
            id: inputMes
            Layout.fillWidth: true
            placeholderText: "Mês do casamento (opcional)"
        }

        TextField {
            id: inputAno
            Layout.fillWidth: true
            placeholderText: "Ano do casamento (opcional)"
        }

        TextField {
            id: inputLocalId
            Layout.fillWidth: true
            placeholderText: "ID do local (opcional)"
        }

        Button {
            text: "Salvar união"
            Layout.alignment: Qt.AlignRight
            onClicked: {
                backendBridge.cria_uniao(
                    inputConjuge1.text,
                    inputConjuge2.text,
                    inputDia.text,
                    inputMes.text,
                    inputAno.text,
                    inputLocalId.text
                )
            }
        }
    }

    Button {
        text: "<- voltar"
        onClicked: stack.pop()
    }
}
