
'''
	Producing tokens from a JavaScript file
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands


def buildToken(parser,inputFile,outputFile):
	'''
		Given an input JavaScript file, write the list of tokens used in an output file.
	'''
	
	if parser.lower() == 'slimit':
	
		inF = open(inputFile,'r');
		s = '';
		for line in inF:
			s += str(line); # Store the content of the JS file in a string
		inF.close();
		
		lexer = Lexer();
		lexer.input(s);

		outF = open(outputFile,'w');

		for token in lexer:
			value = token;
			s = str(value); # Conversion of token type to string
			# Structure of a token: "LexToken(VAR,'var',1,0)"
			tokenPart = s.split('(');
			tokenComplete = tokenPart[1].split(','); # Keyword as used in JS
			
			outF.write(tokenComplete[0] + '\n');
			
		outF.close();
		
		
	elif parser.lower() == 'esprima':
		
		tempFile = 'Tempo.txt';
		subprocess.call("slimit --mangle < " + inputFile + " > " + tempFile, shell = True); # Minify the input file
		
		tFile = open(tempFile,'r');
		s = "var esprima = require('esprima');\nesprima.tokenize('";
		for line in tFile:
			s += line;
		s += "', {}, function (node) {\n\tconsole.log(node.type);\n});"
		#return s;
		tFile.close();
		tFile = open(tempFile,'w');
		
		tFile.write(s);
		tFile.close();
		
		subprocess.call("node " + tempFile + " > " + outputFile, shell = True); # Esprima
		
	else:
		print("Error on the parser's name. Indicate 'slimIt' or 'esprima'.");
	
	
	

	
