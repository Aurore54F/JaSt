
'''
	Plotting an histogram using data from a dictionary.
'''

import matplotlib.pyplot as plt


def histoFromDico(orderedDico, figPath, title = '', xlabel = '', ylabel = ''):
	'''
	Histogram displaying the probability of apparition of each n-gram as stored in the dictionary in input.
	'''

	plt.bar(range(len(orderedDico)), orderedDico.values(), align = 'center');
	plt.xticks(range(len(orderedDico)),(orderedDico.keys()),rotation = 90);
	#plt.show();
	#plt.title(title);
	#plt.xlabel(xlabel);
	#plt.ylabel(ylabel);
	plt.tight_layout(); # Otherwise the xlabel does not fit in the figure
	plt.savefig(figPath);
	plt.clf(); # Otherwise all figures are written one on the other
