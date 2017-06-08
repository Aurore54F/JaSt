
'''
	Simplifing the n-grams list and mapping the resulting n-grams to integers.
'''

import os # To create repositories
import collections # To order a dictionary
import sys
sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from

import DicoIntToNGramsSlimit
import DicoNGramsToIntSlimit
import DicoIntToNGramsEsprima
import DicoNGramsToIntEsprima
import DicoIntToNGramsEsprimaAst
import DicoNGramsToIntEsprimaAst


def mappingNGramsInt(nGramsSet, name1 = 'DicoNGramsToInt.py', name2 = 'DicoIntToNGrams.py'):
	'''
		Construction of dictionaries mapping integers and n-grams.
		They are stored in a configuration file (see DicoNGramsToInt.py and DicoIntToNGrams.py).
		
		-------
		Parameter:
		- nGramsSet: set
			Set of n-grams to be mapped to unique integers.
		- name1: string
			Name of the dictionary storing the mapping of an n-gram to a unique integer.
		- name2: string
			Name of the dictionary storing the mapping of an integer to a unique n-gram.
			
		-------
		Returns:
		- Configuration file 1
			Stores the dictionary dicoNGramsToInt:
				Key: N-gram;
				Value: Unique integer.
		- Configuration file 2
			Stores the dictionary dicoIntToNGrams:
				Key: Integer;
				Value: Unique n-gram.
	'''
	
	s = sorted(nGramsSet);
	i = 0;
	dicoNGramsToInt = {};
	dicoIntToNGrams = {};
	
	
	for el in s:
		dicoNGramsToInt[el] = i; # Dictionary mapping n-grams to unique integers.
		dicoIntToNGrams[i] = el; # Dictionary mapping integers to unique n-grams.
		i = i + 1;
	
	
	# Storage of the dictionaries in configuration files
	
	if not os.path.exists('Dico_MapNGrams-Int'):
		os.makedirs('Dico_MapNGrams-Int');
	
	# dicoNGramsToInt
	dicoFile = open('Dico_MapNGrams-Int/' + name1,'w');
	dicoFile.write('#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary dicoNGramsToInt.\n\t\tKey: N-gram;\n\t\tValue: Unique integer.\n'''\n\n\ndicoNGramsToInt = { \n");
	for el in collections.OrderedDict(sorted(dicoNGramsToInt.items())):
		dicoFile.write("\t'" + str(el) + "'" + ' : ' + str(dicoNGramsToInt[el]) + ', \n');
	dicoFile.write('}');
	dicoFile.close();
	
	# dicoIntToNGrams
	dicoFile = open('Dico_MapNGrams-Int/' + name2,'w');
	dicoFile.write('#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary dicoIntToNGrams.\n\t\tKey: Integer;\n\t\tValue: Unique n-gram.\n'''\n\n\ndicoIntToNGrams = { \n");
	for el in collections.OrderedDict(sorted(dicoIntToNGrams.items())):
		dicoFile.write("\t'" + str(el) + "'" + ' : ' + str(dicoIntToNGrams[el]) + ', \n');
	dicoFile.write('}');
	dicoFile.close();
	

def nGramToInt(dico, nGram):
	'''
		Convert an n-gram into an int.
		
		-------
		Parameters:
		- dico: Dictionary
			Key: N-gram;
			Value: Unique integer.
			Why is DicoNGramsToInt.dicoNGramsToInt no more hard-coded? Because I needed to reload it, after it being modified by the program.
		- nGram: Tuple
			Represents the n-gram to be converted into an int.
			
		-------
		Returns:
		- Integer
			Note that the operation that transforms an n-gram to an int is a bijection.
	'''
	
	# return DicoNGramsToInt.dicoNGramsToInt[str(nGram)];
	try:
		i = dico[str(nGram)];
		return i;
	except KeyError as e:
		print('The key ' + str(e) + ' is not in the dictionary.')
		pass;


def intToNGram(dico, i):
	'''
		Convert an int into an n-gram.
		
		-------
		Parameters:
		- dico: Dictionary
			Key: Integer;
			Value: Unique n-gram.
			Why is DicoNGramsToInt.dicoNGramsToInt no more hard-coded? Because I needed to reload it, after it being modified by the program.
		- i: Integer
			Represents the int to be converted into an n-gram.
			
		-------
		Returns:
		- Tuple
			Corresponds to an n-gram.
			Note that the operation that transforms an int to an n-gram is a bijection.
	'''
	
	# return DicoIntToNGrams.dicoIntToNGrams[str(i)];
	try:
		ngram = dico[str(i)];
		return i;
	except KeyError as e:
		print('The key ' + str(e) + ' is not in the dictionary.')
		pass;
	return ngram;


def dicoUsed(parser):
	'''
		Return the Dictionary corresponding to the parser given in input.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
			
		-------
		Returns:
		- Dictionary
			Either DicoOfTokensSlimit.tokensDico, DicoOfTokensEsprima.tokensDico, or DicoOfAstEsprima.astDico.
	'''
	
	if parser.lower() == 'slimit':
		dico = DicoNGramsToIntSlimit.dicoNGramsToInt;
	elif parser.lower() == 'esprima':
		dico = DicoNGramsToIntEsprima.dicoNGramsToInt;
		pass;
	elif parser.lower() == 'esprimaast':
		dico = DicoNGramsToIntEsprimaAst.dicoNGramsToInt;		
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.");
		return;
	return dico;
