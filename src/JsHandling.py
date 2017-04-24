
'''
	Main program, entry point.
'''

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima
import TokensProduction
import NGrams
import Histogram

import collections # to order a dictionary
import shutil
import glob # Unix style pathname pattern expansion
import os
import numpy as np


def jsToProbaOfTokens(parser, jsFile = '/home/aurore/Documents/Code/JS-samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin', n = 4):
	'''
		Production of a dictionary containing the number of occurrences (probability) of each n-gram (default: 4-gram) from a given JS file.
	'''
	
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimit.tokensDico;
		tokensList = TokensProduction.tokensUsedSlimit(jsFile);
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
		tokensList = TokensProduction.tokensUsedEsprima(jsFile);
	elif parser.lower() == 'esprimaast':
		dico = DicoOfAstEsprima.astDico;
		tokensList = TokensProduction.astUsedEsprima(jsFile);
		
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
		
	numbersList = TokensProduction.tokensToNumbers(dico, tokensList);	
	matrixNGrams = NGrams.nGramsList(numbersList, n);
	#prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
	dicoOfOccurrences = NGrams.countSetsOfNGrams(matrixNGrams);
	orderedDico = collections.OrderedDict(sorted(dicoOfOccurrences.items()))
	
	#Histogram.histoFromDico(orderedDico, './Histo.png', title = jsFile);
	
	return orderedDico;
	


def matrixOfProbaToDoc(matrix, filePath, storage = 'csv'):
	'''
		Given a matrix, write its content in a CSV file.
	'''
	csvFile = open(filePath,'w');
	if storage.lower() == 'csv':
		formatt = ',';
	elif storage.lower() == 'txt':
		formatt = '\t';
	else:
		print("Error on the file format. Indicate csv' or 'txt'.");
		return;
	
	for j in range(len(matrix)): # Number of lines, i.e. of experiments
		if storage.lower() == 'txt':
			csvFile.write('Experiment' + str(j) + formatt);
		for el in range(len(matrix[j]) - 1):
			#csvFile.write(str(el) + '\t\t\t\t\t\t');
			csvFile.write(str(matrix[j][el]) + formatt);
		csvFile.write(str(matrix[j][len(matrix[j])-1]));
		print('After line ' + str(j));
		csvFile.write('\n');
			
	csvFile.close();
	print('end');
	

def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples', exportedFile = True, classifier = 'Weka', fileDir = '/home/aurore/Documents/Code/MatrixFiles/',
	histo = True, histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
	'''

	if histo == True:
		# Directory to store the histograms files
		if not os.path.exists(histoDir):
			os.makedirs(histoDir);
		histoFilePart1 = 'Histo' + parser;
		histoFilePart3 = '.png';
	
	# Dictionary used, according to the chosen parser
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimit.tokensDico;
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
	elif parser.lower() == 'esprimaast':
		dico = DicoOfAstEsprima.astDico;
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;

	i = 1;
	nbTokens = len(dico); # Number of tokens
	nbSamples = len(glob.glob(jsDir + '/*.bin')); # Number of JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamples + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS files
	vectNGramsProba = np.zeros(nbTokens**n);
	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured for xCluster3 and Weka
	
	if exportedFile == True:
		# Directory to store the matrix files
		if not os.path.exists(fileDir):
			os.makedirs(fileDir);
		if classifier.lower() == 'weka':
			formatt = ',';
			extension = '.csv';
		elif classifier.lower() == 'xcluster':
			formatt = '\t';
			extension = '.txt';
		else:
			print("Error on the classifier name. Please indicate either 'Weka' or 'Xcluster'.");
			return;
		expFile = open(fileDir + parser + extension,'w');
		expFile.write('Outlook');
		for j,k in enumerate(vectNGramsProba):
			expFile.write(formatt + str(j));
		expFile.write(formatt + '\n');
		
	for javaScriptFile in sorted(glob.glob(jsDir + '/*.bin')):
		vectNGramsProba = np.zeros(nbTokens**n);
		#print(os.path.join(javaScriptFile));
		if histo == True:
			figPath =  histoDir + histoFilePart1 + str(i) + histoFilePart3;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		
		if histo == True:
			Histogram.histoFromDico(dicoForHisto, figPath, title = javaScriptFile);
		
		for key in dicoForHisto:
			vectNGramsProba[NGrams.nGramToInt(nbTokens,key)] = dicoForHisto[key];
		
		if exportedFile == True:
			expFile.write(javaScriptFile + formatt);
			for el in range(len(vectNGramsProba)-1):
				expFile.write(str(vectNGramsProba[el]) + formatt);
			expFile.write(str(vectNGramsProba[len(vectNGramsProba)-1]));
			print('End line' + str(i));
			expFile.write('\n');

		matrixAllNGramsProba[i] = vectNGramsProba;
		i += 1;
		
	if exportedFile == True:	
		expFile.close();
	print('end');
		
	return matrixAllNGramsProba;
