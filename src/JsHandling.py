
'''
	Main program, entry point.
'''

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import TokensProduction
import NGrams
import Histogram

import collections # to order a dictionary
import shutil
import glob # Unix style pathname pattern expansion
import os


def jsToProbaOfTokens(parser, jsFile = '/home/aurore/Documents/Code/JS-samples/0a2a6e27c7e455b4023b8a29022ade1399080b30.bin', n = 4):
	'''
		Production of a dictionary containing the number of occurrences (probability) of each n-gram (default: 4-gram) from a given JS file.
	'''
	
	if parser.lower() == 'slimit':
		dico = DicoOfTokensSlimit.tokensDico;
		tokensList = TokensProduction.tokensUsedSlimit(jsFile);
	elif parser.lower() == 'esprima':
		dico = DicoOfTokensEsprima.tokensDico;
		tokensList = TokensProduction.tokensUsedEsprima(jsFile);
		
	else:
		print("Error on the parser's name. Indicate 'slimIt' or 'esprima'.");
		return;
		
	numbersList = TokensProduction.tokensToNumbers(dico, tokensList);	
	matrixNGrams = NGrams.nGramsList(numbersList, n);
	#prettyPrintNGramsDico(countSetsOfNGrams(matrixNGrams));
	dicoOfOccurrences = NGrams.countSetsOfNGrams(matrixNGrams);
	orderedDico = collections.OrderedDict(sorted(dicoOfOccurrences.items()))
	
	#Histogram.histoFromDico(orderedDico, './Histo.png', title = jsFile);
	
	return orderedDico;
	


def matrixOfProbaToCsv():
	'''
		
	'''
		
	matrixAllNGramsProba = [[] for j in range(10)]; # TODO hardcoded	
	vectNGramsProba = np.zeros(10000); # TODO hardcoded
	for key in dicoForHisto:
		vectNGramsProba[nGramToInt(10,key)] = dicoForHisto[key]; # TODO hardcoded
			
		matrixAllNGramsProba[i] = vectNGramsProba;
			
	return matrixAllNGramsProba;
	
	

def main(parser, jsDir = '/home/aurore/Documents/Code/JS-samples', histoDir = '/home/aurore/Documents/Code/Histograms/', n = 4):
	'''
		Main program, entry point.
	'''

	# Directory to store the histograms files
	if os.path.exists(histoDir):
		shutil.rmtree(histoDir);
	os.makedirs(histoDir);

	histoFilePart1 = 'Histogram';
	histoFilePart3 = '.png';
	i = 1;
		
	for javaScriptFile in glob.glob(jsDir + '/*.bin'):
		#print(os.path.join(javaScriptFile));
		figPath =  histoDir + histoFilePart1 + str(i) + histoFilePart3;
		dicoForHisto = jsToProbaOfTokens(parser, javaScriptFile, n) # Data for the histogram (i.e. n-gram with occurrence);
		Histogram.histoFromDico(dicoForHisto, figPath, title = javaScriptFile);
		i += 1;
