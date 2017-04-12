
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

import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py


javaScriptFile = '/home/aurore/Documents/Code/JS-samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin';
tokensFile = '/home/aurore/Documents/Code/Tokens.txt';
n = 4;

BINS = 512


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
		print(str(nGrams) + '\t : ' + str(dico[nGrams]) + '\n');
	print('================================');
 
 

def testProg(parser):
	'''
		Test the display of each set of n-gram (for a given JS file) with their number of occurrences.
	'''
	TokenProduction.buildToken(parser, javaScriptFile, tokensFile);
	matrixNGrams = NGram.nGramList(NGram.tokenToNumber(tokensFile, parser), n);
	prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
	
	#return countSetsOfNGrams(matrixNGrams);
	
	
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



def mainProg(parser):
	'''
	Main program, entry point.
	'''

	directoryJS = '/home/aurore/Documents/Code/JS-samples';
	directoryTokens = '/home/aurore/Documents/Code/Token-samples/';
	tokensFilePart1 = 'Tokens';
	tokensFilePart3 = '.txt';
	directoryHistograms = '/home/aurore/Documents/Code/Histograms/';
	tokensFilePart1 = 'Tokens';
	tokensFilePart3 = '.txt';
	n = 4;
	i = 1;
	
	# Directory to store the tokens files
	if os.path.exists(directoryTokens):
		shutil.rmtree(directoryTokens);
	os.makedirs(directoryTokens);
	
	# Directory to store the histograms files
	if os.path.exists(directoryHistograms):
		shutil.rmtree(directoryHistograms);
	os.makedirs(directoryHistograms);
		
		
	for javaScriptFile in os.listdir(directoryJS):
		if javaScriptFile.endswith(".bin"): # TODO other condition or exclusively JS files to be analysed
			#print(os.path.join(directoryJS, javaScriptFile));
			tokensFilePart2 = str(i);
			tokensFile = directoryTokens + tokensFilePart1 + tokensFilePart2 + tokensFilePart3; # Incremental name for each token file
			TokenProduction.buildToken(parser, directoryJS + '/' + javaScriptFile, tokensFile); # Tokens production
			matrixNGrams = NGram.nGramList(NGram.tokenToNumber(tokensFile, parser), n); # Matrix containing every n-gram for a given JS file
			#prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
			dicoForHisto = countSetsOfNGrams(matrixNGrams); # Data for the histogram (i.e. n-gram with occurrence)
			
			plt.bar(range(len(dicoForHisto)), dicoForHisto.values(), align = 'center');
			plt.xticks(range(len(dicoForHisto)),dicoForHisto.keys());
			plt.savefig('Histo.png');
			
			i = i + 1;
			
		# else:
			# print('No JS files to be analysed in this directory ' + directory);


def histogram(dicoForHisto):
	'''
		Histogram presenting the number of occurrences of every n-gram for a given malware.
	'''
	#dico = testProg('esprima');
	#plt.bar(list(dico.keys()),dico.values());
	plt.bar(range(len(dicoForHisto)), dicoForHisto.values(), align = 'center');
	plt.xticks(range(len(dicoForHisto)),dicoForHisto.keys());
	#plt.show();
	#fig = plt.figure();
	plt.savefig('Histo.png');
	#plt.close();
	#fig.savefig('Histo2.pdf');
	'''
		hist, bins = np.histogram(data, bins = bins);
		width = 0,7 * (bins[1] - bins[0]);
		height =  [1,2,5,4];
		center = (bins[:-1] - bins[1:])/2;
		#plt.bar(hist, align = 'center', width = height, height = height);
		plt.bar(hist, align = 'center', width = height, height = height);
		plt.show();
	'''
	
	
	
	

