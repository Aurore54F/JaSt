
"""
    Main module to classify JavaScript files using a given model.
"""

import os
import pickle
import argparse
import logging

import utility
import static_analysis


def test_model(names, labels, attributes, model, print_res=True, print_res_verbose=False,
               print_score=True, threshold=0.29):
    """
        Use an existing model to classify new JS inputs.

        -------
        Parameters:
        - names: list
            Name of the data files used to be tested using the following model.
        - labels: list
            Labels (i.e. 'benign', 'malicious', or '?') of the test data using the model.
        - attributes: csr_matrix
            Features of the data used to be tested using the following model.
        - model
            Model to be used to classify new observations.
        Beware: the model must have been constructed using files of the same format
        (i.e. same attributes) as the format of test_file.
        - print_res: bool
            Indicates whether to print or not the classifier's predictions.
        - print_res_verbose: bool
            Indicates whether to print or not the classifier's predictions, including the
            probability of membership for each class.
        - print_score: bool
            Indicates whether to print or not the classifier's performance.
        - threshold: float
            Probability of a sample being malicious over which the sample will be classified
            as malicious.

        -------
        Returns:
        - list:
            List of labels predicted.
    """

    if isinstance(model, str):
        model = pickle.load(open(model, 'rb'))

    labels_predicted_proba_test = model.predict_proba(attributes)
    # Probability of the samples for each class in the model.
    # First column = benign, second = malicious.
    # labels_predicted_test = model.predict(attributes_test)
    # accuracy_test = model.score(attributes_test, labels_test)  # Detection rate

    labels_predicted_test = utility.\
        predict_labels_using_threshold(len(names), labels_predicted_proba_test, threshold)
    # Perform classification using a threshold (probability of the sample being malicious)
    # to predict the target values

    if print_res:
        utility.get_classification_results(names, labels_predicted_test)

    if print_res_verbose:
        utility.get_classification_results_verbose(names, labels, labels_predicted_test,
                                                   labels_predicted_proba_test, model,
                                                   attributes, threshold)

    if print_score:
        utility.get_score(labels, labels_predicted_test)

    return labels_predicted_test


def parsing_commands():
    """
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * js_dirs=arg_obj['d'],
          * labels_d=arg_obj['l'],
          * js_files=arg_obj['f'],
          * labels_f=arg_obj['lf'],
          * model=arg_obj['m'],
          * threshold=arg_obj['th'],
          * tolerance=arg_obj['t'][0],
          * n=arg_obj['n'][0].
          A more thorough description can be obtained:
            >$ python3 <path-of-clustering/classifier.py> -help
    """

    parser = argparse.ArgumentParser(description='Given a list of directory or file paths,\
    detects the malicious JS inputs.')

    parser.add_argument('--d', metavar='DIR', type=str, nargs='+',
                        help='directories containing the JS files to be analyzed')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious', '?'],
                        help='labels of the JS directories to evaluate the model from')
    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analyzed')
    parser.add_argument('--lf', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious', '?'],
                        help='labels of the JS files to evaluate the model from')
    parser.add_argument('--m', metavar='MODEL', type=str, nargs=1,
                        help='path of the model used to classify the new JS inputs '
                             + '(see >$ python3 <path-of-clustering/learner.py> -help) '
                             + 'to build a model)')
    parser.add_argument('--th', metavar='THRESHOLD', type=float, nargs=1, default=[0.29],
                        help='threshold over which all samples are considered malicious')
    utility.parsing_commands(parser)

    return vars(parser.parse_args())


arg_obj = parsing_commands()
utility.control_logger(arg_obj['v'][0])


def main_classification(js_dirs=arg_obj['d'], js_files=arg_obj['f'], labels_f=arg_obj['lf'],
                        labels_d=arg_obj['l'], model=arg_obj['m'], threshold=arg_obj['th'],
                        n=arg_obj['n'][0], tolerance=arg_obj['t'][0],
                        dict_not_hash=arg_obj['dnh'][0]):
    """
        Main function, performs a static analysis (syntactic) of JavaScript files given as input
        before predicting if the executables are benign or malicious.

        -------
        Parameters:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed.
        - js_files: list of strings
            Files to be analysed.
        - labels_f: list of strings
            Indicates the label's name of the files considered: either benign or malicious.
        - labels_d: list of strings
            Indicates the label's name of the current data: either benign or malicious.
        - model: str
            Path to the model used to classify the new files
        - threshold: int
            Threshold over which all samples are considered malicious
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        The results of the static analysis of the files given as input:
        either benign or malicious
    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be studied')

    elif js_dirs is not None and labels_d is not None and len(js_dirs) != len(labels_d):
        logging.error('Please, indicate either as many directory labels as the number '
                      + str(len(js_dirs))
                      + ' of directories to analyze or no directory label at all')

    elif js_files is not None and labels_f is not None and len(js_files) != len(labels_f):
        logging.error('Please, indicate either as many file labels as the number '
                      + str(len(js_files))
                      + ' of files to analyze or no file label at all')

    elif model is None:
        logging.error('Please, indicate a model to be used to classify new files.\n'
                      + '(see >$ python3 <path-of-clustering/learner.py> -help)'
                      + ' to build a model)')

    else:
        names, attributes, labels = static_analysis.main_analysis \
            (js_dirs=js_dirs, labels_dirs=labels_d, js_files=js_files, labels_files=labels_f,
             tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

        if names:
            # Uncomment to save the analysis results in pickle objects.
            """
            utility.save_analysis_results(os.path.join(js_dirs[0], "Analysis-n" + str(n) + "-dict"
                                                       + str(dict_not_hash)),
                                          names, attributes, labels)
            """

            test_model(names, labels, attributes, model=model[0], threshold=threshold[0])

        else:
            logging.warning('No file found for the analysis.\n'
                            + '(see >$ python3 <path-of-js/is_js.py> -help)'
                            + ' to check your files correctness.\n'
                            + 'Otherwise they may not contain enough n-grams)')


if __name__ == "__main__":  # Executed only if run as a script
    main_classification()


def classify_analysis_results(save_dir, model, threshold):
    """
        Uses the results of a static analysis (syntactic) of JavaScript files to predict if the
        executables are benign or malicious.

        -------
        Parameters:
        - save_dir: str
            Path of the directory where the results (i.e. names of the files considered, their true
            label as well as their attributes) are stored.
        - model: str
            path to the model used to classify the new files
        - threshold: int
            threshold over which all samples are considered malicious

        -------
        Returns:
        The results of the static analysis of the files given as input:
        either benign or malicious
    """

    names = pickle.load(open(os.path.join(save_dir, 'Names'), 'rb'))
    attributes = pickle.load(open(os.path.join(save_dir, 'Attributes'), 'rb'))
    labels = pickle.load(open(os.path.join(save_dir, 'Labels'), 'rb'))

    test_model(names, labels, attributes, model=model, threshold=threshold)
