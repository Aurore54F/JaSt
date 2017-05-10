
'''
	Indicate if given files are (correct) JavaScript files or not.
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands
import glob # Unix style pathname pattern expansion
import os

notJs = [];
structureError = [];


def isJs(jsDir, parser = 'esprimaAst'):
	'''
		Given a repository containing .bin or .js files, indicate whether they are (correct) JavaScript files or not.
	'''
	
	global notJs;
	notJs = [];
	global structureError;
	structureError = [];

	l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	
	if parser.lower() == 'slimit':
		command = 'slimit --mangle '
	elif parser.lower() == 'esprima':
		command = 'node ../src/JsEsprima/tokenizer.js '
	elif parser.lower() == 'esprimaast':
		command = 'node ../src/JsEsprima/parser.js '
		# Tests on 1900 samples demonstrate the added value and performance of Esprima parser (esprimaAst), against the other two ones.
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
			
	for givenFile in sorted(l):
		try:
			subprocess.check_output(command + givenFile + ' 2> /dev/null', shell = True)
		except subprocess.CalledProcessError as e:
			if  e.returncode == 1:
				#subprocess.run('mv ' + givenFile + ' NotJs');
				#print('Return: ' + str(e.output) + '\n');
				if str(e.output) == "b''":
					print('The file ' + givenFile + ' is not considered as JavaScript.');
					notJs += [givenFile];
				else:
					print('Error on the file ' + givenFile + ' structure.');
					structureError += [givenFile];
	
	print('The following files are not considered as JavaScript:\n');
	for el in notJs:
		print('- ' + el + '\n');

	print('The following files structure is not correct:\n');
	for el in structureError:
		print('- ' + el + '\n');
