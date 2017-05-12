
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

simplifiedDico = {}
cpt = 0


def jsToProbaOfTokens(parser, jsFile = '/home/aurore/Documents/Code/JS-samples1/JS-Samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin', n = 4):
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
	if numbersList == []:
		print('Empty');
	matrixNGrams = NGrams.nGramsList(numbersList, n);
	#prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
	dicoOfOccurrences = NGrams.countSetsOfNGrams(matrixNGrams);
	
	if dicoOfOccurrences is not None:
		orderedDico = collections.OrderedDict(sorted(dicoOfOccurrences.items()));
	
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
	

def simplifyMatrix(dicoOfOccurrences, threshold = 0):
	'''
		Given a dictionary containing the probability of occurrences of some n-grams, store the probability which are over a given threshold in a global dictionary.
		Format: key = n-gram and value = [nb, probaSAmple1, probaSample2,...].
		#Coud not work.
		Given a dictionary containing the probability of occurrences of some n-grams, associate each n-gram, provided its probability is not null, to an integer.
		Format: key = n-gram and value = nb, where nb corresponds to the position of the n-gram in the matrix of probabilities, see main program.
	'''	
	global cpt;
	global simplifiedDico;
	
	if dicoOfOccurrences is not None:
		for key in dicoOfOccurrences:
			if dicoOfOccurrences[key] > threshold:
				if key not in simplifiedDico:
					#simplifiedDico[key] = [cpt,dicoOfOccurrences[key]];
					simplifiedDico[key] = cpt;
				#else:
					#simplifiedDico[key].append(dicoOfOccurrences[key]);
					cpt = cpt + 1;
		#return simplifiedDico;
	

def mainSimplified(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', exportedFile = True, classifier = 'Weka', fileDir = '/home/aurore/Documents/Code/MatrixFiles/',
	histo = True, histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
		
		This function ....
		
		@param parser: string with name of the parser to use
		@param jsDir...
		@return: ...
	'''
	global simplifiedDico;
	simplifiedDico = {};
	global cpt;
	cpt = 0;
	
	global notJs;
	global structureError;
	notJs = [];
	structureError = [];
	
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
	l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	nbSamples = len(l); # Number of JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamples + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS files
	
	#print(simplifiedDico);
	where = 0;
	for javaScriptFile in sorted(l):
		where = where + 1;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		#print(simplifiedDico);
		simplifyMatrix(dicoForHisto);
		#print(simplifiedDico);
		print(where);
		print(javaScriptFile);
	vectNGramsProba = np.zeros(len(simplifiedDico));
	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured for xCluster3 and Weka
	#print(collections.OrderedDict(sorted(simplifiedDico.items())));
	return collections.OrderedDict(sorted(simplifiedDico.items()));
	
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
		expFile.write('\n');
		
	for javaScriptFile in sorted(l):
		vectNGramsProba = np.zeros(len(simplifiedDico));
		#print(os.path.join(javaScriptFile));
		if histo == True:
			figPath =  histoDir + histoFilePart1 + str(i) + histoFilePart3;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		
		if histo == True:
			Histogram.histoFromDico(dicoForHisto, figPath, title = javaScriptFile);

		if dicoForHisto is not None:
			for key in dicoForHisto:
				vectNGramsProba[simplifiedDico[key]] = dicoForHisto[key];
		
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
		
	print(notJs);
	print(structureError);
	 	
	#return matrixAllNGramsProba;
	


def mainForClassification(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', fileDir = '/home/aurore/Documents/Code/MatrixFiles/', n = 4):
	'''
		Main program, entry point.
	'''
	global simplifiedDico;
	simplifiedDico = {};
	global cpt;
	cpt = 0;
	
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
	benignSamples = glob.glob(jsDir + '/*.js');
	maliciousSamples = glob.glob(jsDir + '/*.bin');
	nbSamplesM = len(maliciousSamples); # Number of malicious JS file samples
	nbSamplesB = len(benignSamples); # Number of benign JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamplesM + nbSamplesB + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS files
	
	where = 0;
	for javaScriptFile in sorted(maliciousSamples + benignSamples):
		where = where + 1;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		simplifyMatrix(dicoForHisto);
	vectNGramsProba = np.zeros(len(simplifiedDico) + 1);
	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured Weka
	#print(collections.OrderedDict(sorted(simplifiedDico.items())));
	
	# Directory to store the matrix files
	if not os.path.exists(fileDir):
		os.makedirs(fileDir);
	
	expFile = open(fileDir + parser + '.csv','w');
	expFile.write('Outlook');
	for j,k in enumerate(vectNGramsProba):
		expFile.write(',' + str(j));
	expFile.write('\n');
		
	for javaScriptFile in sorted(maliciousSamples):
		vectNGramsProba = np.zeros(len(simplifiedDico));
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);

		if dicoForHisto is not None:
			for key in dicoForHisto:
				vectNGramsProba[simplifiedDico[key]] = dicoForHisto[key];

			expFile.write(javaScriptFile + ',');
			for el in range(len(vectNGramsProba)):
				expFile.write(str(vectNGramsProba[el]) + ',');
			expFile.write('Malicious');
			print('End line' + str(i));
			expFile.write('\n');

			matrixAllNGramsProba[i] = vectNGramsProba;
			i += 1;
			
	for javaScriptFile in sorted(benignSamples):
		vectNGramsProba = np.zeros(len(simplifiedDico));
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);

		if dicoForHisto is not None:
			for key in dicoForHisto:
				vectNGramsProba[simplifiedDico[key]] = dicoForHisto[key];

			expFile.write(javaScriptFile + ',');
			for el in range(len(vectNGramsProba)):
				expFile.write(str(vectNGramsProba[el]) + ',');
			expFile.write('Benign');
			print('End line' + str(i));
			expFile.write('\n');

			matrixAllNGramsProba[i] = vectNGramsProba;
			i += 1;
		
	expFile.close();
	print('end');
		
	#return matrixAllNGramsProba;
	
	
	
	

def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', exportedFile = True, classifier = 'Weka', fileDir = '/home/aurore/Documents/Code/MatrixFiles/',
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
	l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	nbSamples = len(l); # Number of JS file samples
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
		expFile.write('\n');
		
	for javaScriptFile in sorted(l):
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
