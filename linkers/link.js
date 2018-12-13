var textbar = document.getElementById('textbar')

//Adding event listener on enterkey
textbar.addEventListener("keydown", function (e) {
    if (e.keyCode === 13) {
        var args = textbar.value;
        getcmd(args);
    }
});



function getcmd(args="null")
{
    // The path to your python script
    var myPythonScript = "python/engine.py ";

    // Provide the path of the python executable, if python is available as environment variable then you can use only "python"
    var pythonExecutable = "python.exe";

    // Function to convert an Uint8Array to a string
    var uint8arrayToString = function(data){
    return String.fromCharCode.apply(null, data); };

const spawn = require('child_process').spawn;
const scriptExecution = spawn(pythonExecutable, [myPythonScript,args]);

// Handle normal output
scriptExecution.stdout.on('data', (data) => {
    console.log(uint8arrayToString(data));
    swal(uint8arrayToString(data));
});

// Handle error output
scriptExecution.stderr.on('data', (data) => {
    // As said before, convert the Uint8Array to a readable string.
    console.log(uint8arrayToString(data));
    swal("Error!",uint8arrayToString(data) , "error");

});

scriptExecution.on('exit', (code) => {
    console.log("Process quit with code : " + code);
});

}
