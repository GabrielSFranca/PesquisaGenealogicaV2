import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: root
    visible: true
    title: qsTr("Titulo da janela")
    width: 400
    height: 500


    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    Rectangle{
        id: topBar
        height: 40
        color: Material.color(Material.Blue)

        anchors{
            right: parent.right
            left: parent.left
            top: parent.top
        }

        radius: 10

        Label {
            text: qsTr("LOGIN PAGE")
        }

    }

}


// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Window 2.15

// // Janela pai da aplicacao
// ApplicationWindow {
//     visible: true
//     width: 640
//     height: 480
//     title: "Centro de Pesquisas Genealógicas"

//     // 1. Menu de Opções
//     menuBar: MenuBar {
//         Menu {
//             title: "Início"
//             MenuItem { text: "Importar Dados" }
//             MenuItem { text: "Configurações" }
//             MenuItem { text: "Sair" }
//         }

//         Menu {
//             title: "Cadastrar"
//             MenuItem { text: "Importar Dados" }
//             MenuItem { text: "Configurações" }
//             MenuItem { text: "Sair" }
//         }

//         Menu {
//             title: "Usuário"
//             MenuItem { text: "Importar Dados" }
//             MenuItem { text: "Configurações" }
//             MenuItem { text: "Sair" }
//         }


//         Menu {
//             title: "Configurações"
//             MenuItem { text: "Importar Dados" }
//             MenuItem { text: "Configurações" }
//             MenuItem { text: "Sair" }
//         }
//     }

//     // Organiza os itens em uma coluna centralizada
//     Column {
//         anchors.centerIn: parent
//         spacing: 20


//         Text{
//             // anchors.centerIn: parent
//             text: "Hello World QML"
//             color: '#eb6c17'
//             font.bold: true
//         }

//         // 2. Campo de Busca
//         TextField {
//             id: searchField
//             width: 450
//             height: 55
//             placeholderText: "Buscar indivíduo..."
//         }

//         // 3. Botão de Criar Novo Indivíduo
//         Button {
//             text: "Criar Novo Indivíduo"
//             width: 200
//             height: 50
//             // 1. Tipografia básica
//             font.pixelSize: 16
//             font.bold: true
//             font.family: "Arial"
//             // 2. Estilização do fundo do botão
//             background: Rectangle {
//                 color: parent.down ? "#2980b9" : "#3498db" // Muda de cor ao ser clicado (efeito visual)
//                 radius: 10                                 // Cantos arredondados
//                 border.color: "#21618c"                    // Cor do contorno
//                 border.width: 2                            // Espessura do contorno
//             }
//             // 3. Estilização do texto (cor e alinhamento)
//             contentItem: Text {
//                 text: parent.text
//                 font: parent.font
//                 color: "#ffffff"                           // Texto na cor branca
//                 horizontalAlignment: Text.AlignHCenter     // Centraliza na horizontal
//                 verticalAlignment: Text.AlignVCenter       // Centraliza na vertical
//             }
//         }
//     }
// }

