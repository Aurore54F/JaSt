
'''
    Extracting lexical and syntactical units from a JavaScript file
    and converting them into integers.
'''

import subprocess # to call Shell commands
from slimit.lexer import Lexer

from __init__ import *

def astUsedEsprima(inputFile):
    '''
        Given an input JavaScript file, create a list containing the esprima syntactical
        units present in the file.
        The order of the units stored in the previous list resembles a tree traversal using
        the depth-first algorithm post-order.

        -------
        Parameter:
        - inputFile: File
            Should it be malformed or no JS file, then an exception will be raised
            (see JsDetection.isJsFile).

        -------
        Returns:
        - List
            Contains the esprima syntactical units present in the input file.
        - or None if the file either is no JS or malformed.
    '''

    return JsDetection.isJsFile(inputFile, syntacticalUnits=True)


def tokensUsedEsprima(inputFile):
    '''
        Given an input JavaScript file, create a list containing the esprima lexical tokens present
        in the file.

        -------
        Parameter:
        - inputFile: File
            Should it be malformed or no JS file, then an exception will be raised
            (see JsDetection.isJsFile).

        -------
        Returns:
        - List
            Contains the esprima lexical tokens present in the input file.
        - or None if the file either is no JS or malformed.
    '''

    if JsDetection.isJsFile(inputFile) == 0: # Only if the current file is a well-formed JS sample
        tokenizerPath = currentPath + '/src/JsEsprima/tokenizer.js'
        try:
            result = subprocess.run(['nodejs', tokenizerPath, inputFile],\
                                    stdout=subprocess.PIPE).stdout.decode('utf-8')
            # result is a string containing the lexical tokens (as found by esprima) of
            #the given JS script, separated by '\n'.
            # Structure of a token: "b'Punctuator\n'"
            tokenPart = str(result).split('\n') # Keyword as used in JS
            del tokenPart[len(tokenPart) - 1] # As last one = ''
            return tokenPart # Lexical tokens

        except subprocess.CalledProcessError:
            print("Subprocess-related error")

        except OSError: # System-related error, e.g. if file cannot be opened
            print("System-related error")



def tokensUsedSlimit(inputFile):
    '''
        Given an input JavaScript file, create a list containing the SlimIt lexical tokens
        present in the file.

        -------
        Parameter:
        - inputFile: File
            Should it be malformed or no JS file, then an exception will be raised
            (see JsDetection.isJsFile).

        -------
        Returns:
        - List
            Contains the SlimIt lexical tokens present in the input file.
        - or None if the file either is no JS or malformed.
    '''

    if JsDetection.isJsFile(inputFile) == 0: # Only if the current file is a well-formed JS sample
        with open(inputFile, 'r') as inF:
            s = ''
            try:
                for line in inF:
                    s += str(line) # Store the content of the JS file in a string, because
                    #far more faster than using SlimIt minifier.
            except UnicodeDecodeError:
                print('Exception handling')

        lexer = Lexer()
        lexer.input(s)
        l = []

        try:
            for token in lexer:
                # Structure of a token: "LexToken(VAR,'var',1,0)"
                tokenPart = str(token).split('(')
                tokenComplete = tokenPart[1].split(',') # Keyword as used in JS
                l += [tokenComplete[0]]
            return l # Lexical tokens

        except TypeError:
            print('Exception handling')


def tokensUsed(parser, jsFile):
    '''
        Return the list of (lexical/syntactical) units (for a given parser) present in
        a given JavaScript document.

        -------
        Parameter:
        - parser: String
            Either 'slimIt' (tokenizer), 'esprima' (tokenizer), 'esprimaAst' (parser), or
            'esprimaAstSimp' (parser after simplification).
        - jsFile: String
            Path of the JavaScript file to be analysed.

        -------
        Returns:
        - List
            Contains the tokens present in jsFile given in input.
        - or None if the file either is no JS or malformed.
    '''

    if parser.lower() == 'slimit':
        tokensList = tokensUsedSlimit(jsFile)
    elif parser.lower() == 'esprima':
        tokensList = tokensUsedEsprima(jsFile)
    elif parser.lower() == 'esprimaast' or parser.lower() == 'esprimaastsimp':
        tokensList = astUsedEsprima(jsFile)
    else:
        print("Error on the parser's name. Indicate 'slimIt', 'esprima', 'esprimaAst', or\
        'esprimaAstSimp'.")
        return
    return tokensList


def dicoUsed(parser):
    '''
        Return the (lexical/syntactical) units dictionary corresponding to the parser
        given in input.

        -------
        Parameter:
        - parser: String
            Either 'slimIt' (tokenizer), 'esprima' (tokenizer), 'esprimaAst' (parser), or
            'esprimaAstSimp' (parser after simplification).

        -------
        Returns:
        - Dictionary
            Either DicoOfTokensSlimit.tokensDico, DicoOfTokensEsprima.tokensDico,
            DicoOfAstEsprima.tokensDico, or DicoOfAstEsprimaSimplified.tokensDico.
    '''

    if parser.lower() == 'slimit':
        dico = DicoOfTokensSlimit.tokensDico
    elif parser.lower() == 'esprima':
        dico = DicoOfTokensEsprima.tokensDico
    elif parser.lower() == 'esprimaast':
        dico = DicoOfAstEsprima.tokensDico
    elif parser.lower() == 'esprimaastsimp':
        dico = DicoOfAstEsprimaSimplified.tokensDico
    else:
        print("Error on the parser's name. Indicate 'slimIt', 'esprima', 'esprimaAst', or\
        'esprimaAstSimp'.")
        return
    return dico


def tokensToNumbers(tokensDico, tokensList):
    '''
        Convert a list of (lexical/syntactical) units in their corresponding numbers
        (as indicated in the corresponding units dictionary).

        -------
        Parameters:
        - tokensDico: Dictionary
            Either DicoOfTokensSlimit.tokensDico, DicoOfTokensEsprima.tokensDico,
            DicoOfAstEsprima.tokensDico, or DicoOfAstEsprimaSimplified.tokensDico.
        - tokensList: List
            List containing the units extracted from a JS file.
        -------
        Returns:
        - List
            Contains the Integers which correspond to the units given in tokensList.
        - or None if tokensList is empty (cases where the JS file considered either is no JS,
        malformed or empty).
    '''

    if tokensList is not None and tokensList != []:
        numbers = []

        for token in tokensList:
            numbers = numbers + [tokensDico[token]]

        return numbers
