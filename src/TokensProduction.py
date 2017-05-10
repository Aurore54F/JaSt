
'''
	Producing tokens from a JavaScript file and converting them into integers.
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands
import os


def astUsedEsprima(inputFile):
	'''
		Given an input JavaScript file, create a list containing the esprima syntactic elements used.
	'''
	
	try:
		result = subprocess.check_output('node JsEsprima/parser.js ' + inputFile + ' 2> /dev/null', shell = True);
		# result is a string containing the returned objects of the JS script, separated by '\n'
		syntaxPart = str(result).split("b'")[1].split('\\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
	except subprocess.CalledProcessError as e:
		if  e.returncode == 1:
			print('Error with the file ' + inputFile + '.');
	
	'''
		result = subprocess.run(['node' , 'JsEsprima/parser.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
		# result is a string containing the returneinptttd objects of the JS script, separated by '\n'
		syntaxPart = str(result).split('\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
	'''
	
	
def tokensUsedEsprima(inputFile):
	'''
		Given an input JavaScript file, create a list containing the esprima tokens used.
	'''
	
	result = subprocess.run(['node' , 'JsEsprima/tokenizer.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
	# result is a string containing the returned objects of the JS script, separated by '\n'
	tokenPart = str(result).split('\n'); # Keyword as used in JS
	del(tokenPart[len(tokenPart) - 1]); # As last one = ''
		
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
	
	lexer = Lexer();
	lexer.input(s);
	l = [];

	'''
		result = subprocess.run(['slimit', '--mangle', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
		lexer = Lexer();
		lexer.input(result);
		l = [];
	'''

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
