
'''
	Preprocesses JS data.
'''

import collections # to order a dictionary
import glob # Unix style pathname pattern expansion
import numpy as np
import os # for OS dependent functionality
#import sys
#sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from
#sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

#import DicoIntToNGrams
#import DicoNGramsToInt
#import DicoOfTokensSlimit
#import DicoOfTokensEsprima
#import DicoOfAstEsprima
import TokensProduction
import NGramsProduction
import NGramsAnalysis
import NGramsRepresentation


def jsToProbaOfNGrams(parser, jsFile = '/home/aurore/Documents/Code/JS-samples1/JS-Samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin', n = 4):
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

	
def dicoOfAllNGrams(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', label = None, n = 4):
	'''
		This function goes through a directory containing several JS files and returns a list containing all the dictionaries
		containing (for each file) the number of occurrences (probability) of each n-gram.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- jsDir: String
			Path of the directory containing the JS files to be analysed. Default: TODO only for Aurore.
		- label: String
			Indicates the label's name of the current data (if any), useful for supervised classification. Default value is None.
		- n: Integer
			Stands for the size of the sliding-window which goes through the previous list. Default value is 4.
			
		-------
		Returns:
		- List of lists
			* List 1:
				Contains one dictionary per JS file:
					Key: tuple representing an n-gram;
					Value: probability of occurrences of a given tuple of n-gram.
					The dictionary corresponds to the analysis of one JS file.
			* List 2:
				Contains the name of the well-formed JS files.
			* List 3:
				Only if Label is not None. Contains the label assigned to all the files in jsDir.
	'''
	
	allProba = [];
	#l = glob.glob(jsDir + '/*.js') + glob.glob(jsDir + '/*.bin'); # Extension in .bin or .js
	# TODO recursive: directories in a directory
	filesStudied = [];
	lab = [];
	
	#for javaScriptFile in sorted(l):
	for javaScriptFile in sorted(os.listdir(jsDir)):
		dicoForHisto = jsToProbaOfNGrams(parser, jsDir + '/' + javaScriptFile, n) # Histogram containing for each n-gram (key) the probability of occurrences (value).
		if dicoForHisto is not None:
			allProba.append(dicoForHisto); # Store all the dictionaries in a list (this way, we go only once through the JS files).
			filesStudied += [jsDir + '/' + javaScriptFile]; # Store the name of the valid JS files.
			if label is not None and label is not []:
				lab += [label]; # Store the label of the valid JS files. It is duplicated so that the information from allProba[i], filesStudied[i] and lab[i] 
			#corresponds to the same file.
	return ([allProba] + [filesStudied] + [lab]);
	
	
def simplifiedDicoOfAllNGrams(allProba):
	'''
		From a list containing dictionaries, each containing n-grams with their associated probability, returns a simplified set with only the n-grams 
		whose probability is not null.
				
		-------
		Parameter:
		- allProba: List of Dictionaries.
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			One dictionary corresponds to the analysis of one JS file.
			
		-------
		Returns:
		- Set
			Contains tuples representing n-grams whose probability of occurrences is not null.
	'''
	allProba
	nGramList = [i.keys() for i in allProba]; # Store all the n-grams present in the list of dictionaries 'allProba'.
	nGramUnique = set();
	for nGram in nGramList:
		nGramUnique.update(nGram); # Keep only one occurrence for each n-gram. The n-grams which were not in 'allProba' list are not in this set either. It is a 
		#simplification/projection
		# to not consider the huge amount of all possible n-grams, but rather only those that are used.

	return nGramUnique;



def jsToProbaOfNGramsComplete(dicoJS, simplifiedListNGrams, dicoNgramIint, label = None):
	'''
		Mixes the information about one JS file contained in a dictionary (the probability of encountering an n-gram, provided the probability is not null)
		and the set of n-grams present in the JS corpus considered to produce a vector storing for these n-grams their probability.
				
		-------
		Parameters:
		- dicoJS: Dictionary
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			The dictionary corresponds to the analysis of one valid JS file.
		- simplifiedListNGrams: Set
			Contains tuples representing n-grams whose probability of occurrences is not null.
		- dicoNgramIint: Dictionary
			Key: N-gram;
			Value: Unique integer.
		- label: String
			Indicates the label's name of the current data (if any), useful for supervised classification. Default value is None.
		
		-------
		Returns:
		- Vector
			Contains at position i the probability of encountering the n-gram mapped to the integer i (see the complete mapping in DicoNGramsToInt.py).
	'''
	
	i = 0;
	#if label != None and label != []:
		#i = 1; # To have a vector with one extra space for the label
	vectNGramsProba = np.zeros(len(dicoNgramIint) + i);	
	for key in dicoJS: # Key = n-gram
		if key in simplifiedListNGrams: # Simplification so as not to consider n-grams that never appear
			vectNGramsProba[NGramsRepresentation.nGramToInt(dicoNgramIint, key)] = dicoJS[key]; # We use the mapping int/n-gram to store the proba of an 
			#n-gram at a 
			#given place in a vector.

	return vectNGramsProba;
	


def printProbaOfNGramsMatrix(allProba, simplifiedListNGrams, dicoNgramIint):
	'''
		Stores for each file in a JS corpus (one file per row), the probability of encountering every one of the n-grams present in the corpus 
		(one n-gram per column).
				
		-------
		Parameters:
		- allProba: List of Dictionaries.
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			One dictionary corresponds to the analysis of one JS file.
		- simplifiedListNGrams: Set
			Contains tuples representing n-grams whose probability of occurrences is not null.
		- dicoNgramIint: Dictionary
			Key: N-gram;
			Value: Unique integer.
			
		-------
		Returns:
		- Matrix
			Contains for each JS file studied (one per row) the probability of occurrences of all the n-gram encountered in the JS corpus considered.
	'''
	
	i = 1;
	nbSamples = len(allProba); # Number of well-formed JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamples + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS file
	
	for dicoJS in allProba: # Dico for one JS file, key = n-gram and value = proba
		vectNGramsProba = jsToProbaOfNGramsComplete(dicoJS, simplifiedListNGrams, dicoNgramIint); # Contains at position i the probability of encountering 
		#the n-gram mapped to the integer i (see the complete mapping in DicoNGramsToInt.py).
		matrixAllNGramsProba[i] = vectNGramsProba;
		i += 1;

		
	return matrixAllNGramsProba;



#####################################################################################

# Depreciated. Old function to create the file for Weka/xcluster.
# Now it is split in 3 functions: one which creates a line of the matrix, one which returns the complete matrix, and one which creates the file.

"""
def saveFile(parser, allProba, filesStudied, fileDir = '/home/aurore/Documents/Code/MatrixFiles/', classifier = 'Weka', n = 4):
	'''
		From a list containing dictionaries, each containing n-grams with their associated probability, return a simplified set with only the n-grams 
		whose probability is not null.
				
		-------
		Parameters:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- allProba: List of Dictionaries.
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			One dictionary corresponds to the analysis of one JS file.
		- filesStudied: List of Strings
			Contains the name of the well-formed JS files.
		- fileDir: String
			Path of the directory to store the csv/txt files for Weka/xcluster. Default: TODO only for Aurore.
		- classifier: String
			Either 'Weka' or 'xcluster'. Default value is 'Weka'.
		- n: Integer
			Stands for the size of the sliding-window which goes through the previous list. Default value is 4.
			
		-------
		Returns:
		- File
			Contains for each JS file studied the probability of occurrences of all the n-gram encountered in the JS corpus considered.
	'''
	
	dico = TokensProduction.dicoUsed(parser); # Dictionary used, according to the parser selected.

	i = 1;
	nbTokens = len(dico); # Number of tokens
	nbSamples = len(allProba); # Number of well-formed JS file samples
	matrixAllNGramsProba = [[] for j in range(nbSamples + 1)]; # Matrix creation: column = n-grams and row = proba of n-gram for a given JS file
	
	simplifiedListNGrams = simplifiedDicoOfAllNGrams(allProba); # Set containing the name of the n-grams present in our JS corpus.
	vectNGramsProba = np.zeros(len(simplifiedListNGrams));
	matrixAllNGramsProba[0] = [i for i,j in enumerate(vectNGramsProba)]; # Structured for xCluster3 and Weka
	NGramsRepresentation.mappingNGramsInt(simplifiedListNGrams); # Update the dictionaries DicoNGramsToInt and DicoIntToNgrams to map int/ngrams.
		# TODO: current problem, the update comes too late, as the previous version of the dictionary has always been imported...
	
	# Directory to store the matrix files
	if not os.path.exists(fileDir):
		os.makedirs(fileDir);
			
	classifFormat = classifierFormat(classifier);
	formatt = classifFormat[0]; # Separator between the value: either ',' or '\t'.
	extension = classifFormat[1]; # File extension: either '.csv' or '.txt'.
		
	expFile = open(fileDir + parser + extension,'w');
	expFile.write('Outlook');
	for j,k in enumerate(vectNGramsProba):
		expFile.write(formatt + str(j));
	expFile.write('\n');
		
	for dicoJS in allProba: # Dico for one JS file, key = n-gram and value = proba
		vectNGramsProba = np.zeros(len(simplifiedListNGrams));	
		for key in dicoJS: # Key = n-gram
			if key in simplifiedListNGrams: # Simplification so as not to consider n-grams that never appear
				vectNGramsProba[NGramsRepresentation.nGramToInt(key)] = dicoJS[key]; # We use the mapping int/n-gram to store the proba of an n-gram at 
				a given place in a vector.
		expFile.write(filesStudied[i-1] + formatt); # Name of the current file
		for el in range(len(vectNGramsProba)-1):
			expFile.write(str(vectNGramsProba[el]) + formatt);
		expFile.write(str(vectNGramsProba[len(vectNGramsProba)-1])); # Last one could not be in the previous loop, otherwise the last character would have 
		been a separator.
		
		print('End line' + str(i));
		expFile.write('\n');

		matrixAllNGramsProba[i] = vectNGramsProba;
		i += 1;
		
	expFile.close();
	print('end');
		
	return matrixAllNGramsProba;
"""

#####################################################################################

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
		Given a dictionary containing the probability of occurrences of some n-grams, store the probability which are over a given threshold in a global 
		dictionary.
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
