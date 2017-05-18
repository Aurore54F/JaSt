#!/usr/bin/python

'''
	Indicate if given files are (valid) JavaScript files or if they are not JavaScript.
'''


import subprocess # to call Shell commands
import glob # Unix style pathname pattern expansion
import argparse

notJs = [];
structureError = [];



parser = argparse.ArgumentParser(description='Given a repository containing .bin or .js files, indicate whether they are (valid) JavaScript files or not.'); # Creating an ArgumentParser object
# The ArgumentParser object holds all the information necessary to parse the command line into Python data types.

#parser.add_argument('Dir', help='list of files');

parser.add_argument('dir', nargs='*', help='directory containing files to be tested');
parser.add_argument('--f', nargs='+', help='list of files to be tested');
parser.add_argument('--s', help='print a summary of the state of the files');
	
args = vars(parser.parse_args());


def isJsFile(givenFile):
	global notJs;
	global structureError;
	notJs = [];
	structureError = [];

	try:
		subprocess.check_output('node ../src/JsEsprima/parser.js ' + givenFile + ' 2> /dev/null', shell = True)
	except subprocess.CalledProcessError as e:  # TODO catch exception if file cannot be opened
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print('File ' + givenFile + ': not JavaScript');
				notJs += [givenFile];
				return;
			else: # The file could partially be parsed: malformed JS
				print('File ' + givenFile + ': invalid JavaScript');
				structureError += [givenFile];
				return;
	print('File ' + givenFile + ': valid JavaScript');
	

'''
	Given a repository containing .bin or .js files, indicate whether they are (valid) JavaScript files or not.
'''

if args['dir'] != []:
	for el in args['dir']:
		l = glob.glob(el + '/*.js') + glob.glob(el + '/*.bin'); # Extension in .bin or .js			
		for givenFile in sorted(l):
			isJsFile(givenFile);


if args['f'] != None:
	for givenFile in args['f']:
		isJsFile(givenFile);


if args['s'] != None:
	
	print('\n\n Summary:\n');
	print('* The following files are not considered as JavaScript:');
	for el in notJs:
		print('\t- ' + el);
	
	print('\n* The following files structure is not correct:\n');
	for el in structureError:
		print('\t- ' + el);
