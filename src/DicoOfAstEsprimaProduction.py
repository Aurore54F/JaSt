
'''
	Creation of Esprima syntax elements dictionary.
'''

import re # for regular expressions

# Esprima AST syntax
Syntax = "     AssignmentExpression: 'AssignmentExpression',     AssignmentPattern: 'AssignmentPattern',     ArrayExpression: 'ArrayExpression',     ArrayPattern: 'ArrayPattern',     ArrowFunctionExpression: 'ArrowFunctionExpression',     AwaitExpression: 'AwaitExpression',     BlockStatement: 'BlockStatement',     BinaryExpression: 'BinaryExpression',     BreakStatement: 'BreakStatement',     CallExpression: 'CallExpression',     CatchClause: 'CatchClause',     ClassBody: 'ClassBody',     ClassDeclaration: 'ClassDeclaration',     ClassExpression: 'ClassExpression',     ConditionalExpression: 'ConditionalExpression',     ContinueStatement: 'ContinueStatement',     DoWhileStatement: 'DoWhileStatement',     DebuggerStatement: 'DebuggerStatement',     EmptyStatement: 'EmptyStatement',     ExportAllDeclaration: 'ExportAllDeclaration',     ExportDefaultDeclaration: 'ExportDefaultDeclaration',     ExportNamedDeclaration: 'ExportNamedDeclaration',     ExportSpecifier: 'ExportSpecifier',     ExpressionStatement: 'ExpressionStatement',     ForStatement: 'ForStatement',     ForOfStatement: 'ForOfStatement',     ForInStatement: 'ForInStatement',     FunctionDeclaration: 'FunctionDeclaration',     FunctionExpression: 'FunctionExpression',     Identifier: 'Identifier',     IfStatement: 'IfStatement',     Import: 'Import',     ImportDeclaration: 'ImportDeclaration',     ImportDefaultSpecifier: 'ImportDefaultSpecifier',     ImportNamespaceSpecifier: 'ImportNamespaceSpecifier',     ImportSpecifier: 'ImportSpecifier',     Literal: 'Literal',     LabeledStatement: 'LabeledStatement',     LogicalExpression: 'LogicalExpression',     MemberExpression: 'MemberExpression',     MetaProperty: 'MetaProperty',     MethodDefinition: 'MethodDefinition',     NewExpression: 'NewExpression',     ObjectExpression: 'ObjectExpression',     ObjectPattern: 'ObjectPattern',     Program: 'Program',     Property: 'Property',     RestElement: 'RestElement',     ReturnStatement: 'ReturnStatement',     SequenceExpression: 'SequenceExpression',     SpreadElement: 'SpreadElement',     Super: 'Super',     SwitchCase: 'SwitchCase',     SwitchStatement: 'SwitchStatement',     TaggedTemplateExpression: 'TaggedTemplateExpression',     TemplateElement: 'TemplateElement',     TemplateLiteral: 'TemplateLiteral',     ThisExpression: 'ThisExpression',     ThrowStatement: 'ThrowStatement',     TryStatement: 'TryStatement',     UnaryExpression: 'UnaryExpression',     UpdateExpression: 'UpdateExpression',     VariableDeclaration: 'VariableDeclaration',     VariableDeclarator: 'VariableDeclarator',     WhileStatement: 'WhileStatement',     WithStatement: 'WithStatement',     YieldExpression: 'YieldExpression' ";
# List of elements available here <https://github.com/jquery/esprima/blob/master/src/syntax.ts>.


def buildAstDicoEsprima():
	'''
		Construction of a dictionary containing every Esprima syntax element mapped to an integer.
		The dictionary is also stored in a configuration file (DicoOfAstEsprima.py).
	'''
	
	i = 0;
	dico = {};
	
	m = re.findall("\'[A-z]+\'", Syntax);
	astList = [m[i].split("'")[1] for i in range(len(m))];
	
	for el in sorted(astList):
		dico[el] = i;
		i = i + 1;
	
	dicoFile = open('DicoOfAstEsprima.py','w');
	dicoFile.write('#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the mapping between every Esprima syntax element and their corresponding integer.\n'''\n\n\nastDico = { \n");
	for el in dico:
		dicoFile.write("\t'" + el + "'" + ' : ' + str(dico[el]) + ', \n');
	dicoFile.write('}');
	dicoFile.close();
	
	return dico;


def prettyPrintAstDico(dico):
	'''
		Print a human-readable content of the syntactic elements from the dictionary.
	'''
	for el in dico:
		print(el + '\t : ' + str(dico[el]) + '\n');
