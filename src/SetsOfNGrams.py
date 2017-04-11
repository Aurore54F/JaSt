
'''
	Main program, entry point.
'''


import TokenProduction
import NGram
import DicoOfTokensSlimIt
import DicoOfTokensEsprima

import os
import shutil
from itertools import product


javaScriptFile = '/home/aurore/Documents/Code/JS-samples/Test.bin';
tokensFile = '/home/aurore/Documents/Code/Tokens.txt';
tokensFileEsprima = '/home/aurore/Documents/Malware/malware_js/samples/GotTokens.txt';
n = 4;


def countSetsOfNGrams(matrixAllNGrams):
	'''
		Given a matrix containing every possible n-gram (for a JavaScript given file), count and store the occurrences of each set of n-gram in a dictionary.
	'''
	dicoOfNGrams = {};
	setsNGrams = len(matrixAllNGrams); # Number of lines of the matrix, i.e. of sets of n-grams
	for j in range(setsNGrams):
		if matrixAllNGrams[j] in dicoOfNGrams:
			dicoOfNGrams[matrixAllNGrams[j]] = dicoOfNGrams[matrixAllNGrams[j]] + 1/setsNGrams; # Normalization to enable future comparisons
		else:
			dicoOfNGrams[matrixAllNGrams[j]] = 1/setsNGrams;
			
	return dicoOfNGrams;
	

def prettyPrintNGramsDico(dico):
	'''
		Print a human-readable content of the n-grams dictionary.
	'''
	print('================================');
	for nGrams in dico:
		print(nGrams + '\t : ' + str(dico[nGrams]) + '\n');
	print('================================');
 
 

def testProg(parser):
	'''
		Test the display of each set of n-gram (for a given JS file) with their number of occurrences.
	'''
	TokenProduction.buildToken(parser, javaScriptFile, tokensFile);
	matrixNGrams = NGram.nGramList(NGram.tokenToNumber(tokensFile, parser), n);
	prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
	
	return matrixNGrams;
	
	
def allPossibleNGrams(parser, n):
	'''
		Produce all the possible combinations of n-grams using the values stored in DicoOfTokens.py.
	'''
	l = [];
	
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimIt.tokensDico;
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
	else:
		print("Error on the parser's name. Indicate 'slimIt' or 'esprima'.");
	
	for key in dico:
		l = l + [str(dico[key])]; # All the number associated with a token
	
	nb = 0;
	for i in product(l, repeat=n): # Cartesian product
		#print(i);
		nb = nb + 1;
	print('Theorie: ' + str(pow(len(l),n)) + '\nReality: ' + str(nb));


#slimIt
def mainProg(parser):
	'''
	Main program, entry point.
	'''

	directoryJS = '/home/aurore/Documents/Code/JS-samples';
	directoryTokens = '/home/aurore/Documents/Code/Token-samples/';
	tokensFilePart1 = 'Tokens';
	tokensFilePart3 = '.txt';
	n = 4;
	i = 1;
	
	if os.path.exists(directoryTokens):
		shutil.rmtree(directoryTokens);
	os.makedirs(directoryTokens);
		
	#dataForHisto = open('DataForHistogramm','w');
	
	for javaScriptFile in os.listdir(directoryJS):
		if javaScriptFile.endswith(".bin"): # TODO other condition or exclusively JS files to be analysed
			#print(os.path.join(directoryJS, javaScriptFile));
			tokensFilePart2 = str(i);
			tokensFile = directoryTokens + tokensFilePart1 + tokensFilePart2 + tokensFilePart3;
			TokenProduction.buildToken(parser, directoryJS + '/' + javaScriptFile, tokensFile);
			matrixNGrams = NGram.nGramList(NGram.tokenToNumber(tokensFile, parser), n);
			prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
			
			
			
			i = i + 1;
			
		# else:
			# print('No JS files to be analysed in this directory ' + directory);
