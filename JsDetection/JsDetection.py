#!/usr/bin/python

'''
	Indicate whether given files are either valid JavaScript files, malformed JavaScript files or if they are no JavaScript files.
'''

import subprocess # to call Shell commands
import os # for OS dependent functionality
import argparse # to deal with command line arguments


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
	
	try:
		subprocess.check_output('nodejs ../src/JsEsprima/parser.js ' + givenFile + ' 2> /dev/null', shell = True)
		print(givenFile + ': valid JavaScript');
		return 0;
	except subprocess.CalledProcessError as e:
		if  e.returncode == 1:
			if str(e.output) == "b''": # The file could not be parsed: not a JS sample
				print(givenFile + ': not JavaScript');
				return 1;
			else: # The file could partially be parsed: malformed JS
				print(givenFile + ': malformed JavaScript');
				return 2;
	except OSError: # System-related error
		print("System-related error");
		return;


def main():
	'''
		A list of files or repositories can be given as command line arguments, for this program to indicate whether the files are either valid, malformed or no JavaScript.
				
		-------
		Returns:
		- Message (stdout) whose format is:
			* For valid JS files: <fileName>: valid JavaScript
			* For malformed JS files: <fileName>: malformed JavaScript
			* For not JS files: <fileName>: not JavaScript
	'''
	
	parser = argparse.ArgumentParser(description='Given a list of repositories or files paths, indicate whether the files are either valid, malformed or if they are no JavaScript.'); # Creating an ArgumentParser object
	# The ArgumentParser object holds all the information necessary to parse the command line into Python data types.
	
	parser.add_argument('--f', metavar='FILE', nargs='+', help='file to be tested');
	parser.add_argument('--d', metavar='DIR', nargs='+', help='directory to be tested');
		
	args = vars(parser.parse_args());
	
	
	if args['d'] != None:
		for el in args['d']:
			#l = glob.glob(el + '/*.js') + glob.glob(el + '/*.bin'); # Extension in .bin or .js			
			#for givenFile in sorted(l):
				#isJsFile(givenFile);
			for givenFile in sorted(os.listdir(el)):
				isJsFile(el + '/' + givenFile);
	
	if args['f'] != None:
		for givenFile in args['f']:
			isJsFile(givenFile);

		
if __name__ == "__main__": # Executed only if run as a script
	main();
	