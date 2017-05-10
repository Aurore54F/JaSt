
'''
	Producing tokens from a JavaScript file and converting them into integers.
'''

from slimit.lexer import Lexer

import subprocess # to call Shell commands
import glob # Unix style pathname pattern expansion
import os


def isJs(jsDir, parser = 'esprimaAst'):
	'''
		Given a repository containing .bin or .js files, indicate whether they are JavaScript files or not.
	'''
	#subprocess.run(['node' , '../src/JsEsprima/parser.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
	#subprocess.run(['node' , '../src/JsEsprima/tokenizer.js', inputFile], stdout = subprocess.PIPE).stdout.decode('utf-8');
	#subprocess.run(['node' , '../src/JsEsprima/parser.js', givenFile], stdout = subprocess.PIPE).stdout.decode('utf-8');

	if not os.path.exists('NotJs'):
		os.makedirs('NotJs');

	l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	
	if parser.lower() == 'slimit':
		for givenFile in sorted(l):
			#result = subprocess.run('slimit --mangle ' + givenFile + ' 2> /dev/null', stdout = subprocess.PIPE).stdout.decode('utf-8');
			try:
				subprocess.check_output('slimit --mangle ' + givenFile + ' 2> /dev/null', shell = True)
			except subprocess.CalledProcessError as e:
				if  e.returncode == 1:
					#subprocess.run('mv ' + givenFile + ' NotJs');
					print('Return: ' + str(e.output) + '\n');
					if str(e.output) == "b''":
						print('The file ' + givenFile + ' is not considered as a valid JavaScript file.');
					else:
						print('Error on the file ' + givenFile + ' structure.');
				
	elif parser.lower() == 'esprima':
		for givenFile in sorted(l):
			try:
				subprocess.check_output('node ../src/JsEsprima/tokenizer.js ' + givenFile + ' 2> /dev/null', shell = True)
			except subprocess.CalledProcessError as e:
				if  e.returncode == 1:
					#subprocess.run('mv ' + givenFile + ' NotJs');
					print('Return: ' + str(e.output) + '\n');
					if str(e.output) == "b''":
						print('The file ' + givenFile + ' is not considered as a valid JavaScript file.');
					else:
						print('Error on the file ' + givenFile + ' structure.');
				
	elif parser.lower() == 'esprimaast':
		for givenFile in sorted(l):
			try:
				subprocess.check_output('node ../src/JsEsprima/parser.js ' + givenFile + ' 2> /dev/null', shell = True)
			except subprocess.CalledProcessError as e:
				if  e.returncode == 1:
					#subprocess.run('mv ' + givenFile + ' NotJs');
					print('Return: ' + str(e.output) + '\n');
					if str(e.output) == "b''":
						print('The file ' + givenFile + ' is not considered as a valid JavaScript file.');
					else:
						print('Error on the file ' + givenFile + ' structure.');
						
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
