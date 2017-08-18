
'''
    Classifying files.  Can deal with training, validation and test sets.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc


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
    
    cm = confusion_matrix(labels, labelsPredicted) # y = labels, predicted = labels predicted
    TP = cm[0][0]
    FP = cm[0][1]
    FN = cm[1][0]
    TN = cm[1][1]
    
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
    #labelsTest = np.asarray(labelsTest)
    XTest = testSet.ix[:, '0':] # Split off features
    XTest = np.asarray(XTest)
    
    
    labelsPredictedTest = model.predict(XTest) # Perform classification on an array of test vectors X and predict the target values
    accuracyTest = model.score(XTest, labelsTest) # Detection rate
    
    cmTest = confusion_matrix(labelsTest, labelsPredictedTest) # y = labels, predicted = labels predicted
    TP_test = cmTest[0][0]
    FP_test = cmTest[0][1]
    FN_test = cmTest[1][0]
    TN_test = cmTest[1][1]
    
    print("Detection: " + str(accuracyTest))
    print("TP: " + str(TP_test) + ", FP: " + str(FP_test) + ", FN: " + str(FN_test) + ", TN: " + str(TN_test))
    
    
def rocAnalysis(labels, labelsPredicted):
    '''
        TODO ROC analysis, plots ROC curve and gives AUC
    ''' 
    
    labelsTestInt = []
    for el in labels:
        if el == 'benign':
            labelsTestInt.append(1)
        else:
            labelsTestInt.append(-1)
        
    labelsPredictedTestInt = []
    for el in labelsPredicted:
        if el == 'benign':
            labelsPredictedTestInt.append(1)
        else:
            labelsPredictedTestInt.append(-1)
            
            
    fpr, tpr, thresholds = metrics.roc_curve(labelsTestInt, labelsPredictedTestInt, pos_label=1)
    print("AUC of the predictions: {0}".format(metrics.auc(fpr, tpr)))
    roc_auc = auc(fpr,tpr)
    
    plt.figure()
    lw = 2
    
    plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()
    
    