window.onload = function() {
    getTest();
//    setTimeout(AskQuestion, 1500);
};
var synth = window.speechSynthesis;
function submitTestLog(){
    var url = 'log_test_answer';
    var xhr = new XMLHttpRequest()
    var patient_id = document.getElementById('patient_id').value;
    var test_id = document.getElementById('test_id').value;
    url = url + "?patient_id=" + patient_id + "&test_id=" + test_id;
    xhr.open('GET', url, true)  
    xhr.send();
    xhr.onloadend = function () {
        getTest();
    };
}
function getTest() {
    var url = 'get_random_test';
    var xhr = new XMLHttpRequest()
    xhr.open('POST', url, true)
    xhr.send();
    xhr.onloadend = function () {
        var test = document.getElementById('test__contents');
        test.innerHTML = xhr.responseText;
        setTimeout(AskQuestion, 1000);
    };
}

function AskQuestion(){
    var text = document.getElementById("question").innerHTML;
    var voices = speechSynthesis.getVoices();
    var utterThis = new SpeechSynthesisUtterance(text);
    utterThis.voice = voices[0];
    synth.speak(utterThis);
}


function FinishTestAndGetGraphic(){
    document.getElementById('loader').style.display = "block";
    var patient_id = document.getElementById('patient_id').value;
    var url = 'patient_change_plots';
    var xhr = new XMLHttpRequest()
    url = url + "?patient_id=" + patient_id;
    xhr.open('GET', url, true)  
    xhr.send();
    xhr.onloadend = function () {
        document.getElementById('loader').style.display = "none";
        var graphic = document.getElementById('graphic');
        graphic.innerHTML = xhr.responseText;
        // draw a plot 
    };

}
