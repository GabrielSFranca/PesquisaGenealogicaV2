import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    property alias texto: label.text
    property alias placeholder: input.placeholderText
    property alias text: input.text

    Layout.fillWidth: true

    Layout.preferredWidth: 0
    spacing: 6
    
    Text {
        id: label
        font.pixelSize: 14
        font.bold: true
        color: "#374151"
        Layout.fillWidth: true
        elide: Text.ElideRight
    }

    TextField {
        id: input
        Layout.fillWidth: true
    }
}