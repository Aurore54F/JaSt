
'''
	Creation of Esprima syntactical dictionary.
'''

import re # For regular expressions
import collections # To order a dictionary

import ConfFileProduction

# Esprima syntactical tokens:
Syntax = "     AssignmentExpression: 'AssignmentExpression',     AssignmentPattern: 'AssignmentPattern',     ArrayExpression: 'ArrayExpression',     ArrayPattern: 'ArrayPattern',     ArrowFunctionExpression: 'ArrowFunctionExpression',     AwaitExpression: 'AwaitExpression',     BlockStatement: 'BlockStatement',     BinaryExpression: 'BinaryExpression',     BreakStatement: 'BreakStatement',     CallExpression: 'CallExpression',     CatchClause: 'CatchClause',     ClassBody: 'ClassBody',     ClassDeclaration: 'ClassDeclaration',     ClassExpression: 'ClassExpression',     ConditionalExpression: 'ConditionalExpression',     ContinueStatement: 'ContinueStatement',     DoWhileStatement: 'DoWhileStatement',     DebuggerStatement: 'DebuggerStatement',     EmptyStatement: 'EmptyStatement',     ExportAllDeclaration: 'ExportAllDeclaration',     ExportDefaultDeclaration: 'ExportDefaultDeclaration',     ExportNamedDeclaration: 'ExportNamedDeclaration',     ExportSpecifier: 'ExportSpecifier',     ExpressionStatement: 'ExpressionStatement',     ForStatement: 'ForStatement',     ForOfStatement: 'ForOfStatement',     ForInStatement: 'ForInStatement',     FunctionDeclaration: 'FunctionDeclaration',     FunctionExpression: 'FunctionExpression',     Identifier: 'Identifier',     IfStatement: 'IfStatement',     Import: 'Import',     ImportDeclaration: 'ImportDeclaration',     ImportDefaultSpecifier: 'ImportDefaultSpecifier',     ImportNamespaceSpecifier: 'ImportNamespaceSpecifier',     ImportSpecifier: 'ImportSpecifier',     Literal: 'Literal',     LabeledStatement: 'LabeledStatement',     LogicalExpression: 'LogicalExpression',     MemberExpression: 'MemberExpression',     MetaProperty: 'MetaProperty',     MethodDefinition: 'MethodDefinition',     NewExpression: 'NewExpression',     ObjectExpression: 'ObjectExpression',     ObjectPattern: 'ObjectPattern',     Program: 'Program',     Property: 'Property',     RestElement: 'RestElement',     ReturnStatement: 'ReturnStatement',     SequenceExpression: 'SequenceExpression',     SpreadElement: 'SpreadElement',     Super: 'Super',     SwitchCase: 'SwitchCase',     SwitchStatement: 'SwitchStatement',     TaggedTemplateExpression: 'TaggedTemplateExpression',     TemplateElement: 'TemplateElement',     TemplateLiteral: 'TemplateLiteral',     ThisExpression: 'ThisExpression',     ThrowStatement: 'ThrowStatement',     TryStatement: 'TryStatement',     UnaryExpression: 'UnaryExpression',     UpdateExpression: 'UpdateExpression',     VariableDeclaration: 'VariableDeclaration',     VariableDeclarator: 'VariableDeclarator',     WhileStatement: 'WhileStatement',     WithStatement: 'WithStatement',     YieldExpression: 'YieldExpression' "
# List of tokens available here <https://github.com/jquery/esprima/blob/master/src/syntax.ts>.


def buildAstDicoEsprima():
	'''
		Construction of a dictionary containing every Esprima syntactical token mapped to an integer.
		The dictionary is also stored in a configuration file (see DicoOfAstEsprima.py).
		
		-------
		Returns:
		- Ordered dictionary
			Key: Esprima syntactical tokens;
			Value: A unique integer.
		- Configuration file
			Stores the previous dictionary (see DicoOfAstEsprima.py).	
	'''
	
	i = 0
	dico = {}
	
	
	# Creation of a dictionary mapping Esprima syntactical tokens to unique integers.
	
	m = re.findall("\'[A-z]+\'", Syntax)
	astList = [m[i].split("'")[1] for i in range(len(m))] # List containing the Esprima syntactical tokens indicated in the string "Syntax" above.
	
	for el in sorted(astList):
		dico[el] = i
		i = i + 1
	
	j = len(astList)
	orderedDico = collections.OrderedDict(sorted(dico.items()))
	orderedDico['LineComment'] = j  # Single-line comment (// towards the end-of-line)
	orderedDico['BlockComment'] = j + 1  # Multi-line comment (enclosed by /* and */)
	
	
	# Storage of the dictionary in a configuration file
	descr = '#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary tokensDico.\n\t\tKey: Esprima syntactical token;\n\t\tValue: Unique integer.\n'''\n\n\ntokensDico = { \n"
	ConfFileProduction.dicoStorage('../Dico_MapTokens-Int', 'DicoOfAstEsprima.py', descr, orderedDico)
	
	return orderedDico