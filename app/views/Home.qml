import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "./components"

Page {
    //title: "Sistema de Pesquisa Genealógica"
    Rectangle {
        anchors.fill: parent
        color: "#f5f6fa"
        //Layout

        ColumnLayout {
            anchors.top: parent
            anchors.topMargin: 50

            
            width: 700
            spacing: 30
            // Text {
            //     text: "Pesquisa genealógica"
            //     //font.family: "Segoe UI"
            //     font.pixelSize: 24  // tamanho da fonte em pixels
            //     font.bold: true // peso da fonte: negrito
            //     color: "#1f2937"  // cor da fonte
            //     Layout.alignment: Qt.AlignHCenter 
            //     wrapMode: Text.WordWrap // quebra de linha automática
            //     elide: Text.ElideRight  // "..." quando não cabe
            // }
            Title { lbl: "Pesquise um antepassado" }

            GridLayout {
                columns: 2
                columnSpacing: 20
                rowSpacing: 16
                Layout.fillWidth: true

                Layout.alignment: Qt.AlignCenter

                // CORREÇÃO: Uso de ColumnLayout em vez de Column simples

                LbInputField {txt: "Nome"; ph: "Digite o primeiro nome"}

                LbInputField {txt: "Sobrenome"; ph: "Digite os sobrenomes"}

                LbInputField {txt: "Local de nascimento"; ph: "Digite o local"}

                LbInputField {txt: "Ano aproximado de nascimento"; ph: "Digite o ano. Ex.: 1890"}

                // ColumnLayout {
                //     Layout.fillWidth: true
                //     spacing: 6

                //     Text {
                //         text: "Sobrenome"
                //         font.pixelSize: 14
                //         font.bold: true
                //         color: "#374151"
                //     }

                //     TextField {
                //         id: surnameField
                //         Layout.fillWidth: true
                //         placeholderText: "Digite o sobrenome"
                //     }
                // }

                // ColumnLayout {
                //     Layout.fillWidth: true
                //     spacing: 6

                //     Text {
                //         text: "Local"
                //         font.pixelSize: 14
                //         font.bold: true
                //         color: "#374151"
                //     }

                //     TextField {
                //         id: locationField
                //         Layout.fillWidth: true
                //         placeholderText: "Digite a localidade"
                //     }
                // }

                // ColumnLayout {
                //     Layout.fillWidth: true
                //     spacing: 6

                //     Text {
                //         text: "Ano aproximado de nascimento"
                //         font.pixelSize: 14
                //         font.bold: true
                //         color: "#374151"
                //     }

                //     TextField {
                //         id: birthYearField
                //         Layout.fillWidth: true
                //         placeholderText: "Ex.: 1890"
                //     }
                // }
            }

            Button {
                text: "Buscar"
                Layout.alignment: Qt.AlignHCenter
                // Ajustado para usar Layout.preferredWidth em vez de width estático dentro de um layout
                Layout.preferredWidth: 180 

                onClicked: {
                    console.log("Buscar:")
                    console.log("Nome:", firstNameField.text)
                    console.log("Sobrenome:", surnameField.text)
                    console.log("Local:", locationField.text)
                    console.log("Ano:", birthYearField.text)
                }
            }

            Button {
                text: "Cadastrar Pessoa"
                onClicked: { stack.push("PersForm.qml") }
            }

            Button {
                text: "Cadastrar União"
                onClicked: { stack.push("UniaoForm.qml") }
            }

        }
    }
}
