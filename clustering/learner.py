
"""
    Main module to build a model to classify future JavaScript files.
"""

import os
import pickle
import argparse
import logging

import utility
import static_analysis


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def classify(names, labels, attributes, model_dir, model_name, estimators,
             print_score=False, print_res=False):
    """
        Training a classifier.

        -------
        Parameters:
        - names: list
            Name of the data files used to build a model from.
        - labels: list
            Labels (i.e. 'benign', 'malicious') of the data used to build a model from.
        - attributes: np.array
            Features of the data used to build a model from.
        - model_dir: str
            Path to store the model that will be produced.
        - model_name: str
            Name of the model that will be produced.
        - estimators: int
            Number of trees in the forest.
        - print_score: bool
            Indicates whether to print or not the classifier's performance. Default: False.
        - print_res: bool
            Indicates whether to print or not the classifier's predictions. Default: False.

        -------
        Returns:
        - The selected model constructed using the training attributes.
            Beware: the model was implemented as a global variable in sklearn.
        - If specified, can also:
            * Print the detection rate and the TP, FP, FN and TN rates of
            the training names tested with the model built from the training attributes, in stdout.
            It will only work for these two classes: 'benign' and 'malicious'.
            * Print the classifier's predictions.
            Beware, the predictions made using the same file to build and test
            the model will give hopelessly optimistic results.
            See >$ python3 <path-of-clustering/classifier.py> -help
            to test a model on new files.
    """

    # Directory to store the classification related files
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    clf = utility.classifier_choice(estimators=estimators)
    trained = clf.fit(attributes, labels)  # Model
    labels_predicted = clf.predict(attributes)  # Classification and class predictions

    if print_score:
        utility.get_score(labels, labels_predicted)

    if print_res:
        utility.get_classification_results(names, labels_predicted)

    model_path = os.path.join(model_dir, model_name)
    pickle.dump(trained, open(model_path, 'wb'))
    logging.info('The model has been successfully stored in ' + model_path)

    return trained


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
          * model_dir=arg_obj['md'][0],
          * model_name=arg_obj['mn'][0],
          * print_score=arg_obj['ps'][0],
          * print_res=arg_obj['pr'][0],
          * estimators=arg_obj['nt'][0],
          * tolerance=arg_obj['t'][0],
          * n=arg_obj['n'][0].
          A more thorough description can be obtained:
            >$ python3 <path-of-clustering/learner.py> -help
    """

    parser = argparse.ArgumentParser(description='Given a list of directory or file paths, '
                                                 + 'builds a model to classify future '
                                                 + 'JS inputs.')

    parser.add_argument('--d', metavar='DIR', type=str, nargs='+',
                        help='directories to be used to build a model from')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious'],
                        help='labels of the JS directories used to build a model from')
    parser.add_argument('--f', metavar='FILE', type=str, nargs='+',
                        help='files to be used to build a model from')
    parser.add_argument('--lf', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious'],
                        help='labels of the JS files used to build a model from')
    parser.add_argument('--md', metavar='MODEL-DIR', type=str, nargs=1,
                        default=[os.path.join(src_path, 'Classification')],
                        help='path to store the model that will be produced')
    parser.add_argument('--mn', metavar='MODEL-NAME', type=str, nargs=1,
                        default=['model'],
                        help='name of the model that will be produced')
    parser.add_argument('--ps', metavar='BOOL', type=bool, nargs=1, default=[False],
                        help='indicates whether to print or not the classifier\'s detection rate')
    parser.add_argument('--pr', metavar='BOOL', type=bool, nargs=1, default=[False],
                        help='indicates whether to print or not the classifier\'s predictions')
    parser.add_argument('--nt', metavar='NB_TREES', type=int, nargs=1,
                        default=[500], help='number of trees in the forest')
    utility.parsing_commands(parser)

    return vars(parser.parse_args())


arg_obj = parsing_commands()
utility.control_logger(arg_obj['v'][0])


def main_learn(js_dirs=arg_obj['d'], js_files=arg_obj['f'], labels_f=arg_obj['lf'],
               labels_d=arg_obj['l'], model_dir=arg_obj['md'], model_name=arg_obj['mn'],
               print_score=arg_obj['ps'], print_res=arg_obj['pr'], dict_not_hash=arg_obj['dnh'][0],
               n=arg_obj['n'][0], tolerance=arg_obj['t'][0], estimators=arg_obj['nt']):
    """
        Main function, performs a static analysis (syntactic) of JavaScript files given as input
        to build a model to classify future JavaScript files.

        -------
        Parameters:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed.
        - js_files: list of strings
            Files to be analysed.
        - labels_f: list of strings
            Indicates the label's name of the files considered: either benign or malicious.
        - labels_d: list of strings
            Indicates the label's name of the directories considered: either benign or malicious.
        - model_dir: String
            Path to store the model that will be produced.
            Default value being the folder JS-Analysis/Classification/.
        - model_name: String
            Name of the model that will be produced.
            Default value being model.
        - print_score: Boolean
            Indicates whether to print or not the classifier's performance.
        - print_res: Boolean
            Indicates whether to print or not the classifier's predictions.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed.
        - estimators: int
            Number of trees in the forest.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).
    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be used to build a model from')

    elif labels_d is None and labels_f is None:
        logging.error('Please, indicate the labels (either benign or malicious) of the files'
                      + ' used to build the model')

    elif js_dirs is not None and (labels_d is None or len(js_dirs) != len(labels_d)):
        logging.error('Please, indicate as many directory labels as the number '
                      + str(len(js_dirs)) + ' of directories to analyze')

    elif js_files is not None and (labels_f is None or len(js_files) != len(labels_f)):
        logging.error('Please, indicate as many file labels as the number '
                      + str(len(js_files)) + ' of files to analyze')

    else:
        names, attributes, labels = static_analysis.main_analysis\
            (js_dirs=js_dirs, labels_dirs=labels_d, js_files=js_files, labels_files=labels_f,
             tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

        if names:
            # Uncomment to save the analysis results in pickle objects.
            """
            utility.save_analysis_results(os.path.join(model_dir[0], "Analysis-n" + str(n) + "-dict"
                                                       + str(dict_not_hash)),
                                          names, attributes, labels)
            """

            classify(names, labels, attributes, model_dir=model_dir[0], model_name=model_name[0],
                     print_score=print_score[0], print_res=print_res[0], estimators=estimators[0])

        else:
            logging.warning('No file found for the analysis.\n'
                            + '(see >$ python3 <path-of-js/is_js.py> -help)'
                            + ' to check your files correctness.\n'
                            + 'Otherwise they may not contain enough n-grams)')


if __name__ == "__main__":  # Executed only if run as a script
    main_learn()
