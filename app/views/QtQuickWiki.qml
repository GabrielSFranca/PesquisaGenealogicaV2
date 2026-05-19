import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow{
    visible: true
    title: "Titulo da janela de aplicacao"
    height: 600 // altura de 100px
    width: 800 // largura de 200 pixels

    // font.pixelSize: 18 // tam min da font de texto
    // component Titulo
    // Label= vem de QtQuick.Controls
    // se adapta ao tema
    Label{ 
        text: "Elemento Label Título"
        font.pixelSize: 32  // tamanho da fonte de titulo
        font.bold: true  // negrito
    }

    Rectangle{
        // equivalente a tag <div> do HTML
        width: 300 
        height: 150  
        // cor de fundo: vermelho
        color: "#821"
        // borda
        border.color: "black" // cor
        border.width: 2       // espessura
        // raio do arredondamento de 10px
        radius: 10
        anchors.centerIn: parent

        ColumnLayout{
            anchors.fill: parent
            anchors.margins: 20
            // elemento primitivo do modulo QtQuick
            // nao se adapta a temas como Material, Fusion
            Text{ 
                text: "Elemento Text, paragrafo"
                font.family: "Segoe UI"
                font.pixelSize: 18
                color: '#d4c7c5'
            }

            // Botao
            Button {
                text: "Buscar"
                font.pixelSize: 18
                font.bold: true
                //Layout.alignment: Qt.AlignHCenter
                // layouts responsivos
                Layout.preferredWidth: 250 // Botão largo
                Layout.preferredHeight: 55 // Botão alto para fácil clique

                // filhos de Column e Row Layout podem usar fillWidht (ocupar a largura total)
                Layout.fillWidth: true
                onClicked: { console.log("clicked"); }
            }
        }
    }

    Row{
        //anchors.left: parent.right
        spacing: 10 // intervalo de espaçamento entre itens em px
        Rectangle{ width:50; height:50; color: "blue" }
        Rectangle{ width:50; height:50; color: "red" }
    }

    // // elemento primitivo do modulo QtQuick
    // // nao se adapta a temas como Material, Fusion
    // Text{ 
    //     text: "Elemento Text, paragrafo"
    //     font.family: "Segoe UI"
    //     font.pixelSize: 18    
    // }
    
    // Button {
    //     text: "Buscar"
    //     font.pixelSize: 18
    //     font.bold: true
    //     Layout.alignment: Qt.AlignHCenter
    //     Layout.preferredWidth: 250 // Botão largo
    //     Layout.preferredHeight: 55 // Botão alto para fácil clique
    //     onClicked: { console.log("clicked"); }
    //     //
    // }

}




// import QtQuick
// import QtQuick.Controls

// ApplicationWindow{
//     visible: true

//     RowLayout{
//         spacing: 10
        
//         SpinBox{
//             id: spinSmartDay
//             from: 0
//             value: 0
//             to: {
//                 let mes=combMes.currentIndex;
//                 //

//                 if(mes===0) return 31;
//                 if(mes===2){
//                     if(ano !== 0 && ((ano%4==0 && ano%100!=0) ||  (ano%400==0))){
//                         return 29;
//                     }else{
//                         return 28;
//                     }
//                 }

//                 if(mes===4 || mes===6 || mes===9 || mes===11) return 30;

//                 return 31;
//             }
//         }

//         ComboBox{
//             id: combMes
//             model: ["MM", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
//             currentIndex: 0
//         }

//         SpinBox{
//             id: spinYear
//             from: 0
//             to: new Date().getFullYear()
//             value: 0
//             editable: true
//             textFromValue: function (value, locale) {
//                 return value === 0? "AAAA" : Number(value).toLocaleString(locale)
                
//             }
//         }
//     }




// }






// import QtQuick
// import QtQuick.Controls

// Page {
//     title: "Início"

//     Column {
//         anchors.centerIn: parent
//         spacing: 20

//         Label {
//             text: "Sistema de Genealogia"
//             font.pixelSize: 24
//         }

//         Button {
//             text: "Cadastrar Pessoa"
//             onClicked: {
//                 stack.push("PersonForm.qml")
//             }
//         }
//     }
// }



// import QtQuick
// import QtQuick.Controls

// ApplicationWindow{
//     id: root
//     visible: true
//     width: 700
//     height: 500
//     title: "Cadastro"
//     //color: "white"


//     Rectangle{
//         id: rect
//         width: 300
//         height: 100
//         anchors.centerIn: parent

//         Column{
//             id: col
//             width: parent.width
//             height: parent.height
//             spacing: 16

//             Text{
//                 id: lbl
//                 text: "Primeiro nome"
//                 font.pixelSize: 16
//             }


//             TextField{
//                 id: campo
//                 placeholderText: "Digite o primeiro nome"
//                 //width: parent.width
//             }
//         }
//         }