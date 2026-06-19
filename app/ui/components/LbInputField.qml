import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "."

ColumnLayout{
    id: root
    property alias txt: label.text
    property alias ph: input.placeholderText
    property alias text: input.text

    spacing: 6
    width: 250
    Layout.fillWidth: true

    Texto{ id: label }
    Input{ 
        id: input
        Layout.fillWidth: true 
    }
}