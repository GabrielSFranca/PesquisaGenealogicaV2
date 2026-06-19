import QtQuick
import QtQuick.Controls

// container principal da aplicacao
ApplicationWindow {
    visible: true
    width: 1200 // largura
    height: 700 // altura maxima da resolucao hd
    title: "Sistema de Pesquisa Genealógica"

    // 1. Menu de Opções
    menuBar: MenuBar {
        Menu {
            title: "Início"
            MenuItem { text: "Importar Dados" }
            MenuItem { text: "Configurações" }
            MenuItem { text: "Sair" }
        }

        Menu {
            title: "Cadastrar"
            MenuItem { text: "Importar Dados" }
            MenuItem { text: "Configurações" }
            MenuItem { text: "Sair" }
        }

        Menu {
            title: "Usuário"
            MenuItem { text: "Importar Dados" }
            MenuItem { text: "Configurações" }
            MenuItem { text: "Sair" }
        }


        Menu {
            title: "Configurações"
            MenuItem { text: "Importar Dados" }
            MenuItem { text: "Configurações" }
            MenuItem { text: "Sair" }
        }
    }

    StackView {
        id: stack
        anchors.fill: parent
        initialItem: Home {}
    }
}



// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Window 2.15

// ApplicationWindow {
//     id: root
//     visible: true
//     width: 480
//     height: 320
//     title: "Meu Primeiro App QML"
//     color: "#1a1e29"


//     Column{
//         id: coluna
//         anchors.centerIn: parent
//         spacing: 16

//         Text{
//             id: lbl
//             text: "Text"
//             color: '#d8d8d8'
//             font.family: "Segoe UI"
//             font.pixelSize: 16
//             font.weight: Font.Bold
//             wrapMode: Text.WordWrap
//             elide: Text.ElideRight
//             anchors.horizontalCenter: parent.horizontalCenter
//         }
//         TextField{
//             id: campo
//             placeholderText: "Digite seu nome"
//             width: 280
//             font.pixelSize: 20
            
//             onTextChanged: console.log("Texto", text)
//             onAccepted: console.log("enter presssionado")
//         }

//     }



    // Rectangle {
    //     anchors.fill: parent
    //     color: "#1a1e29"

    //     Column {
    //         anchors.centerIn: parent
    //         spacing: 16

    //         Text {
    //             text: "Olá, PySide6 + QML! 🚀"
    //             color: "white"
    //             font.pixelSize: 24
    //             anchors.horizontalCenter: parent.horizontalCenter
    //         }

    //         Button {
    //             text: "Clique aqui"
    //             anchors.horizontalCenter: parent.horizontalCenter
    //             onClicked: console.log("Clicado!")
    //         }
    //     }
    // }