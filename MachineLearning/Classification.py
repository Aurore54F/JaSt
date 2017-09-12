
'''
    Classifying files.  Can deal with training, validation and test sets.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc

from scipy import interp  
#from sklearn.cross_validation import StratifiedKFold
from sklearn import svm, datasets

from sklearn.model_selection import StratifiedKFold


def classify(trainingFile):
    '''
        Training of a Naive Bayes Multinomial classifier.
                
        -------
        Parameter:
        - trainingFile: String
            Path of the CSV file to be used to build a model for.
            
        -------
        Returns:
        - Naive Bayes Multinomial model
            Beware: the model was implemented as a global variable in sklearn TODO.
        - Print the detection rate and the TP, FP, FN and TN rates of trainingFile tested with the model built from this file, in stdout.
    '''
    
    data = pd.read_csv(trainingFile)
        
    names = data['Outlook'] # Vector containing all the names of the samples considered
    labels = data['Label'] # Vector containing all the labels (i.e. 'benign', 'malicious', or '?') of the samples considered
    X = data.ix[:, '0':] # # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)
    
    clf = MultinomialNB()
    trained = clf.fit(X, labels) # Model
    
    #clf.predict_proba(X) # Returns the probability of the samples for each class in the model. The columns correspond 
        #to the classes in sorted order, as they appear in the attribute classes
        
        
    labelsPredicted = clf.predict(X) # Perform classification on an array of test vectors X and predict the target values
    accuracy = clf.score(X,labels) # Detection rate
    
    TN, FP, FN, TP = confusion_matrix(labels, labelsPredicted).ravel() # y = labels, predicted = labels predicted
    
    #print("Detection: " + str(accuracy))
    #print("TP: " + str(TP) + ", FP: " + str(FP) + ", FN: " + str(FN) + ", TN: " + str(TN))
    
    #for i in range(0, len(names)):
        #print(str(names[i]) + ': ' + str(labelsPredicted[i]) + ': ' + str(labels[i]))
    
    return trained;


def validate(validationFile, model):
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
    
    validationSet = pd.read_csv(validationFile)
        
    labelsValidation = validationSet['Label'] # Split off classifications
    XValidation = validationSet.ix[:, '0':] # Split off features
    XValidation = np.asarray(XValidation)
    

    validated = model.partial_fit(XValidation, labelsValidation, ['malicious', 'benign']) # Incremental fit on a batch of samples
    
    return validated

    
def test(testFile, model):
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
    
    testSet = pd.read_csv(testFile)
        
    labelsTest = testSet['Label'] # Split off classifications
    XTest = testSet.ix[:, '0':] # Split off features
    XTest = np.asarray(XTest)
    
    labelsPredictedTest = model.predict(XTest) # Perform classification on an array of test vectors X and predict the target values
    labelsPredictedProbaTest = model.predict_proba(XTest) # Perform classification on an array of test vectors X and predict the target values
    accuracyTest = model.score(XTest, labelsTest) # Detection rate
    
    TN_test, FP_test, FN_test, TP_test = confusion_matrix(labelsTest, labelsPredictedTest).ravel() # y = labels, predicted = labels predicted
    
    print("Detection: " + str(accuracyTest))
    print("TN: " + str(TN_test) + ", FP: " + str(FP_test) + ", TP: " + str(TP_test) + ", FN: " + str(FN_test))

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


def crossValidation(trainingFile, n_splits = 10):
    
    data = pd.read_csv(trainingFile)
    
    labels = data['Label'] # Vector containing all the labels (i.e. 'benign', 'malicious', or '?') of the samples considered
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)


    # Classification and ROC analysis
    
    # Run classifier with cross-validation and plot ROC curves
    
    cv = StratifiedKFold(n_splits=n_splits)
    classifier = BernoulliNB(binarize = 0.00000000000000000000001)
    
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
             label='Mean ROC (AUC = ' + str(round(roc_auc,4)) + ')',lw=1)
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    #plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

