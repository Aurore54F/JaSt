
'''
	Dealing with files.
'''

import os # To create repositories
import importlib
import sys
sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from
sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

import PreprocessingJsData
import NGramsAnalysis
import NGramsRepresentation

import DicoIntToNGrams
import DicoNGramsToInt
import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima



def classifierFormat(classifier = 'Weka'):
	'''
		Format of the soon to be exported file, according to the classifier it will be given to.
				
		-------
		Parameter:
		- classifier: String
			Either 'Weka' or 'xcluster'. Default value is 'Weka'.
			
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



def saveProbaOfNGramsHisto(parser, allProba, filesStudied, histoDir = '/home/aurore/Documents/Code/Histograms/'):
	'''
		From a list containing dictionaries, each containing n-grams (abscissa) with their associated probability (ordinate), saves the corresponding histograms.
				
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
		- histoDir: String
			Path of the directory to store the histograms. Default: TODO only for Aurore.
			
		-------
		Returns:
		- Files
			The number of .png files returned (i.e. of histograms) corresponds to the number of valid JS files (i.e. len(allProba) = len(filesStudied)).
	'''
	
	# Directory to store the histograms files
	if not os.path.exists(histoDir):
		os.makedirs(histoDir);
	
	i = 1;	
	histoFilePart1 = 'Histo' + parser;
	histoFilePart3 = '.png';
		
	for dico in allProba: # Data for the histogram (i.e. n-gram with occurrence);
		figPath =  histoDir + histoFilePart1 + str(i) + histoFilePart3;
		NGramsAnalysis.histoFromDico(dico, figPath, title = filesStudied[i-1]); # Saving an histogram in png format.
		i += 1;

	
def saveProbaOfNGramsFileHeader(parser, allProba, simplifiedListNGrams, dicoNgramIint, formatt, extension, 
							fileDir = '/home/aurore/Documents/Code/MatrixFiles/'):
	'''
		Writes the header (i.e. columns labeling) of the file for Weka/xcluster.
				
		-------
		Parameters:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- allProba: List of Dictionaries.
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			One dictionary corresponds to the analysis of one JS file.
		- simplifiedListNGrams: Set
			Contains tuples representing n-grams whose probability of occurrences is not null.
		- dicoNgramIint: Dictionary
			Key: N-gram;
			Value: Unique integer.
		- formatt: String
			Separator (either ',' or '\t').
		- extension: String
			File extension (either '.csv' or '.txt').
		- fileDir: String
			Path of the directory to store the csv/txt files for Weka/xcluster. Default: TODO only for Aurore.
		
		-------
		Returns:
		- File
			Contains the header for Weka/xcluster (i.e. labels/numbers the columns).
	'''
	
	# Directory to store the matrix files
	if not os.path.exists(fileDir):
		os.makedirs(fileDir);
	
	expFile = open(fileDir + parser + extension,'w');
	expFile.write('Outlook');
	
	vectNGramsProba = PreprocessingJsData.jsToProbaOfNGramsComplete(allProba[0], simplifiedListNGrams, dicoNgramIint); # allProba[0] being a dictionary representing 
	#the analysis of one JS file (i.e. n-gram with associated probability).
	# vectNGramsProba contains at position i the probability of encountering the n-gram mapped to the integer i (see the complete mapping in DicoNGramsToInt.py).
	for j,k in enumerate(vectNGramsProba):
		expFile.write(formatt + str(j)); # Columns labeling
	expFile.write('\n');
	
	#expFile.close();
	
	
def saveProbaOfNGramsFileContent(parser, allProba, simplifiedListNGrams, dicoNgramIint, filesStudied, formatt, extension, 
								fileDir = '/home/aurore/Documents/Code/MatrixFiles/', label = None):
	'''
		Writes in a file, for each JS file studied (row), the probability of occurrences of all the n-gram (column) encountered in the JS corpus considered.
				
		-------
		Parameters:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- allProba: List of Dictionaries.
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
			One dictionary corresponds to the analysis of one JS file.
		- simplifiedListNGrams: Set
			Contains tuples representing n-grams whose probability of occurrences is not null.
		- dicoNgramIint: Dictionary
			Key: N-gram;
			Value: Unique integer.	
		- filesStudied: List of Strings
			Contains the name of the well-formed JS files.
		- formatt: String
			Separator (either ',' or '\t').
		- extension: String
			File extension (either '.csv' or '.txt').
		- fileDir: String
			Path of the directory to store the csv/txt files for Weka/xcluster. Default: TODO only for Aurore.
		- label: String
			Indicates the label's name of the current data (if any), useful for supervised classification. Default value is None.
		
		-------
		Returns:
		- File
			Contains for each JS file studied (row) the probability of occurrences of all the n-gram (column) encountered in the JS corpus considered.
	'''
	
	i = 1;

	# Directory to store the matrix files
	if not os.path.exists(fileDir):
		print('File does not exist.');
		
	expFile = open(fileDir + parser + extension,'a');
	
	#for dicoJS in allProba: # Dico for one JS file, key = n-gram and value = proba
	for dicoJS in allProba: # Dico for one JS file, key = n-gram and value = proba
		vectNGramsProba = PreprocessingJsData.jsToProbaOfNGramsComplete(dicoJS, simplifiedListNGrams, dicoNgramIint);
		expFile.write(filesStudied[i-1] + formatt); # Name of the current file
		for el in range(len(vectNGramsProba)-1):
			expFile.write(str(vectNGramsProba[el]) + formatt);
		expFile.write(str(vectNGramsProba[len(vectNGramsProba)-1])); # Last one could not be in the previous loop, otherwise the last character would have been a separator.
		if label is not None:
			expFile.write(formatt + label);
		
		print('End line' + str(i));
		expFile.write('\n');

		i += 1;
		
	expFile.close();
	print('end');
	
	
def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples1/JS-Samples', exportedFile = True, classifier = 'Weka', 
		fileDir = '/home/aurore/Documents/Code/MatrixFiles/', histo = True, histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
				
		-------
		Parameters:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
		- jsDir: String
			Path of the directory containing the JS files to be analysed. Default: TODO only for Aurore.
			TODO: glob.glob(allJsDir).
		- exportedFile: Boolean
			True to call function 'saveFile' and therefore produce a csv/txt file for Weka/xcluster. Default value is True.
		- classifier: String
			Either 'Weka' or 'xcluster'. Default value is 'Weka'.
		- fileDir: String
			Path of the directory to store the csv/txt files for Weka/xcluster. Default: TODO only for Aurore.
		- histo: Boolean
			True to call function 'saveHisto' and therefore produce histograms from the JS corpus. Default value is True.
		- histoDir: String
			Path of the directory to store the histograms. Default: TODO only for Aurore.
		- n: Integer
			Stands for the size of the sliding-window which goes through the previous list. Default value is 4.
			
		-------
		Returns:
		- Histogram files (if enabled)
			The number of .png files returned (i.e. of histograms) corresponds to the number of valid JS files in the corpus.
		- File
			Contains for each JS file studied the probability of occurrences of all the n-gram encountered in the JS corpus considered.
	'''
	
	allNGrams = PreprocessingJsData.dicoOfAllNGrams(parser, jsDir, n);
	
	if allNGrams != [[]]:
		allProba = allNGrams[0]; # Contains one dictionary per JS file: key = tuple representing an n-gram and value = probability of occurrences of a given tuple of n-gram.
		filesStudied = allNGrams[1]; # Contains the name of the well-formed JS files.
		
		formatt = classifierFormat(classifier)[0]; # Separator between the value: either ',' or '\t'.
		extension = classifierFormat(classifier)[1]; # File extension: either '.csv' or '.txt'.
		
		simplifiedListNGrams = PreprocessingJsData.simplifiedDicoOfAllNGrams(allProba); # Set containing the name of the n-grams present in our JS corpus.
		NGramsRepresentation.mappingNGramsInt(simplifiedListNGrams); # Update the dictionaries DicoNGramsToInt and DicoIntToNgrams to map int/ngrams.
		
		importlib.reload(DicoNGramsToInt);
		
		if histo == True:
			saveProbaOfNGramsHisto(parser, allProba, filesStudied, histoDir = histoDir); # Production of the histograms.
		
		if exportedFile == True:
			#saveFile(parser, allProba, filesStudied, fileDir, classifier, n); # Production of the file for Weka/xcluster.
			saveProbaOfNGramsFileHeader(parser, allProba, simplifiedListNGrams, DicoNGramsToInt.dicoNGramsToInt, formatt, extension, fileDir);
			#TODO loop on the function below
			saveProbaOfNGramsFileContent(parser, allProba, simplifiedListNGrams, DicoNGramsToInt.dicoNGramsToInt, filesStudied, formatt, extension, fileDir, label = None);
			

	