
'''
	Producing tokens from a JavaScript file
'''

from slimit.lexer import Lexer


def buildToken(inputFile,outputFile):
	'''
		Given an input JavaScript file, write the list of tokens used in an output file.
	'''
	
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
	
	
	

	
