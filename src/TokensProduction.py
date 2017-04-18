
'''
	Producing tokens from a JavaScript file and converting them into integers.
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands
import os


def tokensUsedEsprima(inputFile):
	'''
		Given an input JavaScript file, create a list containing the esprima tokens used.
	'''
	tempFile = 'Tempo.txt';
	subprocess.call("slimit --mangle < " + inputFile + " > " + tempFile, shell = True); # Minify the input file
	
	tFile = open(tempFile,'r');
	s = "var esprima = require('esprima');\nesprima.tokenize('";
	for line in tFile:
		line = line.replace("'",'"');
		s += line;
	s += "', {}, function (node) {\n\tconsole.log(node.type);\n});"
	#return s;
	tFile.close();
	tFile = open(tempFile,'w');
	
	tFile.write(s);
	tFile.close();
	
	#subprocess.call("node " + tempFile + " > " + outputFile, shell = True); # Produce the list of tokens using esprima
	
	result = subprocess.run(['node' , tempFile ], stdout = subprocess.PIPE).stdout.decode('utf-8');
	os.remove(tempFile);
	
	tokenPart = str(result).split('\n'); # Keyword as used in JS
	del(tokenPart[len(tokenPart) - 1]);
		
	return tokenPart;
	
		
	
def tokensUsedSlimit(inputFile):
	'''
		Given an input JavaScript file, create a list containing the SlimIt tokens used.
	'''
	inF = open(inputFile,'r');
	s = '';
	for line in inF:
		s += str(line); # Store the content of the JS file in a string
	inF.close();
	
	#result = subprocess.run(["slimit --mangle < ", inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
	
	lexer = Lexer();
	lexer.input(s);

	l = [];

	for token in lexer:
		# Structure of a token: "LexToken(VAR,'var',1,0)"
		tokenPart = str(token).split('(');
		tokenComplete = tokenPart[1].split(','); # Keyword as used in JS
		l += [tokenComplete[0]];
	
	return l;



def tokensToNumbers(tokensDico, tokensList):
	'''
		Convert a list of tokens in their corresponding numbers (as indicated in the tokens dictionary).
	'''

	numbers = [];
	
	for token in tokensList:
		numbers = numbers + [tokensDico[token]];
	
	return numbers;
