window.editorsDone = 0;
var minLines = 1;
var startingValue = document.head.querySelector("[property~=in_code][content]").content;

for (var i = 1; i < minLines; i++) {
    startingValue += '\n';
}

var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    gutter: true,
    lineWrapping: true,
    value: startingValue
});

editor.setValue(startingValue);
editor.setCursor({line: 1, ch: 0}); 

window.onload=function(){
  if (startingValue!='')
      document.getElementById("goesFirst").click();
      document.getElementById("clone").scrollIntoView();
};

$.getJSON('https://json.geoiplookup.io/api?callback=?', function(data) {
    window.ip = JSON.stringify(data["ip"], null, 2);
});

function openTab(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
    
    
  if (window.editorsDone==0){
      window.editorsDone = 1;
      window.codeAmount = document.getElementsByClassName("cloneOur");

      for (i = 1; i < codeAmount.length+1; i++) {
        window["cloneOurEditor"+i] = CodeMirror.fromTextArea(document.getElementById("cloneOur"+i), {
            lineNumbers: true,
            gutter: true,
            lineWrapping: true,
//             firstLineNumber: window.js_startLines[0][i-1],
            readOnly: 'nocursor',
        });

      } 

      window.codeAmount = document.getElementsByClassName("cloneTheir");

      for (i = 1; i < codeAmount.length+1; i++) {
        window["cloneTheirEditor"+i] = CodeMirror.fromTextArea(document.getElementById("cloneTheir"+i), {
            lineNumbers: true,
            gutter: true,
            lineWrapping: true,
//             firstLineNumber: window.js_startLines[1][i-1],
            readOnly: 'nocursor',
        });

      } 
      
      window.codeAmount = document.getElementsByClassName("bugOur");

      for (i = 1; i < codeAmount.length+1; i++) {
        window["bugOurEditor"+i] = CodeMirror.fromTextArea(document.getElementById("bugOur"+i), {
            lineNumbers: true,
            gutter: true,
            lineWrapping: true,
//             firstLineNumber: window.js_startLines[2][i-1],
            readOnly: false,
        });
        window["bugOurEditor"+i].markText({line:window.js_top_bug[i-1][0]-1,ch:0},{line:window.js_top_bug[i-1][1],ch:0},{css:"background-color: #fe3"});
      } 
  }
    else{
        window.codeAmount = document.getElementsByClassName("bugOur");
        for (i = 1; i < codeAmount.length+1; i++) {
            window["bugOurEditor"+i].scrollIntoView({line: window.js_top_bug[i-1][1], ch:1});
        }
    }
    
} 