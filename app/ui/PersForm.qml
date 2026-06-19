import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "./components" as Components

Page {
    //title: "Cadastro"
    // dialogo p mostrar msg de err/sucess vindas do python
    Dialog {
        id: msgDialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok
        property alias texto: lblMsg.text
        Label { id: lblMsg; text: "" }
    }

    Connections {
        target: backendBridge
        function onCadastroFinalizado(sucesso, mensagem) {
            msgDialog.texto = mensagem
            msgDialog.open()
            if (sucesso) {
                inputName.text = ""
                inputSurname.text = ""
            }
        }
    }

    ColumnLayout{
        anchors.centerIn: parent
        spacing: 15
        width: 300
        // Label{
        //     text: "Dados do individuo"
        //     font.pixelSize: 18
        //     font.bold: true
        //     Layout.alignment: Qt.AlignCenter
        // }
        Components.Title {lbl: "Cadastro de indivíduo"}

        TextField{
            id: inputName
            placeholderText: "Primeiro nome"
            Layout.fillWidth: true
        }
        // Components.LbInputField{
        //     id: inputName
        //     txt: "Primeiro nome (obrigatório)"
        //     ph: "Digite o primeiro nome"
        //     Layout.fillWidth: true
        // }
        // Components.LbInputField{
        //     id: inputSurname
        //     txt: "Sobrenome (obrigatório)"
        //     ph: "Digite o sobrenome"
        //     Layout.fillWidth: true
        // }
        TextField {
            id: inputSurname
            placeholderText: "Sobrenome"
            Layout.fillWidth: true
        }
        
        ComboBox {
            id: combGen
            Layout.fillWidth: true
            model: [
                { text: "Masculino", value: "masculino" },
                { text: "Feminino", value: "feminino" },
                { text: "Não-binário", value: "nao-binario" },
                { text: "Outro", value: "outro" }]
                textRole: "text"
        }

        Button{
            text: "Salvar dados"
            Layout.alignment: Qt.AlignRight
            onClicked: {
                backendBridge.cria_individuo(
                    inputName.text,
                    inputSurname.text,
                    combGen.model[combGen.currentIndex].value
                )
            }
        }
    }

    Button{
        text: "<- voltar"
        onClicked: stack.pop()
    }
}