
'''
    Creation of Esprima simplified syntactical dictionary.
'''

import re # For regular expressions
import collections # To order a dictionary

import ConfFileProduction


def simplifyEsprimaSyntacticalTokens():
    '''
        Construction of the list of Esprima syntactical tokens after simplification.
        
        -------
        Returns:
        - List
            Contains lists representing families/groupings of Esprima syntactical tokens.
    '''
    
    # Esprima syntactical tokens:
    Syntax = "     AssignmentExpression: 'AssignmentExpression',     AssignmentPattern: 'AssignmentPattern',     ArrayExpression: 'ArrayExpression',     ArrayPattern: 'ArrayPattern',     ArrowFunctionExpression: 'ArrowFunctionExpression',     AwaitExpression: 'AwaitExpression',     BlockStatement: 'BlockStatement',     BinaryExpression: 'BinaryExpression',     BreakStatement: 'BreakStatement',     CallExpression: 'CallExpression',     CatchClause: 'CatchClause',     ClassBody: 'ClassBody',     ClassDeclaration: 'ClassDeclaration',     ClassExpression: 'ClassExpression',     ConditionalExpression: 'ConditionalExpression',     ContinueStatement: 'ContinueStatement',     DoWhileStatement: 'DoWhileStatement',     DebuggerStatement: 'DebuggerStatement',     EmptyStatement: 'EmptyStatement',     ExportAllDeclaration: 'ExportAllDeclaration',     ExportDefaultDeclaration: 'ExportDefaultDeclaration',     ExportNamedDeclaration: 'ExportNamedDeclaration',     ExportSpecifier: 'ExportSpecifier',     ExpressionStatement: 'ExpressionStatement',     ForStatement: 'ForStatement',     ForOfStatement: 'ForOfStatement',     ForInStatement: 'ForInStatement',     FunctionDeclaration: 'FunctionDeclaration',     FunctionExpression: 'FunctionExpression',     Identifier: 'Identifier',     IfStatement: 'IfStatement',     Import: 'Import',     ImportDeclaration: 'ImportDeclaration',     ImportDefaultSpecifier: 'ImportDefaultSpecifier',     ImportNamespaceSpecifier: 'ImportNamespaceSpecifier',     ImportSpecifier: 'ImportSpecifier',     Literal: 'Literal',     LabeledStatement: 'LabeledStatement',     LogicalExpression: 'LogicalExpression',     MemberExpression: 'MemberExpression',     MetaProperty: 'MetaProperty',     MethodDefinition: 'MethodDefinition',     NewExpression: 'NewExpression',     ObjectExpression: 'ObjectExpression',     ObjectPattern: 'ObjectPattern',     Program: 'Program',     Property: 'Property',     RestElement: 'RestElement',     ReturnStatement: 'ReturnStatement',     SequenceExpression: 'SequenceExpression',     SpreadElement: 'SpreadElement',     Super: 'Super',     SwitchCase: 'SwitchCase',     SwitchStatement: 'SwitchStatement',     TaggedTemplateExpression: 'TaggedTemplateExpression',     TemplateElement: 'TemplateElement',     TemplateLiteral: 'TemplateLiteral',     ThisExpression: 'ThisExpression',     ThrowStatement: 'ThrowStatement',     TryStatement: 'TryStatement',     UnaryExpression: 'UnaryExpression',     UpdateExpression: 'UpdateExpression',     VariableDeclaration: 'VariableDeclaration',     VariableDeclarator: 'VariableDeclarator',     WhileStatement: 'WhileStatement',     WithStatement: 'WithStatement',     YieldExpression: 'YieldExpression' ";
    # List of tokens available here <https://github.com/jquery/esprima/blob/master/src/syntax.ts>.
       
    m = re.findall("\'[A-z]*Expression\'", Syntax);
    expressions = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical expression tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Element\'", Syntax);
    elements = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical element tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Statement\'", Syntax);
    statements = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical statement tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Literal\'", Syntax);
    literals = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical literal tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Declaration\'", Syntax);
    declarations = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical declaration tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Pattern\'", Syntax);
    patterns = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical pattern tokens present in the string "Syntax" above.
    
    m = re.findall("\'[A-z]*Specifier\'", Syntax);
    specifiers = [m[i].split("'")[1] for i in range(len(m))]; # List containing the Esprima syntactical specifier tokens present in the string "Syntax" above.
    
    comments = ['LineComment', 'BlockComment']; # List containing the Esprima syntactical comment tokens.
    
    program = ['Program'];
    property2 = ['Property'];
    super2 = ['Super'];
    switchCase = ['SwitchCase'];
    variableDeclarator = ['VariableDeclarator'];
    catchClause = ['CatchClause'];
    classBody = ['ClassBody'];
    identifier = ['Identifier'];
    import2 = ['Import'];
    metaProperty = ['MetaProperty'];
    methodDefinition = ['MethodDefinition'];
    
    #tot = len(expressions) + len(elements) + len(statements) + len(literals) + len(declarations) + len(patterns) + len(specifiers);
    #print(str(tot));
    
    simplifiedList = [expressions, elements, statements, literals, declarations, patterns, specifiers, comments, program, property2, super2, switchCase, variableDeclarator, catchClause, classBody, identifier, import2, metaProperty, methodDefinition];
    return simplifiedList;


def buildAstSimplifiedDicoEsprima():
    '''
        Construction of a dictionary containing every Esprima syntactical token mapped to an integer.
        As the list of tokens has been simplified, different tokens can be mapped to the same integer.
        The dictionary is also stored in a configuration file (see DicoOfAstEsprimaSimplified.py).
        
        -------
        Returns:
        - Ordered dictionary
            Key: Esprima syntactical tokens;
            Value: A unique integer.
        - Configuration file
            Stores the previous dictionary (see DicoOfAstEsprimaSimplified.py).    
    '''
    
    i = 0;
    dico = {};
    simplifiedList = simplifyEsprimaSyntacticalTokens();
    
    # Creation of a dictionary mapping Esprima syntactical tokens to unique integers.
    
    for l in simplifiedList:
        for el in sorted(l):
            dico[el] = i; # Every elements el in a given list l will be mapped to the same integer, hence the simplification.
        i = i + 1;
        
    orderedDico = collections.OrderedDict(sorted(dico.items()));
    
    
    # Storage of the dictionary in a configuration file
    descr = '#!/usr/bin/python' + '\n \n' + "'''\n\tConfiguration file storing the dictionary tokensDico.\n\t\tKey: Esprima simplified syntactical token;\n\t\tValue: Unique integer.\n'''\n\n\ntokensDico = { \n"
    ConfFileProduction.dicoStorage('../Dico_MapTokens-Int', 'DicoOfAstEsprimaSimplified.py', descr, orderedDico);
    
    return orderedDico;