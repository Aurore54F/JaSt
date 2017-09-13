
'''
    Classifying files. Can deal with training, validation and test sets.
'''

import os
import argparse # To parse command line arguments
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
import pickle

from scipy import interp
from sklearn.model_selection import StratifiedKFold

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
from __init__ import *


def classify(trainingFile, modelDir=currentPath+'/Classification/',\
             modelName='/model', printScore=False, printRes=False):
    '''
        Training of a Naive Bayes Multinomial classifier.
      
        -------
        Parameter:
        - trainingFile: String
            Path of the CSV file to be used to build a model for.
        - modelDir
        
        - modelName
        
        - printScore
        
        - printRes
        

        -------
        Returns:
        - Naive Bayes Multinomial model
            Beware: the model was implemented as a global variable in sklearn TODO.
        - Print the detection rate and the TP, FP, FN and TN rates of trainingFile tested with the model built from this file, in stdout.
    '''

    # Directory to store the classification related files
    if not os.path.exists(modelDir):
        os.makedirs(modelDir)

    data = pd.read_csv(trainingFile)

    names = data['Outlook'] # Vector containing all the names of the samples considered
    labels = data['Label'] # Vector containing all the labels (i.e. 'benign', 'malicious', or '?') of the samples considered
    X = data.ix[:, '0':] # # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)

    clf = MultinomialNB()
    trained = clf.fit(X, labels) # Model

    clf.predict_proba(X) # Returns the probability of the samples for each class in the model. The columns correspond 
        #to the classes in sorted order, as they appear in the attribute classes

    labelsPredicted = clf.predict(X) # Perform classification on an array of test vectors X and predict the target values
    accuracy = clf.score(X,labels) # Detection rate
    
    if printScore:
        TN, FP, FN, TP = confusion_matrix(labels, labelsPredicted).ravel() # y = labels, predicted = labels predicted
        print("Detection: " + str(accuracy))
        print("TP: " + str(TP) + ", FP: " + str(FP) + ", FN: " + str(FN) + ", TN: " + str(TN))
    
    if printRes:
        for i in range(0, len(names)):
            print(str(names[i]) + ': ' + str(labelsPredicted[i]) + ' (' + str(labels[i]) + ')')
        print('> Name: labelPredicted (trueLabel)')
    
    pickle.dump(trained, open(modelDir + modelName, 'wb'))
    
    return trained;


def validate(validationFile, model, modelDir=currentPath+'/Classification/',\
             modelName='/model'):
    '''
        Extension of a Naive Bayes Multinomial classification model with a new CSV file of the same format.

        -------
        Parameter:
        - validationFile: String
            Path of the CSV file to be used to extend the following model.
        - model
            Naive Bayes Multinomial model.
        Beware: the model must have been constructed using files of the same format (i.e. same attributes) as the format of validationFile.

        -------
        Returns:
        - Naive Bayes Multinomial model.
            Beware: the model was implemented as a global variable in sklearn TODO.
    '''

    if type(model) is str:
        model = pickle.load(open(model, 'rb'))

    validationSet = pd.read_csv(validationFile)

    labelsValidation = validationSet['Label'] # Split off classifications
    XValidation = validationSet.ix[:, '0':] # Split off features
    XValidation = np.asarray(XValidation)

    validated = model.partial_fit(XValidation, labelsValidation, ['malicious', 'benign']) # Incremental fit on a batch of samples

    pickle.dump(validated, open(modelDir + modelName, 'wb'))
    return validated


def testModel(testFile, model, printRes=True):
    '''
        Test of a Naive Bayes Multinomial classification model with a new CSV file of the same format.

        -------
        Parameter:
        - testFile: String
            Path of the CSV file to be tested using the following model.
        - model
            Naive Bayes Multinomial model.
        Beware: the model must have been constructed using files of the same format (i.e. same attributes) as the format of testFile.

        -------
        Returns:
        - Naive Bayes Multinomial model.
            Beware: the model was implemented as a global variable in sklearn TODO.
        - Print the detection rate and the TP, FP, FN and TN rates of testFile tested with model, in stdout.
    '''

    if type(model) is str:
        model = pickle.load(open(model, 'rb'))

    testSet = pd.read_csv(testFile)

    names = testSet['Outlook'] # Vector containing all the names of the samples considered
    labelsTest = testSet['Label'] # Split off classifications
    XTest = testSet.ix[:, '0':] # Split off features
    XTest = np.asarray(XTest)

    labelsPredictedTest = model.predict(XTest) # Perform classification on an array of test vectors X and predict the target values
    labelsPredictedProbaTest = model.predict_proba(XTest) # Perform classification on an array of test vectors X and predict the target values
    accuracyTest = model.score(XTest, labelsTest) # Detection rate

    #TN_test, FP_test, FN_test, TP_test = confusion_matrix(labelsTest, labelsPredictedTest).ravel() # y = labels, predicted = labels predicted

    #print("Detection: " + str(accuracyTest))
    #print("TN: " + str(TN_test) + ", FP: " + str(FP_test) + ", TP: " + str(TP_test) + ", FN: " + str(FN_test))
    
    if printRes:
        for i in range(0, len(names)):
            print(str(names[i]) + ': ' + str(labelsPredictedTest[i]) + ' (' + str(labelsTest[i]) + ')')
        print('> Name: labelPredicted (trueLabel)')

    '''
    fpr, tpr, thresholds = roc_curve(labelsTest, labelsPredictedProbaTest[:,0],pos_label = 'benign')
    print('Threshold: ' + str(thresholds))
    print("AUC of the predictions: {0}".format(metrics.auc(fpr, tpr)))
    roc_auc = auc(fpr,tpr)

    plt.figure()
    lw = 1

    plt.plot(fpr, tpr, color='red', lw=lw, label='ROC curve (AUC = ' + str(round(roc_auc,4)) + ')')
    plt.plot([0, 1], [0, 1], color='grey', lw=lw, linestyle='--', label = 'Luck')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    #plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()
    '''

def parsingCommandsClustering():
    '''
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * jsDirs=args['d'],
          * jsFiles=args['f'],
          * parser=args['p'][0],
          * n=args['n'][0],
          * nbCluster=args['c'][0],
          * displayFig=args['g'][0],
          A more thorough description can be obtained:
            >$ python3 <path-of-MachineLearning/Clustering.py> -help
    '''

    parser = argparse.ArgumentParser(description='Given a list of repositories or files paths,\
    cluster the JS files into several families.')

    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analysed')
    parser.add_argument('--d', metavar='DIR', type=str, nargs='+', help='directories containing\
    the JS files to be analysed')
    parser.add_argument('--m', metavar='MODEL', type=str, nargs='+', help='model used to classify the new files')


    args = vars(parser.parse_args())

    return args


argObjC = parsingCommandsClustering()


def mainClassification(jsDirs=argObjC['d'], jsFiles=argObjC['f'], model=argObjC['m']):
    '''
        Main function, performs a static analysis (lexical or syntactical)
        of JavaScript files given in input.

        -------
        Parameters:
        - jsDirs: list of strings
            Directories containing the JS files to be analysed.
        - jsFiles: list of strings
            Files to be analysed.
        - parser: String
            Either 'slimIt', 'esprima', 'esprimaAst', or 'esprimaAstSimp'.
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
        - nbCluster: int
            Number of clusters whished.
        - displayFig: boolean
            Production of a graphical 2D representation of the files from the JS corpus.
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
        csvFile = StaticAnalysisJs.mainS(jsDirs=jsDirs, jsFiles=jsFiles)
        testModel(csvFile, model[0])


if __name__ == "__main__": # Executed only if run as a script
    mainClassification()



def crossValidation(trainingFile, n_splits = 10):
    '''
        x-fold cross-validation and ROC analysis.
    '''

    data = pd.read_csv(trainingFile)

    labels = data['Label'] # Vector containing all the labels (i.e. 'benign', 'malicious', or '?') of the samples considered
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)

    cv = StratifiedKFold(n_splits=n_splits)
    classifier = MultinomialNB()

    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []

    i = 0
    for train, test in cv.split(X,labels):
        model = classifier.fit(X[train], labels[train])
        labelsPredicted = model.predict(X[test])
        labelsPredictedProba = model.predict_proba(X[test])
        # Compute ROC curve and area the curve      

        accuracyTest = model.score(X, labels) # Detection rate

        TN_test, FP_test, FN_test, TP_test = confusion_matrix(labels[test], labelsPredicted).ravel() # y = labels, predicted = labels predicted

        print("Detection: " + str(accuracyTest))
        print("TN: " + str(TN_test) + ", FP: " + str(FP_test) + ", TP: " + str(TP_test) + ", FN: " + str(FN_test))

        fpr, tpr, thresholds = roc_curve(labels[test], labelsPredictedProba[:,0],pos_label = 'benign')
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold ' + str(i) + ' (AUC = ' + str(round(roc_auc,4)) + ')')
        i += 1

    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    mean_tpr /= n_splits
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='Mean ROC (AUC = ' + str(round(mean_auc,4)) + ')',lw=1)

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title('Receiver operating characteristic curves')
    plt.legend(loc="lower right")
    plt.show()

