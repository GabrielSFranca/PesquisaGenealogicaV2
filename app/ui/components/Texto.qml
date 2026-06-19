import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Label {
    // Permite definir o texto de fora do componente
    id: root
    property alias lbl: root.text
    // Configurações padrão para um título
    font.pixelSize: 18          // Tamanho sugerido para títulos principais
    // Garantir que o título se ajusta ao layout
    Layout.fillWidth: true
    horizontalAlignment: Text.AlignHCenter
    
    // Suporte para quebra de linha se o título for longo
    wrapMode: Label.WordWrap
    
    // Margens opcionais para respiro visual
    topPadding: 10
    bottomPadding: 10
}



// import QtQuick
// import QtQuick.Layouts
// import QtQuick.Controls

// ColumnLayout{
//     property alias texto: label.text
//     property alias placeholder: input.placeholderText
//     property alias text: input.text

//     Layout.fillWidth: true

//     Layout.preferredWidth: 0
//     spacing: 6
    
//     Text {
//         id: label
//         font.pixelSize: 14
//         font.bold: true
//         color: "#374151"
//         Layout.fillWidth: true
//         elide: Text.ElideRight
//     }

//     TextField {
//         id: input
//         Layout.fillWidth: true
//     }
// }