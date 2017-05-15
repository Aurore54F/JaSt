
'''
	Main program, entry point.
'''

import collections # to order a dictionary
import shutil
import glob # Unix style pathname pattern expansion
import os # To create repositories
import numpy as np
import sys
sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima
import TokensProduction
import NGramsProduction
import NGramsAnalysis
import NGramsRepresentation


def jsToProbaOfTokens(parser, jsFile = '/home/aurore/Documents/Code/JS-samples1/JS-Samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin', n = 4):
	'''
		Production of a dictionary containing the number of occurrences (probability) of each n-gram (default: 4-gram) from a given JS file.
				
		-------
		Parameters:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- jsFile: String
			Path of the JavaScript file to be analysed. Default: TODO only for Aurore.
		- n: Integer
			Stands for the size of the sliding-window which goes through the previous list. Default value is 4.
			
		-------
		Returns:
		- Dictionary
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			The dictionary corresponds to the analysis of the input JS file.
		- or None if the file either is no JS or malformed.
	'''
	
	dico = TokensProduction.dicoUsed(parser); # Dictionary used, according to the parser selected
	tokensList = TokensProduction.tokensUsed(parser, jsFile); # List of tokens present in the JS file
		
	numbersList = TokensProduction.tokensToNumbers(dico, tokensList); # Tokens converted in numbers
	#if numbersList == []:
		#print('Empty');
	matrixNGrams = NGramsProduction.nGramsList(numbersList, n); # JS file represented through a list of n-grams
	dicoOfOccurrences = NGramsAnalysis.countSetsOfNGrams(matrixNGrams); # Contains the probability of occurrences of the previous n-grams
	
	if dicoOfOccurrences is not None:
		orderedDico = collections.OrderedDict(sorted(dicoOfOccurrences.items()));
		#Histogram.histoFromDico(orderedDico, './Histo.png', title = jsFile);
		
		return orderedDico;


def classifierFormat(classifier = 'Weka'):
	'''
		Format of the soon to be exported file, according to the classifier it will be given to.
				
		-------
		Parameter:
		- classifier: String
			Either 'Weka' or 'xcluster'.
			
		-------
		Returns:
		- List
			Element 1 = formatt: separator (either ',' or '\t');
			Element 2 = extension: file extension (either '.csv' or '.txt').
	'''
	
	if classifier.lower() == 'weka':
		formatt = ',';
		extension = '.csv';
	elif classifier.lower() == 'xcluster':
		formatt = '\t';
		extension = '.txt';
	else:
		print("Error on the classifier name. Please indicate either 'Weka' or 'Xcluster'.");
		return;
	l = [formatt] + [extension];
	return l;
	
	
	
def dicoOfAllNGrams(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', n = 4):
	'''
		This function goes through a directory containing several JS files and returns a list containing all the dictionaries
		containing (for each file) the number of occurrences (probability) of each n-gram.
				
		-------
		Parameter:
		- parser:
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- jsDir:
			Path of the directory containing the JS files to be analysed.
		- n: Integer
			Stands for the size of the sliding-window which goes through the previous list. Default value is 4.
			
		-------
		Returns:
		- List
			Contains one dictionary per JS file:
				Key: tuple representing an n-gram;
				Value: probability of occurrences of a given tuple of n-gram.
				The dictionary corresponds to the analysis of one JS file.
	'''
	
	allProba = [];
	l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	filesStudied = [];
	
	for javaScriptFile in sorted(l):
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Histogram containing for each n-gram (key) the probability of occurrences (value).
		if dicoForHisto is not None:
			allProba.append(dicoForHisto);
			filesStudied += [javaScriptFile];

	return ([allProba] + filesStudied);
	
	
def simplifiedDicoOfAllNGrams(allProba):
	'''
		From a list containing dictionaries, each containing n-grams with their associated probability, return a simplified set with only the n-grams whose probability is not null.
				
		-------
		Parameter:
		- allProba: List of Dictionaries.
			
		-------
		Returns:
		- Set
			Contains tuples representing n-grams.
	'''
	
	nGramList = [i.keys() for i in allProba];
	nGramUnique = set();
	for nGram in nGramList:
		nGramUnique.update(nGram);

	return nGramUnique;


def saveHisto(parser, allProba, filesStudied, histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	
	# Directory to store the histograms files
	print(histoDir);
	
	if not os.path.exists(histoDir):
		os.makedirs(histoDir);
	
	i = 1;	
	histoFilePart1 = 'Histo' + parser;
	histoFilePart3 = '.png';
		
	for dico in allProba: # Data for the histogram (i.e. n-gram with occurrence);
		figPath =  '/home/aurore/Documents/Code/Histograms/' + histoFilePart1 + str(i) + histoFilePart3;
		NGramsAnalysis.histoFromDico(dico, figPath, title = filesStudied[i-1]);
		i += 1;
		
		
def saveFile(parser, allProba, filesStudied, fileDir = '/home/aurore/Documents/Code/MatrixFiles/', classifier = 'Weka', n = 4):
	
	dico = TokensProduction.dicoUsed(parser); # Dictionary used, according to the parser selected

	i = 1;
	nbTokens = len(dico); # Number of tokens
	nbSamples = len(allProba); # Number of well-formed JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamples + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS files
	
	simplifiedListNGrams = simplifiedDicoOfAllNGrams(allProba);
	vectNGramsProba = np.zeros(len(simplifiedListNGrams));
	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured for xCluster3 and Weka
	
	# Directory to store the matrix files
	if not os.path.exists(fileDir):
		os.makedirs(fileDir);
			
	classifFormat = classifierFormat(classifier);
	formatt = classifFormat[0];
	extension = classifFormat[1];
		
	expFile = open(fileDir + parser + extension,'w');
	expFile.write('Outlook');
	for j,k in enumerate(vectNGramsProba):
		expFile.write(formatt + str(j));
	expFile.write('\n');
		
	for dicoJS in allProba:
		vectNGramsProba = np.zeros(len(simplifiedListNGrams));	
		for key in dicoJS:
			if key in simplifiedListNGrams:
				vectNGramsProba[NGramsRepresentation.nGramToInt(key)] = dicoJS[key];
		expFile.write(filesStudied[i-1] + formatt);
		for el in range(len(vectNGramsProba)-1):
			expFile.write(str(vectNGramsProba[el]) + formatt);
		expFile.write(str(vectNGramsProba[len(vectNGramsProba)-1]));
		
		print('End line' + str(i));
		expFile.write('\n');

		matrixAllNGramsProba[i] = vectNGramsProba;
		i += 1;
		
	expFile.close();
	print('end');
		
	return matrixAllNGramsProba;
	

def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', exportedFile = True, classifier = 'Weka', fileDir = '/home/aurore/Documents/Code/MatrixFiles/',
	histo = True, histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
	'''
	
	allNGrams = dicoOfAllNGrams(parser, jsDir, n);
	if allNGrams != [[]]:
		allProba = allNGrams[0];
		filesStudied = allNGrams[1];
	
		if histo == True:
			saveHisto(parser, allProba, filesStudied, histoDir = histoDir, n = n);
		
		if exportedFile == True:
			saveFile(parser, allProba, filesStudied, fileDir, classifier, n);


#####################################################################################

# Depreciated. Old function to write a matrix' content in a CSV/txt file.
# Now we write each line as soon as it is created.

"""	
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
"""	


# Depreciated. Old function to keep only the n-grams used and not store all of them.
# Now we go only once through the JS file, store every n-gram and project them without global variable.

"""	
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
"""	

#####################################################################################
