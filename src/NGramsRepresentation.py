
'''
	Simplifing the n-grams list and mapping the resulting n-grams to integers.
'''

import os # To create repositories
import collections # To order a dictionary
import importlib # To reload updated modules
import sys
#sys.path.insert(0, './Dico_MapNGrams-Int') # To add a directory to import modules from
#sys.path.insert(0, './DicoProduction') # To add a directory to import modules from

import DicoIntToNGramsSlimit
import DicoNGramsToIntSlimit
import DicoIntToNGramsEsprima
import DicoNGramsToIntEsprima
import DicoIntToNGramsEsprimaAst
import DicoNGramsToIntEsprimaAst
import DicoIntToNGramsEsprimaAstSimplified
import DicoNGramsToIntEsprimaAstSimplified

import ConfFileProduction



def mappingNGramsInt(nGramsSet, parser):
	'''
		Construction of dictionaries mapping integers and n-grams.
		They are stored in a configuration file (see DicoNGramsToInt.py and DicoIntToNGrams.py).
		
		-------
		Parameter:
		- nGramsSet: set
			Set of n-grams to be mapped to unique integers.
			
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
	
	s = sorted(nGramsSet)
	
	dicoNGramsToIntOld = dicoNGramsToIntUsed(parser)
	dicoIntToNGramsOld = dicoIntToNGramsUsed(parser)
	i = len(dicoNGramsToIntOld)
	#dicoNGramsToIntOld = {}
	#dicoIntToNGramsOld = {}
	#i = 0
	
	print('Size ' + str(i))
	
	for el in s:
		if str(el) not in dicoNGramsToIntOld:
			dicoNGramsToIntOld[str(el)] = str(i) # Dictionary mapping n-grams to unique integers.
			dicoIntToNGramsOld[str(i)] = str(el) # Dictionary mapping integers to unique n-grams.
			i = i + 1
	
	# Storage of the dictionaries in configuration files
	
	descr1 = '#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary dicoNGramsToInt.\n\t\tKey: N-gram;\n\t\tValue: Unique integer.\n'''\n\n\ndicoNGramsToInt = { \n";
	descr2 = '#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary dicoIntToNGrams.\n\t\tKey: Integer;\n\t\tValue: Unique n-gram.\n'''\n\n\ndicoIntToNGrams = { \n";
	
	dico1 = collections.OrderedDict(sorted(dicoNGramsToIntOld.items()))
	dico2 = collections.OrderedDict(sorted(dicoIntToNGramsOld.items()))
	
	name1 = dicoNGramsIntNames(parser)[0]
	name2 = dicoNGramsIntNames(parser)[1]
	
	# dicoNGramsToInt
	ConfFileProduction.dicoStorage('Dico_MapNGrams-Int', name1, descr1, dico1)
	# dicoIntToNGrams
	ConfFileProduction.dicoStorage('Dico_MapNGrams-Int', name2, descr2, dico2)
	

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
	
	# return DicoNGramsToInt.dicoNGramsToInt[str(nGram)]
	try:
		i = dico[str(nGram)]
		return i
	except KeyError as e:
		print('The key ' + str(e) + ' is not in the dictionary.')
		pass


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
	
	# return DicoIntToNGrams.dicoIntToNGrams[str(i)]
	try:
		ngram = dico[str(i)]
		return ngram
	except KeyError as e:
		print('The key ' + str(e) + ' is not in the dictionary.')
		pass


def dicoNGramsToIntUsed(parser):
	'''
		Return the Dictionary corresponding to the parser given in input.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
			
		-------
		Returns:
		- Dictionary
			Either DicoNGramsToIntSlimit.dicoNGramsToInt, DicoNGramsToIntEsprima.dicoNGramsToInt, DicoNGramsToIntEsprimaAst.dicoNGramsToInt, or
			DicoNGramsToIntEsprimaAstSimplified.dicoNGramsToInt.
	'''
	
	if parser.lower() == 'slimit':
		importlib.reload(DicoNGramsToIntSlimit) # Reload to be sure to work with the last version of the dico
		dico = DicoNGramsToIntSlimit.dicoNGramsToInt
	elif parser.lower() == 'esprima':
		importlib.reload(DicoNGramsToIntEsprima)
		dico = DicoNGramsToIntEsprima.dicoNGramsToInt
	elif parser.lower() == 'esprimaast':
		importlib.reload(DicoNGramsToIntEsprimaAst)
		dico = DicoNGramsToIntEsprimaAst.dicoNGramsToInt	
	elif parser.lower() == 'esprimaastsimp':
		importlib.reload(DicoNGramsToIntEsprimaAstSimplified)
		dico = DicoNGramsToIntEsprimaAstSimplified.dicoNGramsToInt	
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.")
		return
	return dico


def dicoIntToNGramsUsed(parser):
	'''
		Return the Dictionary corresponding to the parser given in input.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', or 'esprimaAst'.
			
		-------
		Returns:
		- Dictionary
			Either DicoIntToNGramsSlimit.dicoIntToNGrams, DicoIntToNGramsEsprima.dicoIntToNGrams, DicoIntToNGramsEsprimaAst.dicoIntToNGrams, or
			DicoIntToNGramsEsprimaAstSimplified.dicoIntToNGrams.
	'''
	
	if parser.lower() == 'slimit':
		importlib.reload(DicoNGramsToIntSlimit) # Reload to be sure to work with the last version of the dico
		dico = DicoIntToNGramsSlimit.dicoIntToNGrams
	elif parser.lower() == 'esprima':
		importlib.reload(DicoNGramsToIntEsprima)
		dico = DicoIntToNGramsEsprima.dicoIntToNGrams
	elif parser.lower() == 'esprimaast':
		importlib.reload(DicoNGramsToIntEsprimaAst)
		dico = DicoIntToNGramsEsprimaAst.dicoIntToNGrams	
	elif parser.lower() == 'esprimaastsimp':
		importlib.reload(DicoNGramsToIntEsprimaAstSimplified)
		dico = DicoIntToNGramsEsprimaAstSimplified.dicoIntToNGrams	
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.")
		return
	return dico


def dicoNGramsIntNames(parser):
	'''
		Return the names of the dictionaries mapping n-grams and integers.
				
		-------
		Parameter:
		- parser: String
			Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
			
		-------
		Returns:
		- List
			Contains as:
			* name1: either DicoNGramsToIntSlimit.dicoNGramsToInt, DicoNGramsToIntEsprima.dicoNGramsToInt, DicoNGramsToIntEsprimaAst.dicoNGramsToInt, or
			DicoNGramsToIntEsprimaAstSimplified.dicoNGramsToInt.
			*name2: either DicoIntToNGramsSlimit.dicoIntToNGrams, DicoIntToNGramsEsprima.dicoIntToNGrams, DicoIntToNGramsEsprimaAst.dicoIntToNGrams, or
			DicoIntToNGramsEsprimaAstSimplified.dicoIntToNGrams.
	'''
	
	'''
	- name1: string
		Name of the dictionary storing the mapping of an n-gram to a unique integer.
	- name2: string
		Name of the dictionary storing the mapping of an integer to a unique n-gram.
	'''
	
	if parser.lower() == 'slimit':
		name1 = 'DicoNGramsToIntSlimit.py'
		name2 = 'DicoIntToNGramsSlimit.py'
	elif parser.lower() == 'esprima':
		name1 = 'DicoNGramsToIntEsprima.py'
		name2 = 'DicoIntToNGramsEsprima.py'
	elif parser.lower() == 'esprimaast':
		name1 = 'DicoNGramsToIntEsprimaAst.py'
		name2 = 'DicoIntToNGramsEsprimaAst.py'
	elif parser.lower() == 'esprimaastsimp':
		name1 = 'DicoNGramsToIntEsprimaAstSimplified.py'
		name2 = 'DicoIntToNGramsEsprimaAstSimplified.py'
	else:
		print("Error on the parser's name. Indicate 'slimIt', 'esprima' or 'esprimaAst'.")
		return
	return [name1, name2]
