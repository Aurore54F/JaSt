#!/usr/bin/python

"""
    Obtaining the optimal set of hyperparameters.
"""

import logging
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, roc_curve

import utility
import static_analysis


def get_optimal_threshold(fpr, tpr, thresholds):
    """
        Determine the optimal threshold (= probability of a sample being malicious over which the
        sample will be classified as malicious) to optimize the detection accuracy.
        Beware, this functionality should be used with cross-validation, so as to not over-fit
        our data.

        -------
        Parameters:
        - fpr: list
            Contains the false positive rate for a given threshold.
        - tpr: list
            Contains the true positive rate for a given threshold.
        - thresholds: list
            Contains the different thresholds tested.

        -------
        Returns:
        - list
            Contains the predicted labels of the files being analysed.
    """

    youden_j = -1  # Youden's J statistic algorithm
    pos_optimal_threshold = -1

    for i in range(0, len(fpr)):
        if (- fpr[i] + tpr[i]) > youden_j:
            youden_j = - fpr[i] + tpr[i]
            pos_optimal_threshold = i

    optimal_threshold = thresholds[pos_optimal_threshold]
    logging.info('Optimal threshold: ' + str(optimal_threshold))

    return optimal_threshold


def random_grid_search(js_dirs, labels_d, n=4, tolerance='false', dict_not_hash=True):
    """
        Random search algorithm to get the optimal set of hyperparameters.

        -------
        Parameter:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed. Format: [Dir1, Dir2]
        - labels_d: list of strings
            Indicates the label's name of the current data: either benign or malicious.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed. Default: 4.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
            Default: False.

        -------
        Returns:
        - RandomForestClassifier:
            The classifier with the best set of hyperparameters.
    """

    names, train_features, train_labels = static_analysis.main_analysis \
        (js_dirs=js_dirs, labels_dirs=labels_d, js_files=None, labels_files=None,
         tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

    # Number of trees in the forest
    n_estimators = [int(x) for x in np.linspace(start=100, stop=1000, num=10)]

    # Number of features to consider at each split
    max_features = ['auto', 'log2']

    # Maximum number of levels in the tree
    max_depth = [int(x) for x in np.linspace(start=10, stop=120, num=12)]
    max_depth.append(None)

    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10, 20, 30, 40, 50]

    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 5, 10, 20, 30, 40, 50]

    # Whether to use out-of-bag samples to estimate the generalization accuracy
    oob_score = [True, False]

    # Criterion to measure the quality of a split
    criterion = ['gini', 'entropy']

    # Create the grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   # 'min_samples_split': min_samples_split,
                   # 'min_samples_leaf': min_samples_leaf,
                   # 'oob_score': oob_score,
                   # 'criterion': criterion
                   }

    clf_rf = utility.classifier_choice(estimators=500)
    clf_rf_random = RandomizedSearchCV(estimator=clf_rf, param_distributions=random_grid,
                                       n_iter=360, cv=5, verbose=2, random_state=0, n_jobs=-1)

    clf_rf_random.fit(train_features[0], train_labels)

    logging.debug('##############################')
    logging.debug('Best parameters:\n')
    logging.debug(clf_rf_random.best_estimator_)

    return clf_rf_random


def grid_search(js_dirs, labels_d, n=4, tolerance='false', dict_not_hash=True):
    """
        Grid search algorithm to get the optimal set of hyperparameters.

        -------
        Parameter:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed. Format: [Dir1, Dir2]
        - labels_d: list of strings
            Indicates the label's name of the current data: either benign or malicious.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed. Default: 4.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
            Default: True.

        -------
        Returns:
        - RandomForestClassifier:
            The classifier with the best set of hyperparameters.
    """

    names, train_features, train_labels = static_analysis.main_analysis \
        (js_dirs=js_dirs, labels_dirs=labels_d, js_files=None, labels_files=None,
         tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

    # Number of trees in the forest
    n_estimators = [int(x) for x in np.linspace(start=500, stop=700, num=5)]

    # Number of features to consider at each split
    max_features = [int(x) for x in np.linspace(start=200, stop=300, num=3)]

    # Maximum number of levels in the tree
    max_depth = [90, 100, 110, None]

    # Criterion to measure the quality of a split
    criterion = ['gini', 'entropy']

    # Create the grid
    grid = {'n_estimators': n_estimators,
            'max_features': max_features,
            'max_depth': max_depth,
            'criterion': criterion
            }

    clf_rf = utility.classifier_choice(estimators=500)
    clf_rf_random = GridSearchCV(estimator=clf_rf, param_grid=grid, cv=5, verbose=2, n_jobs=-1)

    clf_rf_random.fit(train_features[0], train_labels)

    logging.debug('##############################')
    logging.debug('Best parameters:\n')
    logging.debug(clf_rf_random.best_estimator_)

    return clf_rf_random


def evaluate(model, test_features, test_labels):
    """
        Evaluate the performance of a model.

        -------
        Parameters:
        - model: RandomForestClassifier
            Model to be used to test unknown features.
        - test_features: list
            List of the features considered.
        - test_labels: list
            List of the labels considered (corresponding to the previous features).

        -------
        Returns:
        - Float:
            The accuracy of the classifier.
    """

    predictions = model.predict(test_features)
    predictions_proba = model.predict_proba(test_features)
    accuracy = model.score(test_features, test_labels)  # Detection rate

    tn_test, fp_test, fn_test, tp_test = confusion_matrix(test_labels, predictions_proba).ravel()

    fpr, tpr, thresholds = roc_curve(test_labels, predictions[:, 1], pos_label='malicious')
    get_optimal_threshold(fpr, tpr, thresholds)

    print("Detection: " + str(accuracy))
    print("TN: " + str(tn_test) + ", FP: " + str(fp_test) + ", TP: " + str(tp_test)
          + ", FN: " + str(fn_test))

    return accuracy


def test_param(best_random, js_dirs_train, labels_d_train, js_dirs_test, labels_d_test,
               n=4, tolerance='false', dict_not_hast=True):
    """
        Random search algorithm to get the optimal set of hyperparameters.

        -------
        Parameters:
        - best_random: RandomForestClassifier:
            The classifier to be used.
        - js_dirs_train: list of strings
            Directories containing the JS files to be used to train the clf. Format: [Dir1, Dir2]
        - labels_d_train: list of strings
            Labels to train the classifier.
        - js_dirs_test: list of strings
            Directories containing the JS files to be used to test the clf. Format: [Dir1, Dir2]
        - labels_d_test: list of strings
            Labels to test the classifier.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed. Default: 4.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
                - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
            Default: True.

        -------
        Returns:
        - The classifier with the best set of hyperparameters.
    """

    _, features_train, labels_train = static_analysis.main_analysis \
        (js_dirs=js_dirs_train, labels_dirs=labels_d_train, js_files=None, labels_files=None,
         tolerance=tolerance, n=n, dict_not_hash=dict_not_hast)

    _, features_test, labels_test = static_analysis.main_analysis \
        (js_dirs=js_dirs_test, labels_dirs=labels_d_test, js_files=None, labels_files=None,
         tolerance=tolerance, n=n, dict_not_hash=dict_not_hast)

    random_accuracy = evaluate(best_random, features_test[0], labels_test)

    base_model = utility.classifier_choice(estimators=500)
    base_model.fit(features_train[0], labels_train)
    base_accuracy = evaluate(base_model, features_test[0], labels_test)

    logging.info('Improve of {:0.2f}%.'.format(100 *
                                               (random_accuracy - base_accuracy) / base_accuracy))
