#!/usr/bin/python

'''
	Indicate whether given files are either valid JavaScript files, malformed JavaScript files or if they are no JavaScript files.
'''

import subprocess # to call Shell commands
import glob # Unix style pathname pattern expansion
import argparse


def isJsFile(givenFile):
	'''
		Given a file path, indicate whether the file is either valid JavaScript, malformed JavaScript or no JavaScript.
				
		-------
		Parameter:
		- givenFile: string
			Path of the file to be analysed.
			
		-------
		Returns:
		- Message
			Indicates whether the file is either valid JavaScript, malformed JavaScript or no JavaScript.
	'''
	
	try:
		subprocess.check_output('node ../src/JsEsprima/parser.js ' + givenFile + ' 2> /dev/null', shell = True)
	except subprocess.CalledProcessError as e:  # TODO catch exception if file cannot be opened
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print('File ' + givenFile + ': not JavaScript');
				return;
			else: # The file could partially be parsed: malformed JS
				print('File ' + givenFile + ': malformed JavaScript');
				return;
	print('File ' + givenFile + ': valid JavaScript');


parser = argparse.ArgumentParser(description='Given a list of repositories or files paths, indicate whether the files are either valid JavaScript, malformed JavaScript or if they are no JavaScript.'); # Creating an ArgumentParser object
# The ArgumentParser object holds all the information necessary to parse the command line into Python data types.

#parser.add_argument('dir', nargs='*', help='directory containing files to be tested');
parser.add_argument('--f', metavar='FILE', nargs='+', help='file to be tested');
parser.add_argument('--d', metavar='DIR', nargs='+', help='directory to be tested');
	
args = vars(parser.parse_args());


if args['d'] != None:
	for el in args['d']:
		l = glob.glob(el + '/*.js') + glob.glob(el + '/*.bin'); # Extension in .bin or .js			
		for givenFile in sorted(l):
			isJsFile(givenFile);


if args['f'] != None:
	for givenFile in args['f']:
		isJsFile(givenFile);