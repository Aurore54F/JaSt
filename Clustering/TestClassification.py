

import pandas as pd
import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix


def classify(file ='/home/aurore/Documents/Code/JS-samples5-mixed/MatrixFilesesprimaAstSimp.csv'):
    
    data = pd.read_csv(file)
        
    labels = data['Label']      # Split off classifications
    X = data.ix[:, '0':]  # Split off features
    X = np.asarray(X)
    
    
    fileTest = '/home/aurore/Documents/Code/MatrixFiles/esprimaAstSimp.csv'
    testSet = pd.read_csv(fileTest)
        
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
    
    
    labelsPredictedTest = trained.predict(XTest) # Perform classification on an array of test vectors X and predict the target values
    accuracyTest = trained.score(XTest, labelsTest) # Detection rate
    
    cmTest = confusion_matrix(labelsTest, labelsPredictedTest) # y = labels, predicted = labels predicted
    TP_test = cmTest[0][0]
    FP_test = cmTest[0][1]
    FN_test = cmTest[1][0]
    TN_test = cmTest[1][1]
    
    print("Detection: " + str(accuracyTest))
    print("TP: " + str(TP_test) + ", FP: " + str(FP_test) + ", FN: " + str(FN_test) + ", TN: " + str(TN_test))
    
