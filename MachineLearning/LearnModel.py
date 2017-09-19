
'''
    Main module to build a model to classify future JavaScript files.
'''

import os
import argparse

import Classification
from __init__ import *

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def parsingCommands():
    '''
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * jsDirs=args['d'],
          * jsFiles=args['f'],
          * labels=arfs['l'],
          * modelDir=args['md']
          * modelName=args['mn']
          * printScore=args['ps']
          * printRes=args['pr']
          A more thorough description can be obtained:
            >$ python3 <path-of-MachineLearning/LearnModel.py> -help
    '''

    parser = argparse.ArgumentParser(description='Given a list of repositories or JS files paths,\
    construct a model to classify future JavaScript files.')

    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be used\
                        to build a model from')
    parser.add_argument('--d', metavar='DIR', type=str, nargs='+', help='directories to be\
                        used to build a model from')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+', choices=['benign',\
                                                                              'malicious'],\
                        help='labels of the JS files used to construct a model from')
    parser.add_argument('--md', metavar='MODEL-DIR', type=str, nargs=1,\
                    default=[currentPath+'/Classification/'],\
                    help='path to store the model that will be produced')
    parser.add_argument('--mn', metavar='MODEL-NAME', type=str, nargs=1,\
                    default=['model'],\
                    help='name of the model that will be produced')
    parser.add_argument('--ps', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='indicates whether to print or not the classifier\'s performance')
    parser.add_argument('--pr', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='indicates whether to print or not the classifier\'s predictions')

    args = vars(parser.parse_args())
    return args


argObjC = parsingCommands()


def mainLearn(jsDirs=argObjC['d'], jsFiles=argObjC['f'], labels=argObjC['l'],\
              modelDir=argObjC['md'], modelName=argObjC['mn'], printScore=argObjC['ps'],\
              printRes=argObjC['pr']):
    '''
        Main function, performs a static analysis (lexical or syntactical)
        of JavaScript files given as input to build a model to classify future JavaScript files.

        -------
        Parameters:
        - jsDirs: list of strings
            Directories containing the JS files to be analysed.
        - jsFiles: list of strings
            Files to be analysed.
        - labels: list of strings
            Indicates the label's name of the current data: either benign or malicious.
        - modelDir: String
            Path to store the model that will be produced.
            Default value being the folder MalwareClustering/Classification/.
        - modelName: String
            Name of the model that will be produced.
            Default value being model.
        - printScore: Boolean
            Indicates whether to print or not the classifier's performance.
        - printRes: Boolean
            Indicates whether to print or not the classifier's predictions.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        - Naive Bayes Multinomial model
            Beware: the model was implemented as a global variable in sklearn.
    '''

    if jsDirs is None and jsFiles is None:
        print('Please, indicate a directory or a JS file to be used' +
              ' to build a model from')
    elif labels is None:
        print('Please, indicate the labels (either benign or malicious) of the files' +
        ' used to build the model')
    else:
        csvFile = StaticAnalysisJs.mainS(jsDirs=jsDirs, jsFiles=jsFiles, labels=labels)
        Classification.classify(csvFile, modelDir[0], modelName[0],\
                                printScore[0], printRes[0])


if __name__ == "__main__": # Executed only if run as a script
    mainLearn()
