import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Label {
    // Permite definir o texto de fora do componente
    id: root
    property alias lbl: root.text
    // Configurações padrão para um título
    font.pixelSize: 32          // Tamanho sugerido para títulos principais
    font.bold: true             // Títulos devem ter peso visual
    
    // Garantir que o título se ajusta ao layout
    Layout.fillWidth: true
    horizontalAlignment: Text.AlignHCenter
    
    // Suporte para quebra de linha se o título for longo
    wrapMode: Label.WordWrap
    
    // Margens opcionais para respiro visual
    topPadding: 10
    bottomPadding: 10
}


