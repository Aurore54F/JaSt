
'''
	Producing n-grams from tokens.
'''

import DicoOfTokens


def tokenToNumber(tokensFile):
	'''
		Convert a given token in its corresponding number (as indicated in the tokens dictionary).
	'''

	tokens = open(tokensFile,'r');
	numbers = [];
	
	for line in tokens:
		keyword = line.split('\n');
		numbers = numbers + [DicoOfTokens.tokensDico[keyword[0]]];
	
	return numbers;


def nGramList(numbersList, n):
	'''
		Given a list of numbers, produce every possible n-gram (configurable) and store them in a matrix.
	'''
	if (n < 1 or n >= (len(numbersList))):
		print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)');
	else:
		matrixAllNGrams = [[] for i in range(len(numbersList) - (n - 1))];
		for j in range(len(numbersList) - (n - 1)): # Loop on all the n-grams
			matrixAllNGrams[j] = str(numbersList[j]);
			for i in range(n - 1): # Loop on the components of a given n-gram
				#matrixAllNGrams[j] = matrixAllNGrams[j] + [numbersList[j + i]];
				matrixAllNGrams[j] = matrixAllNGrams[j] + ',' + str(numbersList[j + i + 1]); # String and not list, as list cannot be used as key in a dictionary
				# (tuples could, but they are immutable, so my function would not work for them)

		return matrixAllNGrams;


def nGramCsv(numbersList, n):
	'''
		Given a list of numbers, produce every possible n-gram (configurable) and store them in a CSV file.
	'''
	if (n < 1 or n >= (len(numbersList))):
		print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)');
	else:
		csvFile = open('nGram.csv','w');
		for j in range(len(numbersList) - (n - 1)):
			csvFile.write(str(numbersList[j]));
			for i in range(n - 1):
				csvFile.write(',' + str(numbersList[j + i + 1]));
			csvFile.write('\n');
			
		csvFile.close();



