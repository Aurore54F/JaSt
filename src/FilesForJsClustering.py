
'''
    Files production after analysis: histograms, PCA and n-grams frequency.
'''

import os # To create repositories

import PreprocessingJsData
import NGramsAnalysis

import __init__

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def classifierFormat(separatorData='comma'):
    '''
        Formatting the data stored in the soon to be exported file.

        -------
        Parameter:
        - separatorData: String
            Either 'comma' or 'tab'. Default value is 'comma'.

        -------
        Returns:
        - List
            Element 1 = formatt: separator (either ',' or '\t')
            Element 2 = extension: file extension (either '.csv' or '.txt').
    '''

    if separatorData.lower() == 'comma':
        formatt = ','
        extension = '.csv'
    elif separatorData.lower() == 'tab':
        formatt = '\t'
        extension = '.txt'
    else:
        print("Error on the separators' format name. Please indicate either\
        'comma' or 'tab'.")
        return
    l = [formatt] + [extension]
    return l



def saveProbaOfNGramsHisto(parser, allProba, filesStudied,
                           histoDir=currentPath+'/Histograms/'):
    '''
        From a list containing dictionaries, each containing n-grams (abscissa)
        with their associated probability (ordinate), saves the corresponding histograms.

        -------
        Parameters:
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - allProba: List of Dictionaries.
            Key: tuple representing an n-gram
            Value: probability of occurrences of a given tuple of n-gram.
            One dictionary corresponds to the analysis of one JS file.
        - filesStudied: List of Strings
            Contains the name of the well-formed JS files considered.
        - histoDir: String
            Path of the directory to store the histograms.

        -------
        Returns:
        - Files
            The number of .png files returned (i.e. of histograms) corresponds to the
            number of valid JS files (i.e. len(allProba) = len(filesStudied)).
    '''

    # Directory to store the histograms files
    if not os.path.exists(histoDir):
        os.makedirs(histoDir)

    i = 1
    histoFilePart1 = 'Histo' + parser

    for dico in allProba: # Data for the histogram (i.e. n-gram with occurrence)
        figPath = histoDir + histoFilePart1 + str(i)
        NGramsAnalysis.histoFromDico(dico, figPath, title=filesStudied[i-1])
        # Saving an histogram in png format.
        i += 1
    print('The histogram(s) have been successfully stored in ' + histoDir)

def savePcaPlotting(parser, fileAnalysis, plotDir=currentPath+'/PcaPlot/', label=None):
    '''
        Production of a graph representing each file features (i.e. list of n-grams with
        their associated probability) in 2D (using a PCA 2-dimensional transformation).

        -------
        Parameters:
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - fileAnalysis: File
            Contains for each JS file studied (row) the probability of occurrences of all
            the n-gram (column) encountered in the JS corpus considered.
        - plotDir: String
            Path of the directory to store the PCA representation.
        - label: String
            Indicates the label's name of the current data (if any), useful for supervised
            classification. Default value is None.

        -------
        Returns:
        - File
            Plots the multi dimensional vector representing the n-grams, using a 2-dimensional PCA.
    '''

    # Directory to store the histograms files
    if not os.path.exists(plotDir):
        os.makedirs(plotDir)
    NGramsAnalysis.pcaPlotting(fileAnalysis, plotDir + parser + 'PcaPlotting', label=label)
    print('The PCA\'s results have been successfully stored in ' + plotDir)


def saveProbaOfNGramsFileHeader(parser, allProba, simplifiedListNGrams, dicoNgramIint, formatt,
                                extension,
                                fileDir=currentPath+'/MatrixFiles/', label=None):
    '''
        Writes the header (i.e. columns labeling) of the file containing the analysis.

        -------
        Parameters:
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - allProba: List of Dictionaries.
            Key: tuple representing an n-gram
            Value: probability of occurrences of a given tuple of n-gram.
            One dictionary corresponds to the analysis of one JS file.
        - simplifiedListNGrams: Set
            Contains tuples representing n-grams whose probability of occurrences is not null.
        - dicoNgramIint: Dictionary
            Key: N-gram
            Value: Unique integer.
        - formatt: String
            Separator (either ',' or '\t').
        - extension: String
            File extension (either '.csv' or '.txt').
        - fileDir: String
            Path of the directory to store the csv/txt files containing the analysis.
        - label: String
            Indicates the label's name of the current data (if any), useful for supervised
            classification. Default value is None.

        -------
        Returns:
        - File
            Contains the header for the analysis file (i.e. labels/numbers the columns).
    '''

    # Directory to store the matrix files
    if not os.path.exists(fileDir):
        print('Here')
        os.makedirs(fileDir)

    with open(fileDir + parser + extension, 'w') as expFile:
        expFile.write('Outlook')
        if label is not None and label != []:
            expFile.write(formatt + 'Label')

        if allProba is not None and allProba != []:
            vectNGramsProba = PreprocessingJsData.jsToProbaOfNGramsComplete(allProba[0],\
                               simplifiedListNGrams, dicoNgramIint)
            # allProba[0] being a dictionary representing
            #the analysis of one JS file (i.e. n-gram with associated probability).
            # vectNGramsProba contains at position i the probability of encountering the n-gram
            #mapped to the integer i (see the complete mapping in DicoNGramsToInt.py).
            for j, k in enumerate(vectNGramsProba):
                expFile.write(formatt + str(j)) # Columns labeling
            expFile.write('\n')


def saveProbaOfNGramsFileContent(parser, allProba, simplifiedListNGrams, dicoNgramIint,
                                 filesStudied, formatt, extension,
                                 fileDir=currentPath+'/MatrixFiles/', label=None):
    '''
        Writes in a file, for each JS file studied (row), the probability of occurrences
        of all the n-gram (column) encountered in the JS corpus considered.

        -------
        Parameters:
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - allProba: List of Dictionaries.
            Key: tuple representing an n-gram
            Value: probability of occurrences of a given tuple of n-gram.
            One dictionary corresponds to the analysis of one JS file.
        - simplifiedListNGrams: Set
            Contains tuples representing n-grams whose probability of occurrences is not null.
        - dicoNgramIint: Dictionary
            Key: N-gram
            Value: Unique integer.
        - filesStudied: List of Strings
            Contains the name of the well-formed JS files.
        - formatt: String
            Separator (either ',' or '\t').
        - extension: String
            File extension (either '.csv' or '.txt').
        - fileDir: String
            Path of the directory to store the csv/txt files for Weka/xcluster.
        - label: String
            Indicates the label's name of the current data (if any), useful for supervised
            classification. Default value is None.

        -------
        Returns:
        - File
            Contains for each JS file studied (row) the probability of occurrences of all the
            n-gram (column) encountered in the JS corpus considered.
    '''

    i = 1

    # Directory to store the matrix files
    if not os.path.exists(fileDir):
        print('File does not exist.')

    with open(fileDir + parser + extension, 'a') as expFile:
        for dicoJS in allProba: # Dico for one JS file, key = n-gram and value = proba
            vectNGramsProba = PreprocessingJsData.jsToProbaOfNGramsComplete(dicoJS,\
                               simplifiedListNGrams, dicoNgramIint)
            # Contains at position i the probability of encountering the n-gram mapped to the
            #integer i (see the complete mapping in DicoNGramsToInt.py).
            expFile.write(filesStudied[i-1] + formatt) # Name of the current file
            if label is not None and label != []:
                expFile.write(label[i - 1] + formatt) # i - 1 as initially i value is 1
            for el in range(len(vectNGramsProba)-1):
                expFile.write(str(vectNGramsProba[el]) + formatt)
            expFile.write(str(vectNGramsProba[len(vectNGramsProba)-1]))
            # Last one could not be in the previous
            #loop, otherwise the last character would have been a separator.
            expFile.write('\n')
            i += 1

    print('The results of the analysis (n-grams frequency) have been successfully stored in '\
          + fileDir)

    return fileDir + parser + extension
