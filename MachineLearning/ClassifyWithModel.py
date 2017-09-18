
'''
    Main module to classify JavaScript files.
'''

import argparse

import Classification
from __init__ import *

def parsingCommands():
    '''
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * jsDirs=args['d'],
          * jsFiles=args['f'],
          * model=args['m']
          A more thorough description can be obtained:
            >$ python3 <path-of-MachineLearning/ClassifyWithModel.py> -help
    '''

    parser = argparse.ArgumentParser(description='Given a list of repositories or files paths,\
    detect the malicious JS files.')

    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analysed')
    parser.add_argument('--d', metavar='DIR', type=str, nargs='+', help='directories containing\
    the JS files to be analysed')
    parser.add_argument('--m', metavar='MODEL', type=str, nargs=1, help='path of the model\
    used to classify the new files (see >$ python3 <path-of-MachineLearning/LearnModel.py> -help)\
    to build a model)')

    args = vars(parser.parse_args())
    return args


argObjC = parsingCommands()


def mainClassification(jsDirs=argObjC['d'], jsFiles=argObjC['f'], model=argObjC['m']):
    '''
        Main function, performs a static analysis (lexical or syntactical)
        of JavaScript files given as input before indicating if the executables are benign
        or malicious.

        -------
        Parameters:
        - jsDirs: list of strings
            Directories containing the JS files to be analysed.
        - jsFiles: list of strings
            Files to be analysed.
        - model: String
            path to the model used to classify the new files
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        The results of the static analysis of the files given as input:
        either benign or malicious
    '''

    if jsDirs is None and jsFiles is None:
        print('Please, indicate a directory or a JS file to be studied')
    elif model is None:
        print('Please, indicate a model to be used to classify new files.\n'
              + '(see >$ python3 <path-of-MachineLearning/LearnModel.py> -help)'
              + ' to build a model)')
    else:
        csvFile = StaticAnalysisJs.mainS(jsDirs=jsDirs, jsFiles=jsFiles)
        Classification.testModel(csvFile, model[0])


if __name__ == "__main__": # Executed only if run as a script
    mainClassification()
