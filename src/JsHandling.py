
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
	


def matrixOfProbaToDoc(matrix, filePath, storage = 'txt'):
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
		print('Line' + str(j));
		if storage.lower() == 'txt':
			csvFile.write('Experiment' + str(j) + formatt);
		print('LineBis' + str(j));
		for el in matrix[j]:
			#csvFile.write(str(el) + '\t\t\t\t\t\t');
			csvFile.write(str(el) + formatt);
		print('After el');
		csvFile.write('\n');
			
	csvFile.close();
	print('end');
	

def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples', histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
	'''

	# Directory to store the histograms files
	if os.path.exists(histoDir):
		shutil.rmtree(histoDir);
	os.makedirs(histoDir);
	
	
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimit.tokensDico;
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
	elif parser.lower() == 'esprimaast':
		dico = DicoOfAstEsprima.astDico;
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;

	histoFilePart1 = 'Histogram';
	histoFilePart3 = '.png';
	i = 1;
	
	
	nbTokens = len(dico);	
	matrixAllNGramsProba = [[] for j in range(12)]; # TODO hardcoded = nb samples + 1
	vectNGramsProba = np.zeros(nbTokens**n);

	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured for xCluster3
		
	for javaScriptFile in glob.glob(jsDir + '/*.bin'):
		vectNGramsProba = np.zeros(nbTokens**n);
		#print(os.path.join(javaScriptFile));
		figPath =  histoDir + histoFilePart1 + str(i) + histoFilePart3;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		#jsTitle = javaScriptFile.split('/');
		Histogram.histoFromDico(dicoForHisto, figPath, title = javaScriptFile);
		
		for key in dicoForHisto:
			vectNGramsProba[NGrams.nGramToInt(nbTokens,key)] = dicoForHisto[key];
	
		matrixAllNGramsProba[i] = vectNGramsProba;
		i += 1;
			
	return matrixAllNGramsProba;
