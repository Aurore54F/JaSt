
'''
	Counting the number of occurrences (probability) of each n-gram in JavaScript files.
'''

import matplotlib.pyplot as plt
from textwrap import wrap


def countSetsOfNGrams(matrixAllNGrams):
	'''
		Given a matrix containing every possible n-gram (for a JavaScript given file), count and store (once) the probability of occurrences of each set of 
		n-gram in a dictionary.
		
		-------
		Parameter:
		- matrixAllNGrams: 
			Contains in each row a tuple representing an n-gram.
			
		-------
		Returns:
		- Dictionary
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
		- or None if matrixAllNGrams is empty.
	'''
		
	if matrixAllNGrams is not None:
		dicoOfNGrams = {};
		setsNGrams = len(matrixAllNGrams); # Number of lines in the matrix, i.e. of sets of n-grams.
		for j in range(setsNGrams):
			if matrixAllNGrams[j] in dicoOfNGrams:
				dicoOfNGrams[matrixAllNGrams[j]] = dicoOfNGrams[matrixAllNGrams[j]] + 1/setsNGrams; # Normalization to enable future comparisons
			else:
				dicoOfNGrams[matrixAllNGrams[j]] = 1/setsNGrams;
				
		return dicoOfNGrams;
	#else:
		#print('Matrix of type NoneType');
	

def histoFromDico(orderedDico, figPath = 'histo.png', title = '', xlabel = '', ylabel = ''):
	'''
		Histogram displaying the probability of apparition of each n-gram as stored in the dictionary in input.
		
		-------
		Parameters:
		- orderedDico: Dictionary
			Key: tuple representing an n-gram;
			Value: probability of occurrences of a given tuple of n-gram.
		- figPath: 
			Histogram location. Default: "./histo.png".
		- title: String
			Title of the histogram. Default: no title.
		- xlabel: String
			Xlabel of the histogram. Default: no xlabel.
		- ylabel: String
			Ylabel of the histogram. Default: no ylabel.
			
		-------
		Returns:
		- File
			Displays the histogram.
	'''

	plt.bar(range(len(orderedDico)), orderedDico.values(), align = 'center');
	plt.xticks(range(len(orderedDico)),(orderedDico.keys()),rotation = 90); # n-gram labels are vertical
	plt.title("\n".join(wrap(title, 60))); # Title written in several line if necessary
	#plt.xlabel(xlabel);
	#plt.ylabel(ylabel);
	plt.tight_layout(); # Otherwise the xlabel does not fit in the figure
	#plt.show(); # To display the histogram
	
	# Manage the histogram size
	fig = plt.gcf(); # uncomment for slimit and esprimaAst
	fig.set_size_inches(25, 10); # uncomment for slimit and esprimaAst
	
	plt.savefig(figPath, dpi = 100);
	plt.clf(); # Otherwise all figures are written on one another
