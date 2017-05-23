#!/usr/bin/python


'''
	Main program, entry point.
'''

import importlib; # To reload updated modules
import argparse # To parse command line arguments
import sys
sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from
sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

import DicoIntToNGrams
import DicoNGramsToInt
import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima
import PreprocessingJsData
import NGramsRepresentation
import FilesForJsClustering



parser = argparse.ArgumentParser(description='Given a list of repositories or files paths, analyse whether the JS files are either benign or malicious.');
# Creating an ArgumentParser object
# The ArgumentParser object holds all the information necessary to parse the command line into Python data types.

parser.add_argument('--f', metavar='FILE', type = str, nargs='+', help='file to be analysed');
parser.add_argument('--d', metavar='DIR', type = str, nargs='+', help='directory containing the JS files to be analysed');

parser.add_argument('--p', metavar='PARSER', type = str, nargs=1, choices = ['esprimaAst', 'esprima', 'slimIt'], default = 'esprimaAst', help='parser\'s name');
parser.add_argument('--e', metavar='BOOL', type = bool, nargs=1, default = True, help='produce a csv/txt file for Weka/xcluster');
parser.add_argument('--c', metavar='CLASSIFIER', type = str, nargs=1, default = 'Weka', help='classifier\'s name');
parser.add_argument('--ep', metavar='FILE-PATH', type = str, nargs=1,  default = '/home/aurore/Documents/Code/MatrixFiles/', help='path of the directory to store the csv/txt files for Weka/xcluster');
parser.add_argument('--h', metavar='BOOL', type = bool, nargs=1,  default = True, help='produce histograms from the JS corpus');
parser.add_argument('--hp', metavar='FILE-PATH', type = str, nargs=1,  default = '/home/aurore/Documents/Code/Histograms/', help='path of the directory to store the histograms');
parser.add_argument('--n', metavar='INTEGER', type = int, nargs=1,  default = 4, help='stands for the size of the sliding-window which goes through the previous list');
#parser.add_argument('--l', metavar='LABEL', type = str, nargs='*',  default = None, help='indicates the label\'s name of the current data (if any), useful for supervised classification');
# TODO l must be a sub-command <https://docs.python.org/3.3/library/argparse.html#argparse.Namespace>.

# Default, Choices, Required

args = vars(parser.parse_args());

print(args);


if args['d'] == None and args['f'] == None:
	print('Indicate a directory or a JS file to be studied');
	
else:	
	allNGrams = [[] for j in range(2)];
	
	if args['d'] != None:
		for jsDir in args['d']:
			preprocess1Dir = PreprocessingJsData.dicoOfAllNGrams(args['p'], jsDir, args['n']); # args = parser, JsDirectory, n
			allNGrams[0] += preprocess1Dir[0]; # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a 
			#given tuple of n-gram.
			allNGrams[1] += preprocess1Dir[1]; # Contains the name of the well-formed JS files.
	
	if args['f'] != None:
		for jsFile in args['f']:
			dico = PreprocessingJsData.jsToProbaOfNGrams(args['p'], jsFile, args['n']); # args = parser, JsDirectory, n
			if dico is not None:
				allNGrams[0].append(dico); # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a 
				#given tuple of n-gram.
				allNGrams[1] += [jsFile]; # Contains the name of the well-formed JS files.

	if allNGrams != [[]]:
		allProba = allNGrams[0]; # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a given tuple of n-gram.
		filesStudied = allNGrams[1]; # Contains the name of the well-formed JS files.
	
		formatt = FilesForJsClustering.classifierFormat(args['c'])[0]; # Separator between the value: either ',' or '\t' (arg = classifier).
		extension = FilesForJsClustering.classifierFormat(args['c'])[1]; # File extension: either '.csv' or '.txt' (arg = classifier).
				
		simplifiedListNGrams = PreprocessingJsData.simplifiedDicoOfAllNGrams(allProba); # Set containing the name of the n-grams present in our JS corpus.
		NGramsRepresentation.mappingNGramsInt(simplifiedListNGrams); # Update the dictionaries DicoNGramsToInt and DicoIntToNgrams to map int/ngrams.
				
		importlib.reload(DicoNGramsToInt);
				
		if args['h'] == True:
			FilesForJsClustering.saveProbaOfNGramsHisto(args['p'], allProba, filesStudied, histoDir = args['hp']); # Production of the histograms.
				
		if args['e'] == True:
			#saveFile(parser, allProba, filesStudied, fileDir, classifier, n); # Production of the file for Weka/xcluster.
			FilesForJsClustering.saveProbaOfNGramsFileHeader(args['p'], allProba, simplifiedListNGrams, DicoNGramsToInt.dicoNGramsToInt, formatt, extension, args['ep']);
			#TODO loop on the function below
			FilesForJsClustering.saveProbaOfNGramsFileContent(args['p'], allProba, simplifiedListNGrams, DicoNGramsToInt.dicoNGramsToInt, filesStudied, formatt, 
															extension, args['ep'], label = 'Test');
