
'''
	Basis for storing dictionaries in a configuration file.
'''

import os # for OS dependent functionality
import sys

sys.path.insert(0, './Dico_MapTokens-Int') # To add a directory to import modules from
sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima
import DicoOfAstEsprimaSimplified

import DicoIntToNGramsSlimit
import DicoNGramsToIntSlimit
import DicoIntToNGramsEsprima
import DicoNGramsToIntEsprima
import DicoIntToNGramsEsprimaAst
import DicoNGramsToIntEsprimaAst
import DicoIntToNGramsEsprimaAstSimplified
import DicoNGramsToIntEsprimaAstSimplified


def dicoStorage(directoryName, fileName, description, orderedDico):
	'''
		Storing a given dictionary in a configuration file.
		
		-------
		Parameters:
		- directoryName: String
			Indicates where the configuration file will be stored.
		- fileName: String
			Indicates the configuration file name.
		- description: String
			Provides a short description for the configuration file.
		- orderedDico: Dictionary
			Dictionary to be stored in a configuration file
			
		-------
		Returns:
		- Configuration file
			Stores the previous dictionary.	
	'''
	
	if not os.path.exists(directoryName):
		os.makedirs(directoryName);
	
	dicoFile = open(directoryName + '/' + fileName,'w');
	dicoFile.write(description);
	for el in orderedDico:
		dicoFile.write("\t'" + str(el) + "'" + ' : ' + str(orderedDico[el]) + ', \n');
	dicoFile.write('}');
	dicoFile.close();
	

def prettyPrintDico(dico):
	'''
		Print a human-readable content of a dictionary.
		-------
		Parameter:
		- dico: Dictionary
	'''
	
	print('================================');
	for el in dico:
		print(str(el) + '\t : ' + str(dico[el]) + '\n');
	print('================================');