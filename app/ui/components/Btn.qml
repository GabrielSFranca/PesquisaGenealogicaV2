import QtQuick
import QtQuick.Layouts

import "."

Button{
    id: root
    property alias text: root.text

    onClicked: { console.log("clicado") }
    
}