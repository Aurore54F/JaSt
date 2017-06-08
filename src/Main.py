#!/usr/bin/python


'''
	Main program, entry point.
'''

import importlib; # To reload updated modules
import argparse # To parse command line arguments
import sys
sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from
sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

#import DicoIntToNGramsSlimit
#import DicoNGramsToIntSlimit
#import DicoIntToNGramsEsprima
#import DicoNGramsToIntEsprima
import DicoIntToNGramsEsprimaAst
import DicoNGramsToIntEsprimaAst

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima

import PreprocessingJsData
import NGramsRepresentation
import FilesForJsClustering



def parsingCommands():

	parser = argparse.ArgumentParser(description='Given a list of repositories or files paths, analyse whether the JS files are either benign or malicious.');
	# Creating an ArgumentParser object
	# The ArgumentParser object holds all the information necessary to parse the command line into Python data types.
	
	parser.add_argument('--f', metavar='FILE', type = str, nargs='+', help='file to be analysed');
	parser.add_argument('--d', metavar='DIR', type = str, nargs='+', help='directory containing the JS files to be analysed');
	parser.add_argument('--l', metavar='LABEL', type = str, nargs='+', help='label for the files to be analysed');
	subparsers = parser.add_subparsers(help='sub-command help')
	
	"""
	# create the parser for the labeling command
	parser_labeling = subparsers.add_parser('labeling', help='data labeling');
	parser_labeling.add_argument('--f', metavar='FILE', type = str, nargs='+', help='file to be analysed');
	parser_labeling.add_argument('--d', metavar='DIR', type = str, nargs='+', help='directory containing the JS files to be analysed');
	parser_labeling.add_argument('--l', metavar='LABEL', type = str, nargs='+', help='label for the file to be analysed');
	"""
	
	parser.add_argument('--p', metavar='PARSER', type = str, nargs=1, choices = ['esprimaAst', 'esprima', 'slimIt'], default = ['esprimaAst'], help='parser\'s name');
	parser.add_argument('--e', metavar='BOOL', type = bool, nargs=1, default = [False], help='produce a csv/txt file for Weka/xcluster');
	parser.add_argument('--c', metavar='CLASSIFIER', type = str, nargs=1, default = ['Weka'], help='classifier\'s name');
	parser.add_argument('--ep', metavar='FILE-PATH', type = str, nargs=1,  default = ['/home/aurore/Documents/Code/MatrixFiles/'], help='path of the directory to store the csv/txt files for Weka/xcluster');
	parser.add_argument('--h', metavar='BOOL', type = bool, nargs=1,  default = [False], help='produce histograms from the JS corpus');
	parser.add_argument('--hp', metavar='FILE-PATH', type = str, nargs=1,  default = ['/home/aurore/Documents/Code/Histograms/'], help='path of the directory to store the histograms');
	parser.add_argument('--u', metavar='BOOL', type = bool, nargs=1,  default = [False], help='indicates whether the dictionary mapping n-grams and integers has to be updated');
	parser.add_argument('--n', metavar='INTEGER', type = int, nargs=1,  default = [4], help='stands for the size of the sliding-window which goes through the previous list');
	#parser.add_argument('--l', metavar='LABEL', type = str, nargs='*',  default = None, help='indicates the label\'s name of the current data (if any), useful for supervised classification');
	# TODO l must be a sub-command <https://docs.python.org/3.3/library/argparse.html#argparse.Namespace>.
	
	# Default, Choices, Required
	
	args = vars(parser.parse_args());
	
	return args;


def handleDirs(allNGrams, directory, labels, parser, n):
	i = 0;
	for jsDir in directory:
		if labels is not None and labels != []:
			preprocess1Dir = PreprocessingJsData.dicoOfAllNGrams(parser, jsDir, labels[i], n); # args = parser, JsDirectory, label, n
		else:
			preprocess1Dir = PreprocessingJsData.dicoOfAllNGrams(parser, jsDir, n = n); # args = parser, JsDirectory, n
		allNGrams[0] += preprocess1Dir[0]; # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a 
		#given tuple of n-gram.
		allNGrams[1] += preprocess1Dir[1]; # Contains the name of the well-formed JS files.
		allNGrams[2] += preprocess1Dir[2]; # Contains the label of the well-formed JS files.
		i += 1;
		#print(allNGrams);
	return allNGrams;


def handleFiles(allNGrams, file, labels, parser, n):
	i = 0;
	for jsFile in file:
			dico = PreprocessingJsData.jsToProbaOfNGrams(parser, jsFile, n); # args = parser, JsDirectory, n
			if dico is not None:
				allNGrams[0].append(dico); # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a 
				#given tuple of n-gram.
				allNGrams[1] += [jsFile]; # Contains the name of the well-formed JS files.
				if labels is not None:
					allNGrams[2] += labels[i]; # Contains the label of the well-formed JS files.
				# TODO check what happens with labels if not all files have one 
				i += 1;
	return allNGrams;
	


args = parsingCommands();

print('\n');
print(args);
print('\n');

if args['d'] == None and args['f'] == None:
	print('Indicate a directory or a JS file to be studied');
	
else:	
	allNGrams = [[] for j in range(3)];
	if args['d'] != None:
		handleDirs(allNGrams, args['d'], args['l'], args['p'][0], args['n'][0]); # Args: directory, labels, parser, n

	if args['f'] != None:
		handleFiles(allNGrams, args['f'], args['l'], args['p'][0], args['n'][0]);

	if allNGrams != [[]]:
		allProba = allNGrams[0]; # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a given tuple of n-gram.
		filesStudied = allNGrams[1]; # Contains the name of the well-formed JS files.
		labels = allNGrams[2]; # Contains the label of the well-formed JS files.
		
		print('allProba ' + str(len(allProba)));
		print('filesStudied ' + str(len(filesStudied)));
		print('labels ' + str(len(labels)));
		
		formatt = FilesForJsClustering.classifierFormat(args['c'][0])[0]; # Separator between the value: either ',' or '\t' (arg = classifier).
		extension = FilesForJsClustering.classifierFormat(args['c'][0])[1]; # File extension: either '.csv' or '.txt' (arg = classifier).
		
		simplifiedListNGrams = PreprocessingJsData.simplifiedDicoOfAllNGrams(allProba); # Set containing the name of the n-grams present in our JS corpus.
		
		if args['u'][0] == True:
			NGramsRepresentation.mappingNGramsInt(simplifiedListNGrams); # Update the dictionaries DicoNGramsToInt and DicoIntToNgrams to map int/ngrams.
				
		#importlib.reload(DicoNGramsToInt);
				
		if args['h'][0] == True:
			FilesForJsClustering.saveProbaOfNGramsHisto(args['p'][0], allProba, filesStudied, histoDir = args['hp'][0]); # Production of the histograms.
				
		if args['e'][0] == True:
			#saveFile(parser, allProba, filesStudied, fileDir, classifier, n); # Production of the file for Weka/xcluster.
			print('Labels ' + str(len(labels)));
			dicoNGramsToInt = NGramsRepresentation.dicoUsed(args['p'][0]);
			FilesForJsClustering.saveProbaOfNGramsFileHeader(args['p'][0], allProba, simplifiedListNGrams, dicoNGramsToInt, formatt, extension, 
															args['ep'][0], labels);
			#TODO loop on the function below
			FilesForJsClustering.saveProbaOfNGramsFileContent(args['p'][0], allProba, simplifiedListNGrams, dicoNGramsToInt, filesStudied, formatt, 
															extension, args['ep'][0], labels);
