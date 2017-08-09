
'''
	Creation of SlimIt lexical dictionary.
	The general structure is inspired from the one used by PJScan:
	<https://sourceforge.net/p/pjscan/code/HEAD/tree/trunk/pjscan/src/tokens.cpp#l22>.
'''

import collections # To order a dictionary

import ConfFileProduction

# SlimIt lexical tokens:
lextokens = {'BOR': 1, 'LBRACKET': 1, 'WITH': 1, 'MINUS': 1, 'RPAREN': 1, 'PLUS': 1, 'VOID': 1, 'BLOCK_COMMENT': 1, 'GT': 1, 'RBRACE': 1, 'PERIOD': 1, 'GE': 1, 'VAR': 1, 'THIS': 1, 'MINUSEQUAL': 1, 'TYPEOF': 1, 'OR': 1, 'DELETE': 1, 'DIVEQUAL': 1, 'RETURN': 1, 'RSHIFTEQUAL': 1, 'EQEQ': 1, 'SETPROP': 1, 'BNOT': 1, 'URSHIFTEQUAL': 1, 'TRUE': 1, 'COLON': 1, 'FUNCTION': 1, 'LINE_COMMENT': 1, 'FOR': 1, 'PLUSPLUS': 1, 'ELSE': 1, 'TRY': 1, 'EQ': 1, 'AND': 1, 'LBRACE': 1, 'CONTINUE': 1, 'NOT': 1, 'OREQUAL': 1, 'MOD': 1, 'RSHIFT': 1, 'DEFAULT': 1, 'WHILE': 1, 'NEW': 1, 'CASE': 1, 'MODEQUAL': 1, 'NE': 1, 'MULTEQUAL': 1, 'SWITCH': 1, 'CATCH': 1, 'STREQ': 1, 'INSTANCEOF': 1, 'PLUSEQUAL': 1, 'GETPROP': 1, 'FALSE': 1, 'CONDOP': 1, 'BREAK': 1, 'LINE_TERMINATOR': 1, 'ANDEQUAL': 1, 'DO': 1, 'NUMBER': 1, 'LSHIFT': 1, 'DIV': 1, 'NULL': 1, 'MULT': 1, 'DEBUGGER': 1, 'LE': 1, 'SEMI': 1, 'BXOR': 1, 'LT': 1, 'COMMA': 1, 'REGEX': 1, 'STRING': 1, 'BAND': 1, 'FINALLY': 1, 'STRNEQ': 1, 'LPAREN': 1, 'IN': 1, 'MINUSMINUS': 1, 'ID': 1, 'IF': 1, 'XOREQUAL': 1, 'LSHIFTEQUAL': 1, 'URSHIFT': 1, 'RBRACKET': 1, 'THROW': 1, 'CLASS': 1, 'CONST': 1, 'ENUM': 1, 'EXPORT': 1, 'EXTENDS': 1, 'IMPORT': 1, 'SUPER': 1}
# List of tokens available here <https://github.com/rspivak/slimit/blob/master/src/slimit/lextab.py>, augmented with some future reserved words.


def buildTokensDicoSlimit():
	'''
		Construction of a dictionary containing every SlimIt lexical token mapped to an integer.
		The dictionary is also stored in a configuration file (see DicoOfTokensSlimit.py).
		
		-------
		Returns:
		- Ordered dictionary
			Key: SlimIt lexical tokens;
			Value: A unique integer.
		- Configuration file
			Stores the previous dictionary (see DicoOfTokensSlimit.py).	
	'''
	
	i = 0
	dico = {}
	
	
	# Creation of a dictionary mapping SlimIt lexical tokens to unique integers.
	
	for token in sorted(lextokens):
		dico[token] = i
		i = i + 1
		
	j = len(lextokens)
	orderedDico = collections.OrderedDict(sorted(dico.items()))
	'''
		orderedDico['STR_10'] = j  # a string literal of length < 10
		orderedDico['STR_100'] = j + 1 # a string literal of length < 100
		orderedDico['STR_1000'] = j +  2 # a string literal of length < 1,000
		orderedDico['STR_10000'] = j + 3 # a string literal of length < 10,000
		orderedDico['STR_UNBOUND'] = j + 4 # a string literal of length > 10,000
		orderedDico['UNESCAPE'] = j + 5 # a call to unescape()
		orderedDico['SETTIMEOUT'] = j + 6 # a call to setTimeOut()
		orderedDico['FROMCHARCODE'] = j + 7 # a call to fromCharCode
		orderedDico['EVAL'] = j + 8 # a call to eval()
		orderedDico['ERR'] = j + 9
	'''
	
	# Storage of the dictionary in a configuration file
	descr = '#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary tokensDico.\n\t\tKey: SlimIt lexical token;\n\t\tValue: Unique integer.\n'''\n\n\ntokensDico = { \n"
	ConfFileProduction.dicoStorage('../Dico_MapTokens-Int', 'DicoOfTokensSlimit.py', descr, orderedDico)
	
	return orderedDico