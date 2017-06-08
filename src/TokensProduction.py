
'''
	Extracting lexical and syntactical tokens from a JavaScript file and converting them into integers.
'''

from slimit.lexer import Lexer
import sys
sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima

import subprocess # to call Shell commands

globVar = 1;

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
	global globVar;
	#globVar = 0;
	try:
		result = subprocess.check_output('nodejs JsEsprima/parser.js ' + inputFile + ' 2> /dev/null', shell = True);
		# result is a string containing the syntactical tokens (as found by esprima) of the given JS script, separated by '\n'.
		# Structure of a token: "b'Literal\n'"
		syntaxPart = str(result).split("b'")[1].split('\\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		print('File ' + inputFile + ': valid JavaScript');
		print('Tot ' + str(globVar));
		globVar += 1;
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
		
	except subprocess.CalledProcessError as e: # TODO catch exception if file cannot be opened
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print('File ' + inputFile + ': not JavaScript');
				#return;
			else: # The file could partially be parsed: malformed JS
				print('File ' + inputFile + ': malformed JavaScript');
				#return;
	
	'''
		result = subprocess.run(['node' , 'JsEsprima/parser.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
		# result is a string containing the returneinptttd objects of the JS script, separated by '\n'
		syntaxPart = str(result).split('\n'); # Keyword as used in JS
		del(syntaxPart[len(syntaxPart) - 1]); # As last one = ''
		return syntaxPart; # The order of the tokens returned resembles a tree traversal using the depth-first algorithm.
	'''
	

def isJsFile(givenFile):
	'''
		Given a file path, indicate whether the file is either valid JavaScript, malformed JavaScript or no JavaScript.
				
		-------
		Parameter:
		- givenFile: string
			Path of the file to be analysed.
			
		-------
		Returns:
		- Integer
			Indicates whether the file is either valid JavaScript (0), malformed JavaScript (2) or no JavaScript (1).
	'''
	
	global globVar;
	try:
		subprocess.check_output('nodejs JsEsprima/parser.js ' + givenFile + ' 2> /dev/null', shell = True);
		print('File ' + givenFile + ': valid JavaScript');
		print('Tot ' + str(globVar));
		globVar += 1;
		return 0;
	except subprocess.CalledProcessError as e:  # TODO catch exception if file cannot be opened
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print('File ' + givenFile + ': not JavaScript');
				return 1;
			else: # The file could partially be parsed: malformed JS
				print('File ' + givenFile + ': malformed JavaScript');
				return 2;
	
	
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
	
	if isJsFile(inputFile) == 0: # Only if the current file is a well-formed JS sample
		result = subprocess.run(['nodejs' , 'JsEsprima/tokenizer.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
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
	
	if isJsFile(inputFile) == 0: # Only if the current file is a well-formed JS sample
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
		

def tokensUsed(parser, jsFile):
	'''
		Return the list of tokens (for a given parser) present in a given JavaScript document.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- jsFile: String
			Path of the JavaScript file to be analysed.
			
		-------
		Returns:
		- List
			Contains the tokens present in jsFile given in input.
	'''
	
	if parser.lower() == 'slimit':
		tokensList = tokensUsedSlimit(jsFile);
	elif parser.lower() == 'esprima':
		tokensList = tokensUsedEsprima(jsFile);
	elif parser.lower() == 'esprimaast':
		tokensList = astUsedEsprima(jsFile);
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
	return tokensList;


def dicoUsed(parser):
	'''
		Return the Dictionary corresponding to the parser given in input.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
			
		-------
		Returns:
		- Dictionary
			Either DicoOfTokensSlimit.tokensDico, DicoOfTokensEsprima.tokensDico, or DicoOfAstEsprima.astDico.
	'''
	
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimit.tokensDico;
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
	elif parser.lower() == 'esprimaast':
		dico = DicoOfAstEsprima.astDico;		
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
	return dico;


def tokensToNumbers(tokensDico, tokensList):
	'''
		Convert a list of tokens in their corresponding numbers (as indicated in the corresponding tokens dictionary).
		
		-------
		Parameters:
		- tokensDico: Dictionary
			Either DicoOfTokensSlimit.tokensDico, DicoOfTokensEsprima.tokensDico, or DicoOfAstEsprima.astDico. TODO
		- tokensList: List
			List containing the tokens extracted from a JS file.
		-------
		Returns:
		- List
			Contains the Integers which correspond to the tokens given in tokensList.
		- or None if tokensDico is empty.
	'''

	if tokensList is not None and tokensList != []:
		#i = 0;
		#print('Debug, len(tokensList): ' + str(len(tokensList)));
		numbers = [];
		
		for token in tokensList:
			#print(str(i));
			numbers = numbers + [tokensDico[token]];
			#i += 1;
		
		return numbers;
