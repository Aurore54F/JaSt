
# DRAFT: WILL BE DELETED, see Classification.py


import pandas as pd
import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix


def classify(trainingFile ='/home/aurore/Documents/Code/JS-samples5-mixed/MatrixFilesesprimaAstSimp.csv', 
             validationFile = '/home/aurore/Documents/Code/MatrixFiles/esprimaAstSimp.csv', 
             testFile = '/home/aurore/Documents/Code/esprimaAstSimp.csv'):
    
    data = pd.read_csv(trainingFile)
        
    names = data['Outlook']
    labels = data['Label']      # Split off classifications
    X = data.ix[:, '0':]  # Split off features
    X = np.asarray(X)
    
    
    validationSet = pd.read_csv(validationFile)
        
    labelsValidation = validationSet['Label']      # Split off classifications
    XValidation = validationSet.ix[:, '0':]  # Split off features
    XValidation = np.asarray(XValidation)
    
    #classes = 
    
    
    testSet = pd.read_csv(testFile)
        
    labelsTest = testSet['Label']      # Split off classifications
    XTest = testSet.ix[:, '0':]  # Split off features
    XTest = np.asarray(XTest)
    
    
    clf = MultinomialNB()
    trained = clf.fit(X, labels)
    
    #clf.predict_proba(X) # Returns the probability of the samples for each class in the model. The columns correspond 
        #to the classes in sorted order, as they appear in the attribute classes
        
    labelsPredicted = clf.predict(X) # Perform classification on an array of test vectors X and predict the target values
    accuracy = clf.score(X,labels) # Detection rate
    
    cm = confusion_matrix(labels, labelsPredicted) # y = labels, predicted = labels predicted
    TP = cm[0][0]
    FP = cm[0][1]
    FN = cm[1][0]
    TN = cm[1][1]
    
    print("Detection: " + str(accuracy))
    print("TP: " + str(TP) + ", FP: " + str(FP) + ", FN: " + str(FN) + ", TN: " + str(TN))
    
    #for i in range(0, len(names)):
        #print(str(names[i]) + ': ' + str(labelsPredicted[i]) + ': ' + str(labels[i]))
    
    
    labelsPredictedTest = trained.predict(XTest) # Perform classification on an array of test vectors X and predict the target values
    accuracyTest = trained.score(XTest, labelsTest) # Detection rate
    
    cmTest = confusion_matrix(labelsTest, labelsPredictedTest) # y = labels, predicted = labels predicted
    TP_test = cmTest[0][0]
    FP_test = cmTest[0][1]
    FN_test = cmTest[1][0]
    TN_test = cmTest[1][1]
    
    print("Detection: " + str(accuracyTest))
    print("TP: " + str(TP_test) + ", FP: " + str(FP_test) + ", FN: " + str(FN_test) + ", TN: " + str(TN_test))
    
    
    validated = trained.partial_fit(XValidation, labelsValidation, ['malicious', 'benign']) # Incremental fit on a batch of samples
    
    labelsPredictedValidation = validated.predict(XTest) # Perform classification on an array of test vectors X and predict the target values

    accuracyValidation = validated.score(XTest, labelsTest) # Detection rate
    cmValidation = confusion_matrix(labelsTest, labelsPredictedValidation) # y = labels, predicted = labels predicted
    TP_Validation = cmValidation[0][0]
    FP_Validation = cmValidation[0][1]
    FN_Validation = cmValidation[1][0]
    TN_Validation = cmValidation[1][1]
    
    print("Detection: " + str(accuracyValidation))
    print("TP: " + str(TP_Validation) + ", FP: " + str(FP_Validation) + ", FN: " + str(FN_Validation) + ", TN: " + str(TN_Validation))
    
    
    