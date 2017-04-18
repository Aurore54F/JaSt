
'''
	Producing n-grams from tokens and dealing with them.
'''

from itertools import product # for the cartesian product


def nGramsList(numbersList, n = 4):
	'''
		Given a list of numbers, produce every possible n-gram (configurable) and store them in a matrix.
	'''
	if (n < 1 or n >= (len(numbersList))):
		print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)');
		return;
		
	else:
		matrixAllNGrams = [[] for j in range(len(numbersList) - (n - 1))];
		for j in range(len(numbersList) - (n - 1)): # Loop on all the n-grams
			matrixAllNGrams[j] = [numbersList[j + i] for i in range(n)]; # Loop on the components of a given n-gram
				
			matrixAllNGrams[j] = tuple(matrixAllNGrams[j]); # Stored in tuples as they are immutable (lists are not; strings are, but for every op in a string,
			 #a new string is created). I needed an immutable type since it will be used as key in a dictionary.

		return matrixAllNGrams;


def nGramsCsv(numbersList, n = 4, filePath = 'nGram.csv'):
	'''
		Given a list of numbers, produce every possible n-gram (configurable) and store them in a CSV file.
	'''
	if (n < 1 or n >= (len(numbersList))):
		print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)');
		return;
		
	else:
		csvFile = open(filePath,'w');
		for j in range(len(numbersList) - (n - 1)):
			csvFile.write(str(numbersList[j]));
			for i in range(n - 1):
				csvFile.write(',' + str(numbersList[j + i + 1]));
			csvFile.write('\n');
			
		csvFile.close();


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
 
 

def allPossibleNGrams(dico, n = 4):
	'''
		Produce all the possible combinations of n-grams using the values stored either in DicoOfTokensSlimit.py or DicoOfTokensEsprima.py.
	'''

	l = [str(dico[key]) for key in dico]; # List containing all the numbers associated with a token
	
	listNGrams = [i for i in product(l, repeat = n)] # Cartesian product
	print('Theorie: ' + str(len(l)**n) + '\nReality: ' + str(len(listNGrams)));
	
	return listNGrams;


def nGramToInt(nMax, nGram):
	'''
		Convert an n-gram into an int.
	'''
	return sum(nMax**i*j for i,j in enumerate(nGram));


def intToNGram(nMax, i, n = 4):
	'''
		Convert an int into an n-gram.
	'''
	return tuple([int(i/(nMax**j) % nMax) for j in range(n)]);
