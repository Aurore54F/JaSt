
'''
	Producing tokens from a JavaScript file and converting them into integers.
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands
import os

def astUsedEsprima(inputFile):
	'''
		Given an input JavaScript file, create a list containing the esprima syntactical tokens present in the file.
		The order of the tokens stored in the previous list resembles a tree traversal using the depth-first algorithm.
		
		-------
		Parameter:
		- inputFile: File
			Should it be malformed or no JS file, then an exception will be raised.
			
		-------
		Returns:
		- List
			Contains the esprima syntactical tokens present in the input file.
		- or None if the file either is no JS or malformed.
	'''
	
	try:
		result = subprocess.check_output('node JsEsprima/parser.js ' + inputFile + ' 2> /dev/null', shell = True);
		# result is a string containing the syntactical tokens (as found by esprima) of the given JS script, separated by '\n'.
		# Structure of a token: "b'Literal\n'"
		syntaxPart = str(result).split("b'")[1].split('\\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
		
	except subprocess.CalledProcessError as e: # TODO catch exception if file cannot be opened
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print('The file ' + inputFile + ' is not considered as JavaScript.');
			else: # The file could partially be parsed: malformed JS
				print('Error on the file ' + inputFile + ' structure.');
	
	'''
		result = subprocess.run(['node' , 'JsEsprima/parser.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
		# result is a string containing the returneinptttd objects of the JS script, separated by '\n'
		syntaxPart = str(result).split('\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
	'''
	
	
def tokensUsedEsprima(inputFile):
	'''
		Given an input JavaScript file, create a list containing the esprima lexical tokens present in the file.
		
		-------
		Parameter:
		- inputFile: File
			Should it be malformed or no JS file, then an exception will be raised. TODO
			
		-------
		Returns:
		- List
			Contains the esprima lexical tokens present in the input file.
		- or None if the file either is no JS or malformed.
	'''
	
	result = subprocess.run(['node' , 'JsEsprima/tokenizer.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
	# result is a string containing the lexical tokens (as found by esprima) of the given JS script, separated by '\n'.
	# Structure of a token: "b'Punctuator\n'"
	tokenPart = str(result).split('\n'); # Keyword as used in JS
	del(tokenPart[len(tokenPart) - 1]); # As last one = ''
		
	return tokenPart;
	
		
	
def tokensUsedSlimit(inputFile):
	'''
		Given an input JavaScript file, create a list containing the SlimIt lexical tokens present in the file.
		
		-------
		Parameter:
		- inputFile: File
			Should it be malformed or no JS file, then an exception will be raised. TODO
			
		-------
		Returns:
		- List
			Contains the SlimIt lexical tokens present in the input file.
		- or None if the file either is no JS or malformed.
	'''
	
	inF = open(inputFile,'r');
	s = '';
	for line in inF:
		s += str(line); # Store the content of the JS file in a string, because far more quicker than using SlimIt minifier.
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
		Convert a list of tokens in their corresponding numbers (as indicated in the corresponding tokens dictionary).
		
		-------
		Parameters:
		- tokensDico: Dictionary
			Either DicoOfTokensSlimit.tokensDico, or DicoOfTokensEsprima.tokensDico, or DicoOfAstEsprima.astDico. TODO
		- tokensList: List
			List containing the tokens extracted from a JS file.
		-------
		Returns:
		- List
			Contains the Integers which correspond to the tokens given in tokensList.
		- or None if tokensDico is empty.
	'''

	if tokensList is not None:
		numbers = [];
		
		for token in tokensList:
			numbers = numbers + [tokensDico[token]];
		
		return numbers;
