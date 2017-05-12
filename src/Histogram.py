
'''
	Plotting an histogram using data from a dictionary.
'''

import matplotlib.pyplot as plt
from textwrap import wrap


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
