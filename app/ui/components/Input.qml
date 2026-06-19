import QtQuick
import QtQuick.Controls

TextField {
    id: root

    height: 50
    placeholderText: ""
    font.pixelSize: 18
    
    // background: Rectangle {
    //     //radius: 8
    //     //color: '#998f8f'
    //     border.width: 2
    //     border.color: "#FFD54F"
    // }
    
    // Sobrescrevendo o fundo nativo para garantir uma área de clique de 50px
    background: Rectangle {
        implicitHeight: 50 // ALTURA ACESSÍVEL
        color: "#ffffff"
        border.color: input.activeFocus ? "#2563eb" : "#6b7280" // Azul se focado, cinza médio se não
        border.width: 2    // Borda mais grossa para destacar a área
        //radius: 6
    }
}