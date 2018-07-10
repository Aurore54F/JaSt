
"""
    Main module to update a model to classify future JavaScript files.
"""

import os
import pickle
import argparse
import logging

import utility
import static_analysis


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def validate(labels_validation, attributes_validation, model, model_name, model_dir, add_trees=100):
    """
        Extension of a classification model with new attributes of the same format as the model's.

        -------
        Parameters:
        - labels_validation: list
            Labels (i.e. 'benign', 'malicious',or '?') of the data used to extend the model.
        - attributes_validation: csr_matrix
            Features of the data used to extend the following model.
        - model
            Model to be updated.
            Beware: the model must have been constructed using files of the same format
            (i.e. same attributes format) as the format of attributes_validation.
        - model_name: str
            Name of the model that will be produced.
        - model_dir: str
            Path to store the model that will be produced.
        - add_trees: int
            For RF, number of trees that will be added to the model. Default value: 100.

        -------
        Returns:
        - The selected model updated using the validation file.
            Beware: the model was implemented as a global variable in sklearn.
    """

    if isinstance(model, str):
        model = pickle.load(open(model, 'rb'))

    # Directory to store the classification related files
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Incremental fit on a batch of samples
    model.set_params(warm_start=True)  # RF
    model.n_estimators += add_trees  # RF
    validated = model.fit(attributes_validation, labels_validation)  # RF

    model_path = os.path.join(model_dir, model_name)
    pickle.dump(validated, open(model_path, 'wb'))
    logging.info('The model has been successfully updated in ' + model_path)

    return validated


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
          * old_model=arg_obj['m'][0],
          * model_dir=arg_obj['md'][0],
          * model_name=arg_obj['mn'][0],
          * add_trees=arg_obj['at'][0],
          * tolerance=arg_obj['t'][0],
          * n=arg_obj['n'][0].
          A more thorough description can be obtained:
            >$ python3 <path-of-clustering/learner.py> -help
    """

    parser = argparse.ArgumentParser(description='Given a list of directory or file paths, '
                                                 + 'updates a model to classify future '
                                                 + 'JS inputs.')

    parser.add_argument('--d', metavar='DIR', type=str, nargs='+',
                        help='directories to be used to update a model with')
    parser.add_argument('--l', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious'],
                        help='labels of the JS directories used to update a model with')
    parser.add_argument('--f', metavar='FILE', type=str, nargs='+',
                        help='files to be used to update a model with')
    parser.add_argument('--lf', metavar='LABEL', type=str, nargs='+',
                        choices=['benign', 'malicious'],
                        help='labels of the JS files used to update a model with')
    parser.add_argument('--m', metavar='OLD-MODEL', type=str, nargs=1,
                        help='path of the old model you wish to update with new JS inputs')
    parser.add_argument('--md', metavar='MODEL-DIR', type=str, nargs=1,
                        default=[os.path.join(src_path, 'Classification')],
                        help='path to store the model that will be produced')
    parser.add_argument('--mn', metavar='MODEL-NAME', type=str, nargs=1,
                        default=['model'],
                        help='name of the model that will be produced')
    parser.add_argument('--at', metavar='NB_TREES', type=int, nargs=1,
                        default=[100], help='number of trees to be added into the forest')
    utility.parsing_commands(parser)

    return vars(parser.parse_args())


arg_obj = parsing_commands()
utility.control_logger(arg_obj['v'][0])


def main_update(js_dirs=arg_obj['d'], js_files=arg_obj['f'], labels_f=arg_obj['lf'],
                labels_d=arg_obj['l'], old_model=arg_obj['m'], model_dir=arg_obj['md'],
                model_name=arg_obj['mn'], n=arg_obj['n'][0], tolerance=arg_obj['t'][0],
                add_trees=arg_obj['at'], dict_not_hash=arg_obj['dnh'][0]):
    """
        Main function, performs a static analysis (syntactic) of JavaScript files given as input
        to extend an existing model to classify future JavaScript files.

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
        - old_model: String
            Path of the old model you wish to update with new JS files.
        - model_dir: String
            Path to store the model that will be produced.
            Default value being the folder JS-Analysis/Classification/.
        - model_name: String
            Name of the model that will be produced.
            Default value being model.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed.
        - add_trees: int
            Number of trees to be added into the forest.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsingCommands()).

        -------
        Returns:
        - Naive Bayes Multinomial model
            Beware: the model was implemented as a global variable in sklearn.
    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be used to update '
                      + 'the old model with')

    elif labels_d is None and labels_f is None:
        logging.error('Please, indicate the labels (either benign or malicious) of the files '
                      + 'used to update the model')

    elif js_dirs is not None and (labels_d is None or len(js_dirs) != len(labels_d)):
        logging.error('Please, indicate as many directory labels as the number '
                      + str(len(js_dirs)) + ' of directories to analyze')

    elif js_files is not None and (labels_f is None or len(js_files) != len(labels_f)):
        logging.error('Please, indicate as many file labels as the number '
                      + str(len(js_files)) + ' of files to analyze')

    elif old_model is None:
        logging.error('Please, indicate the path of the old model you would like to update.\n'
                      + '(see >$ python3 <path-of-clustering/learner.py> -help)'
                      + ' to build a model)')

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

            validate(labels, attributes, model=old_model[0], add_trees=add_trees[0],
                     model_name=model_name[0], model_dir=model_dir[0])

        else:
            logging.warning('No file found for the analysis.\n'
                            + '(see >$ python3 <path-of-js/is_js.py> -help)'
                            + ' to check your files correctness.\n'
                            + 'Otherwise they may not contain enough n-grams)')


if __name__ == "__main__":  # Executed only if run as a script
    main_update()
