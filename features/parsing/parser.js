// Syntactic analysis of a file whose path is given as command line argument. Esprima is used for
// the parsing process and prints in stdout the list of syntactic units present in the file.

function parse(js, tolerance) {
    var fs = require("fs");
    var text = fs.readFileSync(js).toString('utf-8');
    var esprima = require('esprima');
    esprima.parse(text, {comment: true, tolerant: tolerance}, function (node) {
        console.log(node.type)
    });
}

var tolerance = (process.argv[3] == 'true')
parse(process.argv[2], tolerance)
