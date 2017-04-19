
'''
	Plotting an histogram using data from a dictionary.
'''

import matplotlib.pyplot as plt
from textwrap import wrap


def histoFromDico(orderedDico, figPath, title = '', xlabel = '', ylabel = ''):
	'''
	Histogram displaying the probability of apparition of each n-gram as stored in the dictionary in input.
	'''

	plt.bar(range(len(orderedDico)), orderedDico.values(), align = 'center');
	plt.xticks(range(len(orderedDico)),(orderedDico.keys()),rotation = 90);
	plt.title("\n".join(wrap(title, 60)));
	#plt.xlabel(xlabel);
	#plt.ylabel(ylabel);
	plt.tight_layout(); # Otherwise the xlabel does not fit in the figure
	#plt.show();
	fig = plt.gcf(); # uncomment for slimit and esprimaAst
	fig.set_size_inches(25, 10); # uncomment for slimit and esprimaAst
	plt.savefig(figPath, dpi = 100);
	plt.clf(); # Otherwise all figures are written one on the other
