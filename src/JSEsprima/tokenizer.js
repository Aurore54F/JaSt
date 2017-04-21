var fs = require("fs");
var text = fs.readFileSync(process.argv[2]).toString('utf-8');
var esprima = require('esprima');
esprima.tokenize(text, {}, function (node) {
	console.log(node.type)
	});

