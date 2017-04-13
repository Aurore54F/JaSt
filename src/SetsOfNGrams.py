
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
import collections

import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py


javaScriptFile = '/home/aurore/Documents/Code/JS-samples/0689067c8130efa6396c35af4ae374aa6d736977.bin';
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
	
	return countSetsOfNGrams(matrixNGrams);
	
	
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


def nGramToInt(nMax, nGram):
	'''
		Convert an n-gram into an int.
	'''
	return sum(nMax**i*j for i,j in enumerate(nGram));

def intToNGram(nMax, i, n):
	'''
		Convert an int into an n-gram.
	'''
	return tuple([int(i/(nMax**j) % nMax) for j in range(n)]);
	

def mainProg(parser):
	'''
	Main program, entry point.
	'''

	directoryJS = '/home/aurore/Documents/Code/JS-samples';
	directoryTokens = '/home/aurore/Documents/Code/Token-samples/';
	tokensFilePart1 = 'Tokens';
	tokensFilePart3 = '.txt';
	directoryHistograms = '/home/aurore/Documents/Code/Histograms/';
	histoFilePart1 = 'Histogram';
	histoFilePart3 = '.png';
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
			
			orderedDico = collections.OrderedDict(sorted(dicoForHisto.items()));

			#print(nGramToInt(10,key));
			#print(dicoForHisto[key]);
			#for i in data:
				#print(i);
			#plt.hist(data, bins = 512);
			
			
			'''
				min_bin = 0
				max_bin = 10000
				
				data = np.zeros(max_bin);
				for key in dicoForHisto:
					data[nGramToInt(10,key)] = dicoForHisto[key];

				bins = np.arange(min_bin, max_bin)
				width = 0.7 * (bins[1] - bins[0]);
				#center = (bins[:-1] + bins[1:]) / 2;

				val, weight = zip(*[(k,v) for k,v in enumerate(data)]);
				#plt.hist(val, weights = weight);

				plt.bar(bins, data, align='center', width=width);
				plt.show();
			'''
			
			
			plt.bar(range(len(orderedDico)), orderedDico.values(), align = 'center');
			plt.xticks(range(len(orderedDico)),(orderedDico.keys()),rotation=90);
			#plt.show();
			#plt.title('Probability of every n-gram for malware' + javaScriptFile);
			#plt.xlabel('N-grams for the malware');
			#plt.ylabel('Probability');
			plt.tight_layout();
			plt.savefig(directoryHistograms + histoFilePart1 + tokensFilePart2 + histoFilePart3);
			plt.clf();
			
			i = i + 1;
			
		# else:
			# print('No JS files to be analysed in this directory ' + directory);


def histogram():
	'''
		Histogram presenting the number of occurrences of every n-gram for a given malware.
	'''

	#plt.bar(range(len(dicoForHisto)), dicoForHisto.values(), align = 'center');
	#plt.xticks(range(len(dicoForHisto)),dicoForHisto.keys());
	#plt.savefig('Histo.png');

	#data = [1,2,3,4,5,6,7,8,9,4,5,3];
	#hist, bins = np.histogram(data, bins=20);
	#print(hist);
	#print(bins);
	#width = 0.7 * (bins[1] - bins[0]);
	#center = (bins[:-1] + bins[1:]) / 2;
	#plt.bar(center, hist, align='center', width=width);
	#plt.show();
	
	#plt.hist(np.array([1,2,3,4,5,6,7,8,9,4,5,3]), bins = 20);
	
	
	data = np.zeros(100);
	for i in range(45):
		data[2*i + 5] = 37;
	'''
		val, weight = zip(*[(k,v) for k,v in enumerate(data)]);
		plt.hist(val, weights = weight);
		plt.show();
	'''
	
	
	
	min_bin = 0
	max_bin = 100

	bins = np.arange(min_bin, max_bin)
	#vals = np.zeros(max_bin - min_bin + 1)

	#for k,v in enumerate(data):
		#vals[k - min_bin] = v

	width = 0.7 * (bins[1] - bins[0]);
	#center = (bins[:-1] + bins[1:]) / 2;

	plt.bar(bins, data, align='center', width=width);
	plt.show();
	
	
	#plt.hist([3,5,3,4,8,6,8,8,8,6,5,3], bins = 20);
	#plt.show();

	
	
	
	

