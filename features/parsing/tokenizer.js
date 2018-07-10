// Lexical analysis of a file whose path is given as command line argument. Esprima is used for the
// tokenizing process and prints in stdout the list of lexical units (tokens) present in the file.

var fs = require("fs");
var text = fs.readFileSync(process.argv[2]).toString('utf-8');
var esprima = require('esprima');
esprima.tokenize(text, { comment: true }, function (node) {
	console.log(node.type)
	});
