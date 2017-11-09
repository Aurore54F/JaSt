
'''
    Main module to update a model to classify future JavaScript files.
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
          * oldModel=args['m'],
          * modelDir=args['md']
          * modelName=args['mn']
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
    parser.add_argument('--m', metavar='OLD-MODEL', type=str, nargs=1, help='path of the old model\
    you wish to update with new JS files')
    parser.add_argument('--md', metavar='MODEL-DIR', type=str, nargs=1,\
                    default=[currentPath+'/Classification/'],\
                    help='path to store the model that will be produced')
    parser.add_argument('--mn', metavar='MODEL-NAME', type=str, nargs=1,\
                    default=['model'],\
                    help='name of the model that will be produced')

    args = vars(parser.parse_args())
    return args


argObjC = parsingCommands()


def mainUpdate(jsDirs=argObjC['d'], jsFiles=argObjC['f'], labels=argObjC['l'],\
              oldModel=argObjC['m'], modelDir=argObjC['md'], modelName=argObjC['mn']):
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
        - oldModel: String
            Path of the old model you wish to update with new JS files.
        - modelDir: String
            Path to store the model that will be produced.
            Default value being the folder MalwareClustering/Classification/.
        - modelName: String
            Name of the model that will be produced.
            Default value being model.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        - Naive Bayes Multinomial model
            Beware: the model was implemented as a global variable in sklearn.
    '''

    if jsDirs is None and jsFiles is None:
        print('Please, indicate a directory or a JS file to be used\
              to update the old model with')
    elif labels is None:
        print('Please, indicate the labels (either benign or malicious) of the files' +
              ' used to update the model')
    elif oldModel is None:
        print('Please, indicate the path of the old model you would like to update.\n'
              + '(see >$ python3 <path-of-MachineLearning/LearnModel.py> -help)'
              + ' to build a model)')
    else:
        csvFile = StaticAnalysisJs.mainS(jsDirs=jsDirs, jsFiles=jsFiles, labels=labels)
        Classification.validate(csvFile, oldModel[0], modelDir[0], modelName[0])


if __name__ == "__main__": # Executed only if run as a script
    mainUpdate()
