#!/usr/bin/python


'''
    Static analysis (lexical or syntactical) of JavaScript files given in input.
'''

import os
import argparse # To parse command line arguments

import __init__


import PreprocessingJsData
import NGramsRepresentation
import FilesForJsClustering

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
          * labels=args['l'],
          * parser=args['p'][0],
          * n=args['n'][0],
          * separator=args['s'][0],
          * updateDico=args['u'][0],
          * histo=args['h'][0],
          * fileProd=args['e'][0],
          * pcaProd=args['g'][0],
          * pathHisto=args['hp'][0],
          * pathFile=args['ep'][0],
          * pathPca=args['gp'][0]
          A more thorough description can be obtained:
            >$ python3 <path-of-src/MainStaticAnalysis.py> -help
    '''

    parser = argparse.ArgumentParser(description='Given a list of repositories or files paths,\
    analyse whether the JS files are either benign or malicious.')

    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analysed')
    parser.add_argument('--d', metavar='DIR', type=str, nargs='+', help='directories containing\
    the JS files to be analysed')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+', default=['?'],\
                        help='label for the files to be analysed')

    parser.add_argument('--p', metavar='PARSER', type=str, nargs=1, choices=['esprimaAst',\
                        'esprimaAstSimp', 'esprima', 'slimIt'], default=['esprimaAstSimp'],\
					help='parser\'s name')
    parser.add_argument('--e', metavar='BOOL', type=bool, nargs=1, default=[True],\
                    help='produce a csv/txt file for machine learning schemes')
    parser.add_argument('--s', metavar='SEPARATOR', type=str, nargs=1, choices=['comma', 'tab'],\
                        default=['comma'], help='separator\'s format for machine learning schemes')
    parser.add_argument('--ep', metavar='FILE-PATH', type=str, nargs=1,\
                    default=[currentPath+'/MatrixFiles/'],\
                    help='path of the directory to store the csv/txt file for machine\
                    learning schemes')
    parser.add_argument('--h', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='produce histograms from the JS corpus')
    parser.add_argument('--hp', metavar='FILE-PATH', type=str, nargs=1,\
                    default=[currentPath+'/Histograms/'],\
                    help='path of the directory to store the histograms')
    parser.add_argument('--g', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='produce a graphical 2D representation of the files from the JS corpus')
    parser.add_argument('--gp', metavar='FILE-PATH', type=str, nargs=1, \
                    default=[currentPath+'/PcaPlot/'],\
                    help='path of the directory to store the PCA graph')
    parser.add_argument('--u', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='indicates whether the dictionary mapping n-grams and integers\
                    has to be updated')
    parser.add_argument('--n', metavar='INTEGER', type=int, nargs=1, default=[4],\
                    help='stands for the size of the sliding-window which goes through\
                    the previous list')

    args = vars(parser.parse_args())

    return args


def handleDirs(allNGrams, directory, labels, parser, n):
    '''
        Analysing the JS files contained in the directories given as input in the command line.

        -------
        Parameters:
        - allNGrams: list of lists
            Will be returned once filled.
        - directory: list
            Contains the paths of the directories containing the JS files to be analysed.
        - labels: list of strings
            Indicates the label's name of the current data (if any), useful for supervised
            classification.
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
            Default value is 4.

        -------
        Returns:
        - List of lists
            * List 1:
                Contains one dictionary per JS file:
                    Key: tuple representing an n-gram;
                    Value: probability of occurrences of a given tuple of n-gram.
                    The dictionary corresponds to the analysis of one JS file.
            * List 2:
                Contains the name of the well-formed JS files.
            * List 3:
                Only if Label is not None. Contains the label assigned to all the files in jsDir.
    '''

    i = 0
    newLabels = ['?' for j in range(len(directory))]
    for j in range(len(labels)):
        newLabels[j] = labels[j] # To be sure that every directory has a label,
        #default value being '?'
    for jsDir in directory:
        preprocess1Dir = PreprocessingJsData.dicoOfAllNGrams(parser, jsDir, newLabels[i], n)
        # args = parser, JsDirectory, label, n

        allNGrams[0] += preprocess1Dir[0] # Contains one dictionary per JS file:
        #key = tuple representing an n-gram and value = probability of occurrences of a
        #given tuple of n-gram.
        allNGrams[1] += preprocess1Dir[1] # Contains the name of the well-formed JS files.
        allNGrams[2] += preprocess1Dir[2] # Contains the label of the well-formed JS files.
        i += 1
    return allNGrams


def handleFiles(allNGrams, jsFiles, labels, parser, n):
    '''
        Analysing the JS files given as input in the command line.

        -------
        Parameters:
        - allNGrams: list of lists
            Will be returned once filled.
        - jsFiles: list
            Contains the paths of the JS files to be analysed.
        - labels: list of strings
            Indicates the label's name of the current data (if any), useful for supervised
            classification.
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
            Default value is 4.

        -------
        Returns:
        - List of lists
            * List 1:
                Contains one dictionary per JS file:
                    Key: tuple representing an n-gram;
                    Value: probability of occurrences of a given tuple of n-gram.
                    The dictionary corresponds to the analysis of one JS file.
            * List 2:
                Contains the name of the well-formed JS files.
            * List 3:
                Only if Label is not None. Contains the label assigned to all the files in jsDir.
    '''

    i = 0
    newLabels = ['?' for j in range(len(jsFiles))]
    for j in range(len(labels)):
        newLabels[j] = labels[j] # To be sure that every file has a label,
        #default value being '?'
    for jsFile in jsFiles:
        dico = PreprocessingJsData.jsToProbaOfNGrams(parser, jsFile, n)
        # args = parser, JsDirectory, n
        if dico is not None:
            allNGrams[0].append(dico)
            # Contains one dictionary per JS file: key = tuple representing
            #an n-gram and value = probability of occurrences of a given tuple of n-gram.
            allNGrams[1] += [jsFile] # Contains the name of the well-formed JS files.
            allNGrams[2] += newLabels[i] # Contains the label of the well-formed JS files.
            i += 1
    return allNGrams




def mainS(jsDirs='', jsFiles='', labels='', parser='esprimaAstSimp',\
         n=[4], sep='comma', updateDico=False, histo=False,\
         fileProd=True, pcaProd=False, pathHisto=currentPath+'/Histograms/',\
         pathFile=currentPath+'/MatrixFiles/', pathPca=currentPath+'/PcaPlot/'):
    '''
        Main function, performs a static analysis (lexical or syntactical)
        of JavaScript files given in input.

        -------
        Parameters:
        - jsDirs: list of strings
            Directories containing the JS files to be analysed.
        - jsFiles: list of strings
            Files to be analysed.
        - labels: list of strings
            Indicates the label's name of the current data (if any), useful for supervised
            classification.
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
        - sep: string
            Separator's format for machine learning schemes.
        - updateDico: boolean
            Indicates whether the dictionary mapping n-grams and integers
                    has to be updated.
        - histo: boolean
            Production of histograms from the JS corpus.
        - fileProd: boolean
            Production of a csv/txt file for machine learning schemes.
        - pcaProd: boolean
            Production of a graphical 2D representation of the files from the JS corpus.
        - pathHisto: string
            Path of the directory to store the histograms.
        - pathFile: string
            Path of the directory to store the csv/txt file for machine learning schemes.
        - pathPca: string
            Path of the directory to store the PCA graph.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        The results of the static analysis of the files given as input.
        These are stored in the MalwareClustering directory.
    '''

    if jsDirs is None and jsFiles is None:
        print('Please, indicate a directory or a JS file to be studied')

    else:
        allNGrams = [[] for j in range(3)]
        if jsDirs is not None:
            handleDirs(allNGrams, jsDirs, labels, parser, n)
            # Args: directory, labels, parser, n

        if jsFiles is not None:
            handleFiles(allNGrams, jsFiles, labels, parser, n)

        if allNGrams != [[]]:
            allProba = allNGrams[0] # Contains one dictionary per JS file: key = tuple representing
            #an n-gram and value = probability of occurrences of a given tuple of n-gram.
            filesStudied = allNGrams[1] # Contains the name of the well-formed JS files.
            labels = allNGrams[2] # Contains the label of the well-formed JS files.

            formatt = FilesForJsClustering.classifierFormat(sep)[0]
            # Separator between the value: either ',' or '\t' (arg = separator).
            extension = FilesForJsClustering.classifierFormat(sep)[1]
            # File extension: either '.csv' or '.txt' (arg = separator).

            simplifiedListNGrams = PreprocessingJsData.simplifiedDicoOfAllNGrams(allProba)
            # Set containing the name of the n-grams present in our JS corpus.

            if updateDico: # Update the dictionaries DicoNGramsToInt and DicoIntToNgrams
                NGramsRepresentation.mappingNGramsInt(simplifiedListNGrams, parser)

            if histo: # Production of the histograms
                FilesForJsClustering.saveProbaOfNGramsHisto(parser, allProba,\
                                                        filesStudied, histoDir=pathHisto)

            if fileProd: # Production of the analysis csv/txt file
                dicoNGramsToInt = NGramsRepresentation.dicoNGramsToIntUsed(parser)
                FilesForJsClustering.saveProbaOfNGramsFileHeader(parser, allProba,\
                                      simplifiedListNGrams, dicoNGramsToInt, formatt, extension,\
                                      pathFile, labels)
                file = FilesForJsClustering.saveProbaOfNGramsFileContent(parser, allProba,\
                                    simplifiedListNGrams, dicoNGramsToInt, filesStudied, formatt,
                                    extension, pathFile, labels)

            if pcaProd:
                FilesForJsClustering.savePcaPlotting(parser, file,\
                                                    plotDir=pathPca, label=labels)

            if fileProd:
                return file;
